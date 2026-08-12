#!/usr/bin/env node
// Assembles the content tree the GM Quartz build reads from: every top-level
// entry of content/ plus every top-level entry of gm/, linked side by side
// via symlinks (falling back to a copy if symlinks aren't available). This
// puts GM-only sections (e.g. gm/Party Info, gm/Session Info, gm/Gamemaster
// Info) at the same sidebar level as content/'s World Info — see the
// Explorer sortFn override in quartz.ts for the resulting nav order. The
// player build never runs this script — it points Quartz straight at
// content/, so gm/ is physically absent from anything the player build
// touches.
import { existsSync, mkdirSync, readdirSync, rmSync, symlinkSync, statSync, cpSync } from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const repoRoot = path.resolve(__dirname, "..")
const contentDir = path.join(repoRoot, "content")
const gmDir = path.join(repoRoot, "gm")
const outDir = process.argv[2] ? path.resolve(process.argv[2]) : path.join(repoRoot, ".gm-build", "content")

function link(target, dest) {
  try {
    const isDir = statSync(target).isDirectory()
    symlinkSync(target, dest, isDir ? "junction" : "file")
  } catch {
    // Unprivileged Windows can't create symlinks; copy instead.
    cpSync(target, dest, { recursive: true })
  }
}

rmSync(outDir, { recursive: true, force: true })
mkdirSync(outDir, { recursive: true })

for (const entry of readdirSync(contentDir)) {
  link(path.join(contentDir, entry), path.join(outDir, entry))
}

if (existsSync(gmDir)) {
  for (const entry of readdirSync(gmDir)) {
    link(path.join(gmDir, entry), path.join(outDir, entry))
  }
}

console.log(`Prepared GM content at ${outDir}`)
