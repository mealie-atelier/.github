# Brand assets

Mealie Atelier uses an editorial close crop of real pasta being made by hand. The photograph keeps the organization avatar specific to cooking and readable in GitHub's circular crop. It is an actual credited photograph, not generated imagery or an abstract letter mark.

## App icons

- `mealie-atelier.svg` is the editable crop master and uses the adjacent credited source photograph.
- `mealie-atelier.png` is the 1024 × 1024 organization-avatar master.
- `mealie-atelier-icon-192.png` and `mealie-atelier-icon-512.png` are PWA exports.
- `mealie-atelier-maskable-512.png` is a full-bleed photographic export for maskable icon contexts.
- `mealie-atelier-apple-touch-icon.png` is the 180 × 180 Apple touch icon.

## Repository previews

- `mealie-atelier-cards-social-preview.png` and `mealie-atelier-bridge-social-preview.png` are 1280 × 640 GitHub previews.
- The matching SVG files are editable source artwork, with the warm editorial palette carried across both repository previews.
- The Cards preview uses the same real pasta-making photograph as the icon, credited in `CREDITS.md`.

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
