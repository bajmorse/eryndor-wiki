import { loadQuartzConfig, loadQuartzLayout } from "./quartz/plugins/loader/config-loader"
import * as ExternalPlugin from "./.quartz/plugins"
import type { ExplorerOptions } from "./.quartz/plugins"

// Pins the top-level Explorer sidebar order: World Info first (from
// content/), then the GM-only sections scripts/prepare-gm-content.mjs
// merges in alongside it. Everything else keeps the plugin's default
// (folders first, alphabetical) sort. Must be a self-contained function —
// Explorer serializes it with .toString() and re-parses it client-side, so
// it can't close over outer variables.
const explorerSortFn: ExplorerOptions["sortFn"] = (a, b) => {
  const order = ["World Info", "Party Info", "Session Info", "Gamemaster Info"]
  const ai = order.indexOf(a.displayName ?? "")
  const bi = order.indexOf(b.displayName ?? "")
  if (ai !== -1 || bi !== -1) {
    if (ai === -1) return 1
    if (bi === -1) return -1
    return ai - bi
  }
  if ((!a.isFolder && !b.isFolder) || (a.isFolder && b.isFolder)) {
    return (a.displayName || "").localeCompare(b.displayName || "", undefined, {
      numeric: true,
      sensitivity: "base",
    })
  }
  return a.isFolder ? -1 : 1
}

ExternalPlugin.Explorer({ sortFn: explorerSortFn })

// Lets the GM build override baseUrl (gm.eldressa.fyi) without a second
// copy of quartz.config.yaml. Unset in the player build, which uses the
// baseUrl from quartz.config.yaml as-is.
const configOverrides = process.env.QUARTZ_BASE_URL
  ? { baseUrl: process.env.QUARTZ_BASE_URL }
  : undefined

const config = await loadQuartzConfig(configOverrides)
export default config
export const layout = await loadQuartzLayout()
