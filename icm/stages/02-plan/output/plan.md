# Plan — Omarchy OS setup on this PC

Form: automation. Scope: inline. Deliverable: **runbook + hardware verdict**.
No partition is touched without explicit captain go.

## Units

### U1 — Hardware compatibility verdict
- **Goal**: decide whether this PC can run Omarchy 4.0.4, on measured evidence.
- **Acceptance**: every Omarchy hard requirement (UEFI, Secure Boot off, TPM off,
  RAM, disk, keyboard type) gets a VERIFIED / UNVERIFIED / FAIL tag with the
  command that produced it.
- **Paths**: read-only queries against `Get-Disk`, `Get-Partition`,
  `Get-PnpDevice`, `Get-Volume`, HKLM registry.
- **Done when**: no requirement is left untagged.
- **Verify**: re-run each command; tags must match output.

### U2 — Space plan (read-only)
- **Goal**: determine what disk space exists and what each install mode needs.
- **Acceptance**: total free space, per-volume free, unallocated space presence,
  and the reclaimable partition identified — with the exact free-space figure
  each mode (full-disk / free-space dual-boot) requires.
- **Paths**: `Get-Volume`, `Get-Partition -DiskNumber 0`, `Get-ChildItem V:\`.
- **Done when**: captain can pick a mode knowing the byte cost.
- **Verify**: partition sizes sum vs disk size.

### U3 — Runbook artifact
- **Goal**: write `OMARCHY-INSTALL.md` at repo root — the ordered steps, captain-
  facing, split into "safe / destructive" halves, with the irreversible steps
  marked.
- **Acceptance**: covers ISO download + SHA256, USB flash, BIOS changes, space
  prep, the installer wizard, first boot, and rollback (how to get Windows back).
- **Paths**: `OMARCHY-INSTALL.md`.
- **Done when**: captain can follow it without asking a question.
- **Verify**: every step traces to a VERIFIED hardware fact or a cited Omarchy
  doc line.

### U4 — Pre-flight script
- **Goal**: one PowerShell command the captain runs before touching anything,
  which re-prints every gate and exits non-zero if any gate fails.
- **Acceptance**: `pwsh -File omarchy-preflight.ps1` returns 0 only when UEFI +
  Secure Boot off + USB attached + enough space. No writes, no deletes.
- **Paths**: `omarchy-preflight.ps1`.
- **Done when**: it fails on this machine today (no USB, no unallocated space) —
  that failure is the point.
- **Verify**: run it; expect non-zero + the specific failing gate named.

## Dependencies
U1, U2, U4 are independent and read-only. U3 depends on U1 + U2 (the verdict and
the space numbers go into the runbook). Serialize only U3.

## Explicitly out of scope
- Deleting `V:` — captain's call, destructive.
- Shrinking `C:` — captain's call, destructive.
- Flashing a USB stick — no stick attached, and physical.
- Touching the BIOS — physical.

---

# Round 2 — captain decisions landed

Captain answered: **(a)** no USB stick, wants a non-stick boot path;
**(b)** approve **deleting the empty `V:`** partition. Both are now in scope.

## Units round 2

### U5 — Stick-free boot path
- **Goal**: boot the Omarchy ISO without a USB stick. Probe what the firmware
  can boot from (optical / SD card reader / second disk), then pick the least
  invasive path.
- **Acceptance**: one viable path identified, with its uncertainty marked
  UNVERIFIED until actually tested from firmware.
- **Paths**: read-only hardware probe (`Get-PnpDevice`, `Get-Volume`,
  `Get-Disk`).
- **Done when**: captain is told exactly which piece of media to supply, or
  which firmware-side route to use if none is available.
- **Verify**: the probe command output itself.

### U6 — Reclaim V:  ← captain-approved DESTRUCTIVE
- **Goal**: delete partition 4 (`V:`), freeing ~50 GB unallocated for the
  free-space install, while Windows and this repo stay intact.
- **Acceptance**: (i) script refuses if `V:` holds anything beyond
  `$RECYCLE.BIN` + `System Volume Information`; (ii) reports exact bytes freed;
  (iii) requires elevation (agent shell is **not** admin — verified).
- **Paths**: `remove-V.ps1` (repo root, new file).
- **Done when**: script runs clean or refuses for a stated reason; a refusal
  is a pass, not a failure.
- **Verify**: after run, `unalloc` on disk 0 ≈ 50 GB.

### U7 — Installer disk-visibility risk (RST/RAID)
- **Goal**: the disk is behind Intel RST (`iaStorAC` boot driver, BusType RAID).
  Omarchy's installer may not see it. Assess the AHCI switch — its risk and
  the safe prep if needed.
- **Acceptance**: risk stated with evidence; no registry or BIOS change made
  in this round — prep only if the installer actually fails to see the disk.
- **Paths**: read-only (`Get-Service`, `Get-Disk`).
- **Done when**: captain knows Windows may blue-screen (0x7B) on an
  unprepared AHCI switch, and that the fix is a small prep step first.
- **Verify**: `iaStorAC` Status=Running, StartType=Boot; `storahci` = Stopped.

### U8 — Finish the ISO (restarted in background)
- **Goal**: complete the 6.19 GB download and verify SHA-256 before any flash.
- **Acceptance**: file length == 6,185,304,064 **and** hash ==
  `ddeded2758c48318d201dfdac905ecb28f570441883f0c052ea3cd5d05acf92d`.
- **Paths**: `%USERPROFILE%\Downloads\omarchy-4.0.4.iso`.
- **Done when**: both match. A length match with a bad hash = UNVERIFIED, not pass.
- **Verify**: `certutil -hashfile ... SHA256`.

## New triplets
See `triplets.md` round 3 (T11–T14). Proposals written before solving U5–U8.
