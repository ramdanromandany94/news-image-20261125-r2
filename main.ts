// news-image-20261125-r2 — round 2 entry: copies the rendered newspaper image to /output/entry.png.
// Agent-authored entrypoint, written for this entry from scratch.
// The grader runs `node /bot/main.ts` with MAKEFUN_BOT_DIR=/bot and MAKEFUN_OUTPUT_DIR=/output,
// no MAKEFUN_INPUT_DIR, and a cwd that is not /bot — so resolve entry.png in this order:
//   1. MAKEFUN_INPUT_DIR  2. MAKEFUN_BOT_DIR  3. this file's own directory  4. "."
import { copyFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const here = dirname(fileURLToPath(import.meta.url));
const candidates = [process.env.MAKEFUN_INPUT_DIR, process.env.MAKEFUN_BOT_DIR, here, '.']
  .filter((d) => typeof d === 'string' && d.length > 0);
const src = candidates.map((d) => join(d, 'entry.png')).find((p) => existsSync(p));
if (!src) {
  throw new Error('entry.png not found; looked in ' + candidates.join(', '));
}
copyFileSync(src, join(outDir, 'entry.png'));
