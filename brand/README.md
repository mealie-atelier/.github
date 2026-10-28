# Brand assets

Mealie Atelier's icon family turns a real handmade-pasta photograph into three practical app marks. The shared plate, pasta and aubergine palette keep the family together; the recipe card and home connection distinguish Cards from Bridge. The artwork uses no generated food imagery or letter monogram.

## App icons

- `mealie-atelier.svg` is the editable Atelier master. `mealie-atelier.png` is its 1024 × 1024 organization-avatar export.
- `mealie-atelier-icon-192.png`, `mealie-atelier-icon-512.png`, `mealie-atelier-maskable-512.png` and `mealie-atelier-apple-touch-icon.png` are PWA and Apple exports.
- `mealie-atelier-cards-icon.svg` and `mealie-atelier-bridge-icon.svg` are the product masters. Each has 192, 512 and 1024 pixel PNG exports.
- The source photograph is `photographer-davide-ragusa-handmade-pasta.jpg`; its credit is in `CREDITS.md`.
- `mealie-atelier-apple-touch-icon.png` is the 180 × 180 Apple touch icon.

## Repository previews

- `mealie-atelier-cards-social-preview.png` and `mealie-atelier-bridge-social-preview.png` are 1280 × 640 GitHub previews.
- The matching SVG files are editable source artwork, with the warm editorial palette carried across both repository previews.
- The Cards preview pairs the real pasta-making photograph with the Cards app icon.
- The Bridge preview presents the recipe-to-kitchen pasta connection icon.

## Exporting

From this folder, regenerate all icon PNGs and social previews with `rsvg-convert`:

```sh
rsvg-convert -w 1024 -h 1024 mealie-atelier.svg > mealie-atelier.png
rsvg-convert -w 512 -h 512 mealie-atelier.svg > mealie-atelier-icon-512.png
rsvg-convert -w 192 -h 192 mealie-atelier.svg > mealie-atelier-icon-192.png
rsvg-convert -w 512 -h 512 mealie-atelier.svg > mealie-atelier-maskable-512.png
rsvg-convert -w 180 -h 180 mealie-atelier.svg > mealie-atelier-apple-touch-icon.png
for name in mealie-atelier-cards mealie-atelier-bridge; do
  rsvg-convert -w 1024 -h 1024 "$name-icon.svg" > "$name-icon-1024.png"
  rsvg-convert -w 512 -h 512 "$name-icon.svg" > "$name-icon-512.png"
  rsvg-convert -w 192 -h 192 "$name-icon.svg" > "$name-icon-192.png"
done
rsvg-convert -w 1280 -h 640 mealie-atelier-cards-social-preview.svg > mealie-atelier-cards-social-preview.png
rsvg-convert -w 1280 -h 640 mealie-atelier-bridge-social-preview.svg > mealie-atelier-bridge-social-preview.png
```
