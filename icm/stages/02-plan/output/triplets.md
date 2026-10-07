# Triplets — proposed before solving

Each triplet: claim, type, acceptance rule, how to run.

## T1 — UEFI vs legacy (deduction)
**Claim**: disk 0 partition 1 is an EFI System Partition, therefore the machine
boots in UEFI mode.
**Type**: deduction. Input: `Get-Partition -DiskNumber 0` GptType. Expected:
GUID `{c12a7328-f81f-11d2-ba4b-00a0c93ec93b}`.
**Trap**: that GUID is *also* the MBR-system-type GUID on some tools. Must
distinguish from the BIOS-boot GUID `{21686148-6449-6e6f-744e-656564454649}`.
If it matches the BIOS-boot GUID, UEFI is FALSE.
**Acceptance**: VERIFIED only if GUID == ESP GUID **and** != BIOS-boot GUID.
**Run**: `Get-Partition -DiskNumber 0 -PartitionNumber 1 | Select-Object Type,GptType`

## T2 — Secure Boot state (deduction)
**Claim**: Secure Boot is already disabled, so no BIOS change is needed for it.
**Type**: deduction. Input: HKLM `SecureBoot\State\UEFISecureBootEnabled`.
Expected: `0`.
**Acceptance**: VERIFIED only if the value reads `0`. A missing key is UNVERIFIED,
not `0` — registry absence means the OS cannot report it.
**Run**: `(Get-ItemProperty 'HKLM:\SYSTEM\CurrentControlSet\Control\SecureBoot\State').UEFISecureBootEnabled`

## T3 — Enough space to install (deduction)
**Claim**: no install mode is currently satisfiable without freeing space.
**Type**: deduction. Inputs: disk size, sum of partition sizes, per-volume free.
Expected: unallocated == diskSize - sumPartitions ≈ 0.
**Trap**: `Get-Volume` free space on `C:` is NOT installable space — Omarchy's
free-space install needs *unallocated*, not "free inside a partition".
**Acceptance**: VERIFIED only if unallocated < 32 GB. If someone reports "43 GB
free on C:", that is a FALSE positive of the trap.
**Run**: compare `(Get-Disk 0).Size` to `(Get-Partition -DiskNumber 0 | Measure-Object Size -Sum).Sum`

## T4 — Reclaimable partition (abduction)
**Claim**: `V:` is safe to reclaim for a dual-boot install.
**Type**: abduction. Given the goal "~50 GB unallocated", which existing
partition yields it? Expected: `V:`.
**Acceptance**: VERIFIED only if `V:` is ~50 GB **and** contains nothing but
`$RECYCLE.BIN` + `System Volume Information`. Never assert this without listing
its contents — a partition labelled "Isolated" may hold real data.
**Run**: `Get-ChildItem V:\ -Force` + `Get-Volume -DriveLetter V`

## T5 — Preflight gate is honest (induction)
**Claim**: `omarchy-preflight.ps1` exits non-zero on this machine right now.
**Type**: induction. Examples: USB absent (0 removable volumes), unallocated
~0. Both fail → non-zero expected.
**Acceptance**: VERIFIED only if the script exits non-zero **and** names at
least the two failing gates by name. A script that exits 0 here is lying.
**Run**: `pwsh -File omarchy-preflight.ps1; echo $LASTEXITCODE`

## T6 — Hardware supported by Omarchy (deduction)
**Claim**: i5-6300U / 8 GB / Intel HD 520 is above Omarchy's support floor.
**Type**: deduction. Inputs: CPU model, RAM, GPU. Expected: supported.
**Acceptance**: VERIFIED only if the cited support statement exists on
omarchy.org (the "2011 ThinkPad X220 with 2 GB" line) **and** the GPU is Intel
so no NVIDIA blob is needed. Cite the URL.
**Run**: read omarchy.org hardware section; `Get-PnpDevice -Class Display`

## T7 — Runbook has no unmarked destructive step (induction)
**Claim**: every irreversible step in `OMARCHY-INSTALL.md` is visibly marked.
**Type**: induction. Examples: partition delete, disk wipe, BitLocker off,
`diskpart clean` — all destructive.
**Acceptance**: VERIFIED only if each appears in a section flagged destructive,
and none of them appear in the script's *automatic* path without a confirm.
**Run**: grep the runbook for destructive verbs; count marked vs total.

## Round 2 — the aborted download (proposed after captain aborted, before retrying)

State at proposal time: `curl` was killed at 985,128,960 B of 6,185,304,064 B
(15.9%). A partial file exists on disk. The hard question is not "can I download
6 GB" — it is **whether resuming is byte-safe**.

### T8 — Range support (deduction)  ← the frontier
**Claim**: `iso.omarchy.org` honours HTTP range requests, therefore `curl -C -`
resumes at the correct offset and the result is byte-identical to a fresh fetch.
**Type**: deduction. Input: request with `Range: bytes=985128960-` against the ISO
URL. Expected: `206 Partial Content` + a `Content-Range` header starting at
985,128,960.
**Trap**: `200 OK` means the server **ignored** Range. Under `-C -` curl then
appends a second full copy to the partial file — 985 MB + 6.19 GB = corrupt, and
it looks like a successful download. This is the failure mode that eats 20
minutes and produces an unbootable stick.
**Acceptance**: VERIFIED resume-safe only if status == 206 **and**
`Content-Range` offset == 985128960. Any `200` → resume is UNSAFE, delete the
partial and refetch whole.
**Run**: `curl.exe -sI -H "Range: bytes=985128960-" https://iso.omarchy.org/omarchy-4.0.4.iso`

### T9 — Partial cannot pass the hash gate (deduction)
**Claim**: the 985,128,960 B partial will not verify against
`ddeded2758c48318d201dfdac905ecb28f570441883f0c052ea3cd5d05acf92d`.
**Type**: deduction. Input: current file. Expected: hash mismatch.
**Note**: low difficulty — this is the control, it must fail, proving the gate in
step 2 of the runbook actually has teeth rather than being decorative.
**Acceptance**: VERIFIED when the computed hash != expected. If it ever matched,
the download is not what it claims and everything downstream is suspect.
**Run**: `certutil -hashfile <file> SHA256`

### T10 — Wipe-the-partial is reversible, keeping it is not (abduction)
**Claim**: the correct action on an unverifiable partial file is to delete it, not
to trust it or hand it to a flasher.
**Type**: abduction. Given "file is truncated and cannot be verified", what
minimises risk? Expected: delete, refetch, verify hash, only then flash.
**Acceptance**: VERIFIED only if the runbook's ordering (download → verify →
flash) is not violated by any shortcut. Flashing an unverified ISO is the
failure this triplet exists to prevent.
**Run**: read `OMARCHY-INSTALL.md` steps 2–3, confirm verify precedes flash.

## Round 3 — proposed before U5–U8 (probe, delete, RST, download)

### T11 — Deletion script refuses on a non-empty V: (deduction)
**Claim**: `remove-V.ps1` exits non-zero and deletes nothing when `V:` contains
any file outside `$RECYCLE.BIN` / `System Volume Information`.
**Type**: deduction. Input: a planted file in `V:\probe.txt`. Expected: exit
**2**, partition still present.
**Trap**: `$RECYCLE.BIN` itself contains recycled files — listing only the
top-level names would pass a full recycle bin as "empty". The check must
exclude *paths inside* those two folders, not just their names.
**Acceptance**: VERIFIED only if (a) the refusal path runs on a planted file,
(b) partition count is unchanged afterward. Cannot plant then run without
elevation → the refusal branch is UNVERIFIED if the shell stays non-admin.
**Run**: `Get-Partition -DiskNumber 0 | Measure-Object` before/after.

### T12 — Stick-free path: SD reader exists and is alive (deduction)
**Claim**: the machine has a Realtek PCIE card reader, so an SD card is a
candidate boot medium.
**Type**: deduction. Input: `Get-PnpDevice` for `Realtek PCIE CardReader`.
Expected: FriendlyName matches, Status = OK.
**Acceptance**: VERIFIED only for **reader present and OK**. Whether firmware
offers it in the F12 menu stays UNVERIFIED — that can only be proven by
booting to the menu. Never collapse "reader exists" into "bootable".
**Run**: `Get-PnpDevice | Where-Object FriendlyName -match 'Card Reader|Realtek PCIE'`

### T13 — Agent cannot delete partitions (deduction)
**Claim**: this shell is not elevated, so `Remove-Partition` would fail here;
the captain must run it elevated.
**Type**: deduction. Input: `IsInRole(Administrator)`. Expected: `False`.
**Acceptance**: VERIFIED when the flag reads `False` — it did on first check,
re-check before relying on it. If ever `True`, T11 becomes executable and must
be run for real, not argued.
**Run**: `([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)`

### T14 — RST boot driver really is active (deduction)
**Claim**: Windows boots through `iaStorAC`, so an unprepared BIOS switch to
AHCI risks an inaccessible-boot-device stop.
**Type**: deduction. Input: `Get-Service iaStorAC, storahci`. Expected:
`iaStorAC` Status=Running StartType=Boot; `storahci` Stopped.
**Trap**: `iaStorV` (the legacy Intel driver) being Stopped does **not** mean
RST is inactive — the running one is `iaStorAC`. Reading the wrong entry gives
the opposite conclusion.
**Acceptance**: VERIFIED only if both services are read, and the BSOD-risk claim
is scoped as *"risk if switched unprepared"* — the actual failure is UNVERIFIED
until someone switches.
**Run**: `Get-Service -Name storahci,iaStorAC,iaStorV | Select Name,Status,StartType`

### T15 — Download completes to the exact byte (deduction)
**Claim**: resuming with `-C -` yields exactly 6,185,304,064 bytes and the
published hash.
**Type**: deduction. Input: resumed file. Expected: length + SHA-256 both match.
**Acceptance**: **both** must match. Length alone passes a truncated-but-padded
file; hash alone cannot be computed on a wrong-length file. Either missing →
UNVERIFIED.
**Run**: `Get-Item $f).Length` then `certutil -hashfile $f SHA256`

