---
title: Players
---

# Players

Who plays whom, and how they show up in the Discord (Craig) session recordings.

| Player | Character | Discord / Craig track |
|---|---|---|
| Brenton | GM | `twill` |
| Chris | [[Aangry Mank]] | `ctag_` |
| Rory | [[Nyx Ashwisk]] | `rory676` |
| Ryan | [[Zella Ironstone]] | `captain_racoonz` |
| Kyle | [[Frayne Castel]] | `ahidingcamel` |
| Mike | [[Finnegan Endercast]] | `tezlagunner66` |

## Session recordings

Sessions are recorded with the Craig bot in the **Session** voice channel and exported as a multitrack FLAC set into `recordings/<session>/` in the repository (gitignored — too large to push). Each export contains:

- `N-username.flac` — one time-aligned track per participant, all padded to the same length.
- `o2rAHcYDl1HQ.flac`-style file — the merged mix of every track.
- `info.txt` — Craig's metadata: guild, channel, requester, start time (UTC), track list.
- `raw.dat` — Craig's raw capture the FLACs were rendered from; not needed.

The per-participant tracks are what make automatic transcription reliable: transcribing each one separately gives exact speaker attribution with no diarization guesswork. `tools/transcribe/run.ps1` does this in Docker and produces `recordings/<session>/transcript/transcript.md`, which is the source material for each session's notes under [[Session Info]]. The track mapping above lives in `tools/transcribe/speakers.json`; update both if a player's Discord name changes.
