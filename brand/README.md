# Mealie Atelier brand: Week Dial

A cream plate seen from above. Its rim is notched into seven day sections, one of them (today) in
paprika. On the plate sits a glyph: the herb leaf for Mealie Atelier itself, a card grid for Cards, a
three-arch bridge for Bridge, a browser window for the web app.

This folder is the single source of truth for the brand. Every file is generated; never edit an SVG or PNG by hand.

| Folder | Content |
|---|---|
| `svg/` | vector masters: marks, mono, transparent, maskable, pixel-tuned small sizes, lockups |
| `png/` | raster and icon deliverables: favicons, apple-touch, web app icons, Home Assistant brand set, avatar |
| `social/` | 1280 × 640 GitHub social previews (PNG and JPG under 1 MB) for the organization, Cards and Bridge |
| `source/` | generator, font and its license |

All file names start with `mealie-atelier-`. Families: no infix is the organization mark (herb leaf);
`cards-`, `bridge-` and `webapp-` follow the prefix (for example `mealie-atelier-cards-mark.svg`).

## Palette

| Token | Hex | Role |
|---|---|---|
| Night | `#14201A` | tile background, dark plate, wordmark on light grounds |
| Night rim | `#2B3B31` | divider line on the night plate |
| Oat | `#F2E9D8` | cream plate, light tile, wordmark on dark grounds |
| Oat rim | `#DCCDB0` | divider line on the cream plate |
| Herb | `#3E6B48` | glyph on the cream plate, product name on light grounds |
| Mint | `#9DCBB2` | glyph on the night plate, product name on dark grounds (the `--demo-brand` color of the UI) |
| Paprika | `#B8532E` | today's section, in every color version |

**Glyph color follows the plate, never the background:** Herb on the Oat plate, Mint on the Night plate.
No file mixes them; `check.py` fails the build if one does. Mono versions use one color only (black in the
masters; recolor freely, e.g. white on dark).

## Which file for which use

File names below are for the main mark; family files carry `cards-`, `bridge-` or `webapp-` after `mealie-atelier-`.
SVG files are in `svg/`, PNG and ICO files in `png/`.

| Use | File |
|---|---|
| App icon, store artwork, README | `mealie-atelier-mark.svg`, `mealie-atelier-icon-512.png` (rounded Night tile, cream plate) |
| App icon in a light context | `mealie-atelier-mark-light.svg` (Oat tile, Night plate) |
| Plate without tile on dark or mid-tone grounds | `mealie-atelier-mark-transparent.svg`, `mealie-atelier-ha-dark-icon.png` |
| Plate without tile on light grounds | `mealie-atelier-mark-light-transparent.svg`, `mealie-atelier-ha-icon.png` |
| Home Assistant brands (integration or plugin) | `ha-icon`, `ha-icon@2x`, `ha-dark-icon`, `ha-dark-icon@2x`, `ha-logo`, `ha-logo@2x`, `ha-dark-logo`, `ha-dark-logo@2x` (`.png`). In the brands repository drop `mealie-atelier-<family>-ha-` and use `icon.png`, `dark_icon.png`, `logo.png`, `dark_logo.png` |
| Browser tab | `mealie-atelier-favicon.svg` (pixel-tuned 16 px master), `mealie-atelier-favicon-16.png`, `mealie-atelier-favicon-32.png`, `mealie-atelier-favicon.ico` (16/32/48) |
| iOS home screen | `mealie-atelier-apple-touch-icon.png` (180, opaque, full bleed; iOS rounds the corners) |
| Web app manifest | `mealie-atelier-icon-192.png`, `mealie-atelier-icon-512.png` (purpose `any`), `mealie-atelier-icon-maskable-512.png` (purpose `maskable`) |
| GitHub org avatar | `mealie-atelier-avatar-500.png` (full bleed, survives the circular crop) |
| Repository social preview | `social/mealie-atelier-social-preview.png`, `social/mealie-atelier-cards-social-preview.png`, `social/mealie-atelier-bridge-social-preview.png` (and `.jpg`) |
| One color (print, engraving, embossing), 180 px and up | `mealie-atelier-mark-mono.svg` (with today's accent line) |
| One color below 180 px | `mealie-atelier-mark-mono-small.svg`; at exactly 32 or 48 px the pixel masters `mealie-atelier-<family>-mark-mono-32.svg` / `-mark-mono-48.svg` where a family has them (Cards, Bridge, web app); at 16 px and for the Safari pinned tab `mealie-atelier-mark-mono-16.svg` |
| Wordmark lockup | `mealie-atelier-lockup-dark.svg` (on Night), `mealie-atelier-lockup-light.svg` (on Oat), `mealie-atelier-lockup-dark-transparent.svg` (dark grounds), `mealie-atelier-lockup-light-transparent.svg` (light grounds) |

The mono masters use the solid style: one solid disc, the seven sections separated by notch cuts, the
glyph knocked out. From 180 px up (`mealie-atelier-mark-mono.svg`) today carries one subtle accent: a thin knocked-out line,
exactly as wide as a notch, between today's section and the well, so today reads as its own solid block.
Below 180 px there is no accent at all; a cut that thin would blur into a crack or read as a bite. The
small master (`mealie-atelier-mark-mono-small.svg`) widens the notch slightly so it stays a whole pixel at 32 px, and the
16 px master drops the notches and keeps only the disc with the glyph knocked out.

Small sizes are drawn on the pixel grid where scaling would blur:

- Bridge at 16 and 32 px (color, mono, favicons, ico): one full-width deck bar over one wide stepped
  arch between two solid piers. Three arches read as a comb at 32 px and a single arch in a block as a
  tunnel at 16 px. From 48 px the three-arch viaduct returns (`mealie-atelier-bridge-mark-48.svg`,
  `mealie-atelier-bridge-mark-mono-48.svg` with whole-pixel piers, `mealie-atelier-bridge-mark.svg` above).
- Cards and web app at 32 and 48 px (`mealie-atelier-<family>-mark-32.svg`, `-mark-48.svg`, `-mark-mono-32.svg`, `-mark-mono-48.svg`): card gaps
  and window frames on whole pixels, so they stay crisp instead of a gray smear.

## Clear space

- Plate on its own: keep free space of at least half the plate radius (a quarter of the plate diameter)
  on every side. The rounded tile already contains its clear space; keep at least an eighth of the tile
  width free around it.
- Lockup: at least the plate radius on every side of the lockup's bounding box. Do not move the wordmark
  closer to the plate than the generated lockup does.

## Minimum size

| Version | Minimum |
|---|---|
| Color tile or plate (`mealie-atelier-mark.svg`, `mealie-atelier-mark-transparent.svg`, `mealie-atelier-mark-light-transparent.svg`) | 32 px (below that use the 16 px master) |
| 16 px color master (`mealie-atelier-mark-16.svg`, `mealie-atelier-favicon.svg`) | 16 px, made for 16 to 31 px |
| Pixel tiles (`mealie-atelier-<family>-mark-32.svg`, `-mark-48.svg`) | exactly 32 and 48 px; from 49 px use the full master |
| Mono with accent (`mealie-atelier-mark-mono.svg`) | 180 px |
| Mono small (`mealie-atelier-mark-mono-small.svg`) | 32 px, made for 32 to 179 px (pixel masters at exactly 32 and 48 px where they exist) |
| Mono 16 px (`mealie-atelier-mark-mono-16.svg`) | 16 px, made for 16 to 31 px |
| Lockup | 24 px plate height on screen, 10 mm in print |

## Do

- Use the generated files as they are; pick the version by background (table above).
- Keep today's section at the upper right, centered on the leaf's axis.
- Keep the glyph color paired to the plate color (Herb on Oat, Mint on Night).
- Use the mono master for single-color reproduction and recolor it as a whole.

## Don't

- Don't recolor parts of the mark, swap Herb and Mint, or put a Herb glyph on the Night plate.
- Don't rotate the plate, move today to another section or add a second accent section.
- Don't add strokes, shadows, gradients, outlines or a needle; the mark is flat fills only.
- Don't place the cream plate (`mealie-atelier-mark-transparent.svg`) on white or cream; use the Night plate there.
- Don't scale the full master below 32 px; use the 16 px master. Don't use the mono master with the
  accent line below 180 px; use `mealie-atelier-mark-mono-small.svg` or the pixel masters.
- Don't re-set the wordmark in another font or weight; it is Bricolage Grotesque (SIL OFL 1.1), outlined.
- Don't crop the maskable or avatar files to anything smaller than the 80 % safe circle.

## Rebuild

Everything under `svg/`, `png/` and `social/` is generated from `source/`. Requirements: macOS or Linux with
Python 3.14 and `uv`, the Python packages `skia-pathops`, `fonttools` and `uharfbuzz` (installed into a local
`source/venv` by `make.sh`), Google Chrome or Chromium (headless renders) and ImageMagick 7 (`magick`). The
scripts look for the browser in this order: the `CHROME` environment variable, the macOS Google Chrome app,
then `google-chrome`, `chromium` or `chromium-browser` on `PATH`. If none is found they stop with a message.
Example: `CHROME=/usr/bin/chromium ./make.sh`.

```sh
cd brand/source
./make.sh                          # masters, checks, renders, rollout set in source/out/
venv/bin/python publish.py         # copy into ../svg and ../png under the mealie-atelier- names
./social.sh                        # 1280 × 640 social previews into ../social
```

`check.py` and `check_png.py` fail the build if glyph and plate colors are mixed or a small size renders wrongly.
`make.sh` also writes working files (`venv/`, `png/`, `out/`, `tmp/`, generated `*.svg`) inside `source/`;
they are git-ignored. Edit the generator (`build.py` for marks, `wordmark.py` for lockups), never the output.

The wordmark font is Bricolage Grotesque, licensed under the SIL Open Font License 1.1 (`source/font/OFL.txt`);
see `CREDITS.md`.
