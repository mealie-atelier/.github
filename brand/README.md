# Brand assets

Mealie Atelier uses a compact, hand-drawn pasta-ribbon mark: one tagliatelle ribbon forms the Atelier “A”. The flat mark is designed to stay legible in GitHub's circular avatar crop, PWA icons and small in-app placements. Its restrained palette pairs aubergine, warm pasta gold and cream; no generated food imagery is used in the identity mark.

## App icons

- `mealie-atelier.svg` is the editable vector master.
- `mealie-atelier.png` is the 1024 × 1024 organization-avatar master.
- `mealie-atelier-icon-192.png` and `mealie-atelier-icon-512.png` are PWA exports.
- `mealie-atelier-maskable-512.png` is a 512 × 512 maskable export with the mark kept within the safe area.
- `mealie-atelier-apple-touch-icon.png` is the 180 × 180 Apple touch icon.

## Repository previews

- `mealie-atelier-cards-social-preview.png` and `mealie-atelier-bridge-social-preview.png` are 1280 × 640 GitHub previews.
- The matching SVG files are editable source artwork. They use the same type hierarchy and palette as the icon.
- The Cards preview uses a real pasta-making photograph credited in `CREDITS.md`.

## Exporting

From this folder, regenerate all icon PNGs and social previews with `rsvg-convert`:

```sh
rsvg-convert -w 1024 -h 1024 mealie-atelier.svg > mealie-atelier.png
rsvg-convert -w 512 -h 512 mealie-atelier.svg > mealie-atelier-icon-512.png
rsvg-convert -w 192 -h 192 mealie-atelier.svg > mealie-atelier-icon-192.png
rsvg-convert -w 512 -h 512 mealie-atelier.svg > mealie-atelier-maskable-512.png
rsvg-convert -w 180 -h 180 mealie-atelier.svg > mealie-atelier-apple-touch-icon.png
rsvg-convert -w 1280 -h 640 mealie-atelier-cards-social-preview.svg > mealie-atelier-cards-social-preview.png
rsvg-convert -w 1280 -h 640 mealie-atelier-bridge-social-preview.svg > mealie-atelier-bridge-social-preview.png
```
