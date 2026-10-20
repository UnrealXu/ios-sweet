# Working on ios-sweet

- Read `NOTES.md` before starting; it contains the project goal, hardware facts,
  current blocker, local artifact locations and the next concrete action.
- The user switches agents frequently. Update the active handoff in `NOTES.md`
  after each milestone and before stopping. Record commits, CI run IDs, exact
  build/boot results and unfinished work. Distinguish observations from guesses.
- Commit completed changes. Use `gh` for GitHub Actions kernel builds and logs.
  Local single-file cross-compiles are useful before spending a CI run.
- Subsequent kernel iterations default to workflow `build_mode=cached` and
  `diagnostic_artifacts=false`. Use the native XNU CCACHE interface and keyed
  caches on the branch containing the current workflow and kernel patches
  (currently `UnrealXu/ios-sweet:codex/ace-initial-platform`). Do not dispatch an
  older default-branch workflow that lacks the cached mode. Use
  source/KDK caches; reset restored sources and reapply current patches each
  time. Never cache fakeroot, generated XNU headers, raw build objects or linked
  kernels as a shortcut. Record real cache hits, build time and artifact hashes.
  Use `build_mode=full` for an uncached audit or cache-related diagnosis; it
  also preserves local compile-tree/KDK diagnostics. Request extra diagnostics
  explicitly when needed. Both paths retain entry and exact-artifact checks.
- The active device is OnePlus Ace PGKM10 / MT6895. Its bootloader has been
  verified to reject `fastboot boot`; do not repeat unsupported temporary
  boot attempts or apply the Redmi transport assumptions to Ace. Use only
  concrete, hash-checked images through the verified device-specific path.
- The user updated the bring-up workflow on 2026-10-20: retain the latest
  experimental image between tests and debug it in place. Do not routinely
  restore the original boot image after every trial. Keep the original
  partition backups intact and ready for explicitly requested or separately
  authorized recovery. Record the actual installed image and pending recovery
  state so a later agent does not silently roll back or repeat a write.
- The user approved (2026-10-15) using
  internal UFS for iOS and said Android may be deleted: the iOS root goes
  into the existing `userdata` partition (no GPT changes). Keep bootloaders,
  recovery, modem, persist and the backups intact.
- On 2026-10-20 the user explicitly replaced the per-step confirmation rule:
  proceed directly with necessary experimental boot-image and iOS-root writes
  within this project's already authorized scope; do not ask for confirmation
  on each write. Before each operation, prepare a concrete reviewable image,
  verify its hash, device/partition identity, backups and recovery path, and
  record the exact operation/result. This standing authorization does not
  expand scope to protected partitions, GPT changes or unrelated data. Keep
  the retain-experimental-image workflow; do not routinely restore backups.
- The user requires subsequent Ace candidates to use the physically verified
  automatic trial workflow (2026-10-20), rather than requesting manual Fastboot
  keys after each test. Build with a fresh run token, --pmsg, the hash-pinned
  Android refusal path and --auto-readout-after-reset. Verify the pending-trial
  latch/refusal and check that the new token is absent from pretrial evidence.
  After the guarded one-time boot_b write, run tools/ace-auto-trial.py with
  the private transport JSON and trial directory. It waits for diagnostic ADB,
  validates the current token, root/B-slot and boot/vendor hashes, saves
  pstore/dmesg/AEE, and returns the phone to Fastboot through ADB automatically.
  Before returning to Fastboot, refresh the serial-verified ADB transport and
  recheck the current token. Retain every return-record observation; re-read
  incomplete/malformed observations at most three times through refreshed
  identity-bound transports, but stop immediately for a complete different
  diagnostic record. These are read retries, never reboot retries. Retry that
  reboot at most once only for the exact
  pre-command "device not found" error; observe ambiguous errors without a
  second reboot, and verify firmware Fastboot (is-userspace=no) physically.
  Inspect the real logs, fix the next established failure, validate and package
  a new candidate, then repeat with a new token. Never blindly retry writes,
  restart a consumed controller, or call a log latch XNU/iOS success. Do not
  routinely restore the original backup. The complete warm-reset workflow was
  physically verified with candidate4115699e...ff24b7c: diagnostic ADB76.1s,
  logs collected, expected Fastboot ready, no manual keys. Manual help remains
  a last resort for lost RAM, ring overwrite or earlier firmware/entry faults;
  record the concrete failure before requesting it. Keep the protected
  partitions, GPT and original backups intact.
- Keep device dumps, serial numbers and downloaded Apple artifacts out of git.
- The user requested automatic phone screenshots on 2026-10-20. Whenever the
  expected phone has an identity-verified ADB connection, collect a screencap
  with trial evidence and inspect the image before claiming visible behavior.
  Keep screenshots private under research/. Android fallback screenshots prove
  only Android's visible state, never XNU display, touch or iOS success. ADB
  screenshots are unavailable while firmware Fastboot or an early kernel hang
  is active; record this limitation rather than inventing screen observations.
