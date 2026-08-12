# Eryndor Wiki

The campaign wiki for Eryndor, a fantasy setting run as a Daggerheart TTRPG campaign. Built with [Quartz](https://quartz.jzhao.xyz/) and published as two separate static sites from one shared content base:

- **[wiki.eldressa.fyi](https://wiki.eldressa.fyi)** — the player-facing wiki. World lore, geography, peoples, history.
- **gm.eldressa.fyi** — the private GM wiki (Cloudflare Access-gated). Everything in the player wiki, plus storylines, session notes, NPC secrets, and campaign planning.

## Repository structure

```
content/    Canonical player-facing lore. Published to both sites.
gm/         GM-only material. Published only to the GM site.
info/       Reference material (world encyclopedia, session recaps) used
            for authoring. Not part of either built site.
quartz/     The Quartz site generator itself (vendored, plugin-loader
            architecture — see quartz.config.yaml for the plugin list).
scripts/    prepare-gm-content.mjs, which merges content/ + gm/ for the
            GM build.
```

Player and GM pages can freely `[[wikilink]]` to each other. A page under
`content/` never needs to know it's also being read by the GM build.

## Development

Open this repo in [GitHub Codespaces](https://github.com/features/codespaces) for a ready-to-go environment (Node 22, Quartz plugins, Claude Code, and both preview ports pre-configured). Then:

```bash
npm run dev:player   # live preview of the player site at :8080
npm run dev:gm       # live preview of the GM site (content/ + gm/) at :8081
```

There's no local dev setup required on the self-hosted production host — everything Quartz-related runs in Codespaces or in CI.

## Publishing

Commit and push to `main`:

```bash
git add -A
git commit -m "..."
git push github main
```

That's the entire deploy step. GitHub Actions builds both sites into Docker images and publishes them to GHCR; a Watchtower instance on the production host picks up new images automatically within a few minutes. See `CLAUDE.md` for the full breakdown of the build/deploy architecture, including how GM content is kept out of the player build.

## GM/player separation

The player build only ever reads `content/` — `gm/` is never copied into its Docker build context, so GM material is physically absent from the player site's build artifact, not just hidden from navigation. The GM build merges `content/` and `gm/` together, so GM pages live under `/gm/...` alongside the full player wiki.

---

## Built with Quartz

This site runs on [Quartz](https://quartz.jzhao.xyz/), a static site generator for publishing digital gardens, by [Jacky Zhao](https://github.com/jackyzha0) and the Quartz community. If you want to build something similar, [the Quartz docs](https://quartz.jzhao.xyz/) are the place to start, and the [Discord community](https://discord.gg/cRFFHYye7t) is active and helpful.
