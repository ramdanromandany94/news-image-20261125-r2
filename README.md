# The World in One Image — 25 November 2026 (round 2)

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/ramdanromandany94/news-image-20261125-r2/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/ramdanromandany94/news-image-20261125-r2/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A one-page newspaper summing up the world's news of **Wednesday, 25 November 2026**,
built for the [make.fun bounty](https://make.fun/bounty/news-image-20261125).

## The front page

- **Hero — Indonesia:** three dead as a flood traps 26 miners in an illegal gold mine
  in Bogor, West Java. Rescuers pulled three bodies from a 100-metre shaft after the
  Ciseureuh River burst into it; twenty-three men are still trapped underground.
- **United States:** a Brooklyn jury finds Huawei guilty on 10 of 12 counts — bank
  fraud, wire fraud, sanctions breaches and conspiring to steal trade secrets.
- **Ukraine:** Kyiv needs €115 billion in outside support for 2027; the EU has
  promised €90 billion, leaving a €25 billion gap.
- **Colombia / Bangladesh / North Korea:** all hostages freed in the Cartagena
  supermarket siege; garment pay rises 36% to 17,000 taka; Pyongyang expels the
  Swiss envoy within 48 hours.
- **Also today:** Anthropic slides further below its IPO price; Houthi strikes on
  Riyadh; Britain's sabotage warning; the Hodeidah strikes; the Chen Jining probe;
  eurozone inflation at 4.0%.

## How it is made

`tools/render.py` draws the page from scratch with PIL and DejaVu fonts
(1024×1024 PNG). `main.ts` copies `entry.png` to the output directory,
resolving it the way the grader runs it: `MAKEFUN_INPUT_DIR`, then
`MAKEFUN_BOT_DIR`, then this file's own directory, then the working directory.

```sh
python3 tools/render.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

New to make.fun? Start here: [make.fun](https://make.fun/r/hxd0fhbx)

## License

MIT — see [LICENSE](LICENSE).
