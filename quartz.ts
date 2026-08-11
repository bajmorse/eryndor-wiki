import { loadQuartzConfig, loadQuartzLayout } from "./quartz/plugins/loader/config-loader"

// Lets the GM build override baseUrl (gm.eldressa.fyi) without a second
// copy of quartz.config.yaml. Unset in the player build, which uses the
// baseUrl from quartz.config.yaml as-is.
const configOverrides = process.env.QUARTZ_BASE_URL
  ? { baseUrl: process.env.QUARTZ_BASE_URL }
  : undefined

const config = await loadQuartzConfig(configOverrides)
export default config
export const layout = await loadQuartzLayout()
