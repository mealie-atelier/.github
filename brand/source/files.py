"""Write out/FILES.md: every file in out/ with its pixel size, byte size and intended use. Called by make.sh."""
import os
import re
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FAMILY = {"": "Mealie Atelier (main mark)", "cards-": "Cards", "bridge-": "Bridge", "webapp-": "web app"}

USE = [
    (r"icon\.png", "Home Assistant brand `icon.png` (light UI): night plate, trimmed transparent square"),
    (r"icon@2x\.png", "Home Assistant brand `icon@2x.png` (light UI, hDPI)"),
    (r"dark_icon\.png", "Home Assistant brand `dark_icon.png` (dark UI): cream plate, trimmed transparent square"),
    (r"dark_icon@2x\.png", "Home Assistant brand `dark_icon@2x.png` (dark UI, hDPI)"),
    (r"logo\.png", "Home Assistant brand `logo.png` (light UI): lockup, transparent, shortest side 128"),
    (r"logo@2x\.png", "Home Assistant brand `logo@2x.png` (light UI, hDPI), shortest side 256"),
    (r"dark_logo\.png", "Home Assistant brand `dark_logo.png` (dark UI): lockup, transparent, shortest side 128"),
    (r"dark_logo@2x\.png", "Home Assistant brand `dark_logo@2x.png` (dark UI, hDPI), shortest side 256"),
    (r"favicon\.svg", "browser favicon, scalable (`<link rel=icon type=image/svg+xml>`), pixel-tuned 16 px master"),
    (r"favicon-16\.png", "browser favicon 16 px fallback"),
    (r"favicon-32\.png", "browser favicon 32 px fallback"),
    (r"favicon\.ico", "legacy favicon, contains 16, 32 and 48 px"),
    (r"apple-touch-icon\.png", "iOS home screen (`apple-touch-icon`), opaque full-bleed, iOS rounds the corners"),
    (r"icon-192\.png", "web app manifest icon, purpose `any`, rounded tile with transparent corners"),
    (r"icon-512\.png", "web app manifest icon, purpose `any`, also store/listing artwork"),
    (r"icon-maskable-512\.png", "web app manifest icon, purpose `maskable`: opaque, plate inside the 80 % safe circle"),
    (r"avatar-500\.png", "GitHub org avatar (`mealie-atelier`), full-bleed so the circular crop keeps the plate whole"),
    (r"size-sheet\.png", "review sheet: mark, mono and family at 16/32/48/180/512 on cream, white, black and dark"),
    (r"overview-sheet\.png", "review sheet: maskable and GitHub crops, bare plates, lockups"),
]


def dims(path):
    with open(path, "rb") as fh:
        head = fh.read(64)
    if head[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", head[16:24])
        return f"{w}×{h}"
    if path.endswith(".ico"):
        n = struct.unpack("<H", head[4:6])[0]
        sizes = [(head[6 + 16 * i] or 256) for i in range(n)]
        return " + ".join(f"{s}×{s}" for s in sizes)
    if path.endswith(".svg"):
        m = re.search(r'viewBox="[-\d.]+ [-\d.]+ ([\d.]+) ([\d.]+)"', open(path).read())
        return f"vector, viewBox {float(m.group(1)):g}×{float(m.group(2)):g}"
    return ""


def use_of(name):
    for prefix, fam in sorted(FAMILY.items(), key=lambda kv: -len(kv[0])):
        if prefix and not name.startswith(prefix):
            continue
        rest = name[len(prefix):]
        for pat, text in USE:
            if re.fullmatch(pat, rest):
                return fam, text
    return "", ""


SVG_USE = {
    "": "app tile on night (default app icon master)",
    "-light": "app tile on cream, for light contexts",
    "-16": "16 px colour master, drawn on the pixel grid",
    "-32": "32 px app tile, glyph redrawn on the pixel grid (favicon-32, ico)",
    "-48": "48 px app tile, glyph redrawn on the pixel grid (ico)",
    "-mono": "single-colour master from 180 px: solid plate, notches, today cut free by a thin line; recolour freely",
    "-mono-small": "single-colour master for 49 to 179 px (and 32 or 48 px where no pixel master exists): solid plate, no today accent",
    "-mono-32": "single-colour 32 px master, glyph redrawn on the pixel grid, no today accent",
    "-mono-48": "single-colour 48 px master, glyph redrawn on the pixel grid, no today accent",
    "-mono-16": "single-colour 16 px master (solid plate, glyph knocked out), also the Safari pinned-tab mask icon",
    "-maskable": "full-bleed square, plate in the 80 % safe circle (maskable, avatars)",
    "-square": "full-bleed square with tile proportions (apple-touch-icon)",
    "-transparent": "plate without tile, cream plate: for dark and mid-tone backgrounds",
    "-transparent-light": "plate without tile, night plate: for light backgrounds",
}


def svg_use(name):
    stem = name[:-4]
    if stem.startswith("lockup"):
        light = "light backgrounds" if stem.endswith("-light") else "dark backgrounds"
        kind = "transparent lockup" if "-transparent" in stem else "lockup on its own background"
        return f"{kind}, for {light}"
    for v in ("mark", "cards", "bridge", "webapp"):
        if stem == v or stem.startswith(v + "-"):
            return SVG_USE.get(stem[len(v):], "")
    return ""


def kb(path):
    n = os.path.getsize(path)
    return f"{n / 1024:.1f} KB" if n >= 1024 else f"{n} B"


rows = []
for name in sorted(os.listdir(OUT)):
    p = os.path.join(OUT, name)
    if os.path.isdir(p) or name == "FILES.md":
        continue
    fam, text = use_of(name)
    if not text:
        raise SystemExit(f"files.py: no intended use known for out/{name}")
    rows.append((fam or "all", name, dims(p), kb(p), text))

svg_rows = []
for name in sorted(os.listdir(os.path.join(OUT, "svg"))):
    text = svg_use(name)
    if not text:
        raise SystemExit(f"files.py: no intended use known for out/svg/{name}")
    p = os.path.join(OUT, "svg", name)
    svg_rows.append((name, dims(p), kb(p), text))

lines = [
    "# Week Dial · files",
    "",
    "Generated by `make.sh` (do not edit by hand; rebuild instead). Colours, clear space and rules: `../README.md`.",
    "Family prefixes: none = Mealie Atelier main mark, `cards-`, `bridge-`, `webapp-`. For the Home Assistant",
    "brands repository, copy a family's eight brand files into the domain folder and drop the prefix.",
    "",
    "## Raster and icon files (`out/`)",
    "",
    "| Family | File | Pixels | Bytes | Use |",
    "|---|---|---|---|---|",
]
lines += [f"| {f} | `{n}` | {d} | {k} | {u} |" for f, n, d, k, u in rows]
lines += [
    "",
    "## Vector masters (`out/svg/`)",
    "",
    "| File | Size | Bytes | Use |",
    "|---|---|---|---|",
]
lines += [f"| `{n}` | {d} | {k} | {u} |" for n, d, k, u in svg_rows]
with open(os.path.join(OUT, "FILES.md"), "w") as fh:
    fh.write("\n".join(lines) + "\n")
