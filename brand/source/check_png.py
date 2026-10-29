"""Pixel checks on the 16 px renders. Run after the renders: venv/bin/python check_png.py [png dir]

The vector checks in check.py prove the geometry; these prove what Chrome actually draws at 1x:
- mono 16: the plate is solid wherever it has no glyph (no crack, no bite: every pixel fully inside the
  plate and clear of the glyph is opaque), and every pixel mostly covered by the glyph shows through.
- bridge 16 and 32 (colour): the deck row is solid Herb from end to end, the crown pixel under it is
  cream (arch void), and no Herb pixel touches a paprika pixel at 16 px."""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as b  # noqa: E402

PNG = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "png")
LIGHT = 200  # a pixel lighter than this lets a hole show through
SOLID = 240
errors = []


def pixels(path):
    out = subprocess.run(["magick", path, "-depth", "8", "txt:-"], capture_output=True, text=True, check=True).stdout
    px = {}
    for line in out.splitlines()[1:]:
        pos, rest = line.split(":", 1)
        x, y = map(int, pos.split(","))
        vals = [int(v) for v in rest.split("(")[1].split(")")[0].split(",")]  # 0..255 with -depth 8
        if len(vals) == 2:  # graya
            vals = [vals[0]] * 3 + [vals[1]]
        px[(x, y)] = tuple(vals) if len(vals) == 4 else tuple(vals) + (255,)
    return px


def coverage(path, x, y):
    return b.inter(path, b.rrect(x, y, 1, 1, 0.0001)).area


disc = b.circle(b.MONO16_R, 8, 8)
for v in b.GLYPHS:
    px = pixels(os.path.join(PNG, f"{v}-mono-16.png"))
    glyph = b.glyph16(v)
    for (x, y), c in sorted(px.items()):
        g = coverage(glyph, x, y)
        if coverage(disc, x, y) > 0.999 and g < 1e-6 and c[3] < SOLID:
            errors.append(f"{v}-mono-16.png: crack in the plate at {x},{y} (alpha {c[3]})")
            break
        if g > 0.75 and c[3] >= LIGHT:
            errors.append(f"{v}-mono-16.png: glyph pixel {x},{y} filled in (alpha {c[3]})")
            break

px = pixels(os.path.join(PNG, "bridge-16.png"))


def near(c, ref, tol=60):
    return sum(abs(c[i] - ref[i]) for i in range(3)) < tol and c[3] > 200


herb = tuple(int(b.HERB[i : i + 2], 16) for i in (1, 3, 5))
pap = tuple(int(b.PAPRIKA[i : i + 2], 16) for i in (1, 3, 5))
for (x, y), c in px.items():
    if near(c, herb) and any(near(px.get((x + dx, y + dy), (0, 0, 0, 0)), pap) for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
        errors.append(f"bridge-16.png: glyph pixel {x},{y} touches today")
        break

for n in (16, 32):
    px = pixels(os.path.join(PNG, f"bridge-{n}.png"))
    x0, x1, y0, dh, *_ = b.BRIDGE_SIMPLE[(n, "tile")]
    for x in range(x0, x1):
        if not near(px[(x, y0)], herb, 40):
            errors.append(f"bridge-{n}.png: deck pixel {x},{y0} is not solid Herb {px[(x, y0)]}")
            break
    crown = px[((x0 + x1) // 2, y0 + dh)]
    if near(crown, herb, 200):
        errors.append(f"bridge-{n}.png: no arch void under the deck at the crown")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print("check_png: ok")
