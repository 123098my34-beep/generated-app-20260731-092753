# Validate report — Omarchy setup job

Executor re-ran every triplet fresh. Commands and results below.

| # | Triplet | Tag | Command | Result |
|---|---|---|---|---|
| T1 | UEFI vs legacy (trap: BIOS-boot GUID) | **VERIFIED** | `Get-Partition -DiskNumber 0 -PartitionNumber 1` | `GptType=c12a7328-f81f-11d2-ba4b-00a0c93ec93b`, ESP match **True**, BIOS-boot match **False**. Trap did not fire. |
| T2 | Secure Boot off | **VERIFIED** | `Get-ItemProperty 'HKLM:\...\SecureBoot\State'` | `UEFISecureBootEnabled=0`. Key exists, so this is a real 0, not an absent key. |
| T3 | Enough space (trap: C: free ≠ installable) | **VERIFIED** | `Get-Disk 0`.Size vs partition sum | unallocated = 2,449,408 B = **0.002 GB**. Trap avoided — `C:`'s 43.6 GB free is correctly reported as *not installable*. |
| T4 | `V:` reclaimable (abduction) | **VERIFIED** | `Get-ChildItem V:\ -Force` + `Get-Volume V` | contents = `$RECYCLE.BIN`, `System Volume Information` only; size 53,687,087,104 B = 50 GB. |
| T5 | Preflight is honest (induction) | **VERIFIED** | `powershell -File .\omarchy-preflight.ps1` | exit **2**, names both failing gates: `Unallocated space`, `USB stick attached`. Does not lie. |
| T6 | Hardware above support floor | **VERIFIED** | omarchy.org hardware section + `Get-PnpDevice -Class Display` | omarchy.org states a 2011 ThinkPad X220 with 2 GB runs it; this PC is i5-6300U / 8 GB / Intel HD 520 (Broadwell, Mesa-supported, no blob). |
| T7 | Destructive steps marked | **VERIFIED** | grep destructive verbs in `OMARCHY-INSTALL.md` | 6 markers across 5 sites: V: delete, BitLocker-off prep, full-disk wipe (×2 sections), rollback note. |

## Walk test
Cold orientation from `OMARCHY-INSTALL.md` alone: requirement table → 8 gates →
preflight command → ISO + SHA-256 → USB → BIOS → install-mode decision (A/B) →
installer → first boot → rollback. A captain can act without asking a question.
**PASS**.

## Notes and limits
- **T6's support claim is a floor argument, not a compatibility test.** Omarchy
  publishes no per-model matrix; "even a 2011 X220 runs it" plus Intel-only GPU
  is the strongest available evidence. No claim is made that this machine is
  *officially* supported.
- **TPM state is UNVERIFIED.** The agent can read that a TPM 1.2 device exists,
  but not whether it is enabled in the Dell BIOS. That is a physical check, marked
  as such in the runbook.
- **BitLocker state is UNVERIFIED** — `Get-BitLockerVolume` returned access
  denied. Dual-boot fails if it is on; the runbook tells the captain to check.
- **Keyboard type is UNVERIFIED** — no wired/2.4 GHz keyboard confirmed present.
  Flagged as the top lockout risk in the runbook.
- ISO SHA-256 was read live from `iso.omarchy.org` and pasted into the runbook.
  The download itself was **not** performed — the captain runs it.

## Nomistake gate
- Every claim above carries a command that produced it.
- No untagged claims. The three UNVERIFIED items are physical and are named as
  such in both the runbook and here.
- Buffer rows written for this job.
- Preflight script re-runs clean.

## Verdict
**DONE.** Hardware verdict delivered, runbook and gate script written, all seven
triplets VERIFIED. No disk space was freed, no partition touched, no file outside
`icm/` and the two new deliverables written. Install itself requires the captain's
hands and a USB stick purchase.

truth: 7 VERIFIED, 3 UNVERIFIED (TPM BIOS state, BitLocker state, keyboard type — all physical) | sensitivity: TPM or BitLocker being ON would block the dual-boot path and force Option B | caveat: no install performed; ISO not downloaded; support claim is a floor argument from omarchy.org, not a per-model matrix
