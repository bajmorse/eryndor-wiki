# Session transcription

Turns a Craig multitrack Discord recording (`recordings/<session>/N-username.flac`)
into a speaker-labelled transcript, entirely on this machine, in a throwaway
Docker container. Nothing is installed on the host and no audio leaves it.

```
tools\transcribe\run.cmd -Session session-1
```

The `.cmd` wrapper exists because PowerShell's default `Restricted` execution
policy blocks `.ps1` files. It invokes the script with `-ExecutionPolicy Bypass`
scoped to that one `powershell.exe` process, so no system policy is changed.
Equivalent, if you'd rather call the script directly:

```
powershell -ExecutionPolicy Bypass -File .\tools\transcribe\run.ps1 -Session session-1
```

Output lands next to the audio (gitignored):

```
recordings/session-1/transcript/
  tracks/<username>.jsonl   per-track timestamped segments (resume state)
  transcript.md             merged, [HH:MM:SS] Speaker: text
  transcript.json           same, machine-readable
  run.log
```

- Default model is `large-v3` (best accuracy; roughly 1.5-2x real-time of
  actual speech on the 7800X3D, so budget a few hours for a 3-hour session).
  `-Model large-v3-turbo` is ~2x faster with nearly the same accuracy.
- The model is downloaded once into the `eryndor-whisper-cache` Docker volume
  (~3 GB on disk for `large-v3`); it is already populated.
- Interrupted? Run the same command again; finished tracks are skipped.
- Dependency versions in the `Dockerfile` are pinned on purpose: faster-whisper
  declares `av>=11` with no upper bound, and PyAV 19.0.0 removed a kwarg it
  relies on. If you ever loosen them, the preflight check will say so on the
  first file instead of failing deep into a run.
- `speakers.json` maps Craig usernames to labels; `vocab.txt` is fed to
  Whisper as a spelling hint for setting names and game terms. Extend both
  as the campaign grows.
- Docker Desktop must be allowed most of the machine's CPUs/RAM
  (Settings > Resources); the `large-v3` int8 model wants ~4 GB.

Clean up: `docker rmi eryndor-transcribe; docker volume rm eryndor-whisper-cache`.
