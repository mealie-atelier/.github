# Brand assets

Mealie Atelier uses a warm editorial identity built around its original pasta-and-tomato photograph. Product graphics use square, full-bleed compositions and crisp, straight edges. Cards and Bridge share the same food photography and palette while their names and simple marks keep the products distinct. GitHub applies its own circular crop to the organization avatar.

## App icons

- `mealie-atelier.svg` is the standalone, square organization-avatar master; `mealie-atelier.png` is its 1024 × 1024 export and `mealie-atelier.jpg` is the lightweight upload-ready GitHub avatar.
- `mealie-atelier-icon-192.png`, `mealie-atelier-icon-512.png`, `mealie-atelier-maskable-512.png` and `mealie-atelier-apple-touch-icon.png` are photo-only PWA and Apple exports.
- `mealie-atelier-cards-icon.svg` and `mealie-atelier-bridge-icon.svg` are the product masters. Each has 192, 512 and 1024 pixel PNG exports.
- Each SVG is self-contained and embeds the source photo. This keeps previews and raster exports reliable in tools that do not resolve relative image paths.
- The original source photograph remains in `pasta-with-tomatoes.jpg`; its origin is documented in `CREDITS.md`.

## Repository previews

- `mealie-atelier-cards-social-preview.png` and `mealie-atelier-bridge-social-preview.png` are 1280 × 640 masters; their matching `.jpg` exports are optimized for GitHub uploads under its 1 MB limit.
- The matching SVG files are editable, self-contained source artwork.
- Both previews use editorial two-column layouts with square photo edges, strong type, and a single gold divider. There are no floating icon tiles, rounded photo frames, or capsule labels.

## Exporting

On macOS, use the built-in `sips` tool from this directory to regenerate the PNGs from the SVG masters:

```sh
sips -s format png -z 1024 1024 mealie-atelier.svg --out mealie-atelier.png
sips -s format jpeg -s formatOptions 86 mealie-atelier.png --out mealie-atelier.jpg
sips -s format png -z 192 192 mealie-atelier.svg --out mealie-atelier-icon-192.png
sips -s format png -z 512 512 mealie-atelier.svg --out mealie-atelier-icon-512.png
sips -s format png -z 512 512 mealie-atelier.svg --out mealie-atelier-maskable-512.png
sips -s format png -z 180 180 mealie-atelier.svg --out mealie-atelier-apple-touch-icon.png
for name in mealie-atelier-cards mealie-atelier-bridge; do
  for size in 192 512 1024; do
    sips -s format png -z "$size" "$size" "$name-icon.svg" --out "$name-icon-$size.png"
  done
done
sips -s format png mealie-atelier-cards-social-preview.svg --out mealie-atelier-cards-social-preview.png
sips -s format jpeg -s formatOptions 86 mealie-atelier-cards-social-preview.png --out mealie-atelier-cards-social-preview.jpg
sips -s format png mealie-atelier-bridge-social-preview.svg --out mealie-atelier-bridge-social-preview.png
sips -s format jpeg -s formatOptions 86 mealie-atelier-bridge-social-preview.png --out mealie-atelier-bridge-social-preview.jpg
```
