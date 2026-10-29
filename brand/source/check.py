"""Checks for the Week Dial masters. Run after build.py and wordmark.py: venv/bin/python check.py

Optional argument: a directory of SVGs to check instead of this one. Only the per-file checks run
there; it exists to prove the checks bind against an older build (e.g. the zigzag midrib)."""
import glob
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as b  # noqa: E402

SVG_DIR = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else HERE
ALLOWED = {b.NIGHT, b.NIGHT_RIM, b.OAT, b.OAT_RIM, b.HERB, b.MINT, b.PAPRIKA, "#000000"}
PAIR = {b.OAT.upper(): b.HERB.upper(), b.NIGHT.upper(): b.MINT.upper()}
errors = []


def radius_range(path):
    # on-curve points only: cubic control points of an arc lie outside the circle by design
    rs = [math.hypot(*pts[-1]) for _, pts in path.segments if pts]
    return min(rs), max(rs)


# ---------------------------------------------------------------- geometry

# today's section has the same radii as the other six (no step forward out of the rim)
days, today, _ = b.plate_parts()
t_min, t_max = radius_range(today)
o_min, o_max = radius_range(b.section(3))
if abs(t_max - o_max) > 1e-3 or abs(t_min - o_min) > 1e-3:
    errors.append(f"today section radii {t_min:.2f}..{t_max:.2f} differ from the rim {o_min:.2f}..{o_max:.2f}")
if t_max > b.R_PLATE + 1e-3:
    errors.append("today section sticks out of the plate")

# the leaf points at the centre of today's section
leaf_axis = math.degrees(math.atan2(18 - 6, 19 - 5))
if abs(leaf_axis - b.AXIS) > 0.01:
    errors.append(f"leaf axis {leaf_axis:.1f} does not match today centre {b.AXIS:.1f}")

# mono: the original solid style. The 1024 master (used from 180 px) cuts today free from the well with
# a knocked-out line exactly as wide as a notch, so today is its own solid island; the small masters
# (16 to 179 px) have no accent at all, today stays joined to the well
empty = b.pathops.Path()  # plate only: a glyph would add islands of its own (the leaf's midrib)
big = b.mono_plate(empty, True)
small = b.mono_plate(empty, False)
_, today_s, _ = b.plate_parts()
if abs(b.inter(today_s, big).area - (today_s.area - b.inter(today_s, b.today_line()).area)) > 1e-3:
    errors.append("mono: today section is not solid apart from the accent line")
line = b.today_line()
r_lo, r_hi = radius_range(line)
if abs((r_hi - r_lo) - b.NOTCH) > 1e-3:
    errors.append(f"mono: accent line is {r_hi - r_lo:.2f} wide, the notch is {b.NOTCH}")
outer_cw = b.circle(b.R_PLATE).clockwise
islands = [c for c in big.contours if c.clockwise == outer_cw]
if len(islands) != 2:
    errors.append(f"mono 1024: expected the plate and today as two solid islands, got {len(islands)}")
# the accent line ends flush on the far edge of each neighbouring notch: the notch turns into the line
# with one clean corner. Probe just inside and just outside that edge line, in the inner half of the
# accent line (below the well rim, where only the line cuts): inside must be cut, outside solid. A line
# ending on the notch's centre line leaves a stair step and fails the inside probe.
def _probe(theta, offset, r, e=0.02):
    x, y = b.pt(r, theta)
    nx, ny = math.cos(math.radians(theta)), math.sin(math.radians(theta))
    x, y = x + nx * offset, y + ny * offset
    return b.inter(big, b.rrect(x - e, y - e, 2 * e, 2 * e, 0)).area


h, r_probe = b.NOTCH / 2, b.R_WELL - b.NOTCH / 4
t1 = b.AXIS - b.SEG / 2
for theta, far in ((t1, -h), (t1 + b.SEG, h)):
    inward = -0.05 if far > 0 else 0.05
    if _probe(theta, far + inward, r_probe) > 1e-6:
        errors.append(f"mono: accent line stops short of the notch edge at {theta:.1f} deg (stair step)")
    if _probe(theta, far - inward, r_probe) < (0.04 ** 2) - 1e-6:
        errors.append(f"mono: accent line overshoots the notch edge at {theta:.1f} deg")
if b.inter(small, line).area < 0.9 * line.area:
    errors.append("mono small: carries the today accent line (only from 180 px)")
if len([c for c in small.contours if c.clockwise == outer_cw]) != 1:
    errors.append("mono small: today is not joined to the plate")
for k in range(7):  # seven sections, six notches plus the two at today: every section stays solid
    sec = b.section(k, gap=b.NOTCH_SMALL)
    if b.inter(sec, small).area < sec.area - 1e-3:
        errors.append(f"mono small: day section {k} is not solid")
if b.NOTCH_SMALL * 48 / 1024 * 32 < 1.0:
    errors.append("mono small: notch narrower than a pixel at 32 px")

# mono 16: the plain plate with the glyph knocked out, nothing else (no notch, no channel, no accent)
for v in b.GLYPHS:
    m = b.minus(b.circle(b.MONO16_R, 8, 8), b.glyph16(v))
    if abs(m.area - (b.circle(b.MONO16_R, 8, 8).area - b.inter(b.glyph16(v), b.circle(b.MONO16_R, 8, 8)).area)) > 1e-3:
        errors.append(f"mono 16 {v}: plate has cuts besides the glyph")

# colour 16: the bridge keeps a cream gap to today (its deck once ran into the paprika section)
_, today16 = b.parts16()
grown = b.transform(b.section(0, r_out=7, r_in=4.25 - 0.6, gap=0.9 - 1.2, rho=0.0001), 1, 8, 8)
if b.inter(b.glyph16("bridge"), grown).area > 1e-4:
    errors.append("colour 16 bridge: glyph closer than 0.6 px to today")


def off_grid(path, label):
    """Every straight horizontal or vertical edge of a pixel-tuned glyph lies on a whole pixel."""
    prev = None
    for verb, pts in path.segments:
        if verb == "lineTo" and prev:
            (x, y), (px, py) = pts[-1], prev
            if abs(x - px) < 1e-6 and abs(x - round(x)) > 1e-6:
                errors.append(f"{label}: vertical edge at x={x:.3f}, off the pixel grid")
            if abs(y - py) < 1e-6 and abs(y - round(y)) > 1e-6:
                errors.append(f"{label}: horizontal edge at y={y:.3f}, off the pixel grid")
        prev = pts[-1] if pts else prev


# simplified bridge (16 and 32 px): one deck bar over one arch between two piers. Deck at least 2 px at 32
# and 1 px at 16, piers at least a pixel, and the arch void reaches the deck under the crown
for key, (x0, x1, y0, dh, inset, pw, foot) in b.BRIDGE_SIMPLE.items():
    n = key[0]
    label = f"bridge {n} px {key[1]}"
    gl = b.bridge_simple(key)
    off_grid(gl, label)
    if dh < (2 if n >= 32 else 1) or pw < 1:
        errors.append(f"{label}: deck {dh} px or pier {pw} px too thin")
    holes = [c for c in gl.contours if c.clockwise != b.poly([(0, 0), (1, 0), (1, 1)]).clockwise]
    crown = b.poly([((x0 + x1) / 2 - 0.5, y0 + dh), ((x0 + x1) / 2 + 0.5, y0 + dh), ((x0 + x1) / 2 + 0.5, y0 + dh + 1), ((x0 + x1) / 2 - 0.5, y0 + dh + 1)])
    if b.inter(gl, crown).area > 1e-4:
        errors.append(f"{label}: no arch void under the deck at the crown")
    if b.bridge_simple(key).area <= 0 or len(list(gl.contours)) != 1:
        errors.append(f"{label}: glyph is not one piece (deck, piers and arch must hold together)")
    x_mid = (x0 + x1) / 2
    void_w = (x1 - inset - pw) - (x0 + inset + pw)
    if void_w < 4:
        errors.append(f"{label}: arch span {void_w} px is too narrow to read as an arch")
if b.glyph16("bridge").area != b.bridge_simple((16, "tile")).area:
    errors.append("bridge 16: the 16 px masters do not use the simplified bridge")

# three-arch bridge at 48 px: whole-pixel piers and deck of at least a pixel
for key in b.BRIDGE_PX:
    gl = b.bridge_px(key)
    off_grid(gl, f"bridge {key[0]} px {key[1]}")
    (x0, y0, x1, y1), _, (cx, cy, r), offs, scy, sr = b.BRIDGE_PX[key]
    edges = sorted([x0, x1, cx - r, cx + r] + [cx + o + k * sr for o in offs for k in (-1, 1)])
    piers = [edges[i + 1] - edges[i] for i in range(0, len(edges), 2)]
    if min(piers) < 1 or cy - r - y0 < 1:
        errors.append(f"bridge {key}: pier or deck thinner than a pixel ({piers}, deck {cy - r - y0})")

# cards and web app pixel glyphs: on the grid, centred on the plate, gaps and frames at least a pixel
for key in b.CARDS_PX:
    n = key[0]
    x0, a, g, _ = b.CARDS_PX[key]
    off_grid(b.cards_px(key), f"cards {key}")
    if g < 1 or abs(x0 + a + g / 2 - n / 2) > 1e-6:
        errors.append(f"cards {key}: gap under a pixel or grid off centre")
for key in b.WEBAPP_PX:
    n = key[0]
    x0, y0, x1, y1, t, bar, _ = b.WEBAPP_PX[key]
    off_grid(b.webapp_px(key), f"webapp {key}")
    if t < 1 or abs((x0 + x1) / 2 - n / 2) > 1e-6 or abs((y0 + y1) / 2 - n / 2) > 1e-6:
        errors.append(f"webapp {key}: frame under a pixel or window off centre")

# every pixel-tuned glyph has its master file
for v in b.GLYPHS:
    for n in (32, 48):
        if b.px_glyph(v, n) is not None and not os.path.exists(os.path.join(HERE, f"{v}-{n}.svg")):
            errors.append(f"missing {v}-{n}.svg")
        if b.px_glyph(v, n, "mono") is not None and not os.path.exists(os.path.join(HERE, f"{v}-mono-{n}.svg")):
            errors.append(f"missing {v}-mono-{n}.svg")

# ---------------------------------------------------------------- per file

NUM = re.compile(r"-?\d*\.?\d+(?:e-?\d+)?")
CMD = re.compile(r"([MLHVCSQTZmlhvcsqtz])([^MLHVCSQTZmlhvcsqtz]*)")
SHORT = 0.02  # a straight segment shorter than 2 % of the viewBox width is "tiny"
# measured 2026-10-29: clean masters peak at a run of 2 and 16 in total (divider notch crossings, font
# outlines); the old zigzag midrib had a run of 71 and 103 in total
MAX_SHORT_RUN, MAX_SHORT_TOTAL = 6, 40


def short_lines(d, vb):
    """(longest run of consecutive tiny straight segments, total tiny straight segments) of an absolute
    path. A curve flattened into a polyline shows up as a long run and leaves seam hatching."""
    run = best = total = 0
    cur = start = (0.0, 0.0)
    for cmd, args in CMD.findall(d):
        v = [float(x) for x in NUM.findall(args)]
        if cmd == "M":
            cur = start = (v[0], v[1])
            pairs = list(zip(v[2::2], v[3::2]))  # implicit lineTos
        elif cmd == "L":
            pairs = list(zip(v[0::2], v[1::2]))
        elif cmd in "Zz":
            pairs = [start]
        else:
            run = 0
            if len(v) >= 2:
                cur = (v[-2], v[-1])
            continue
        for p in pairs:
            if 0 < math.hypot(p[0] - cur[0], p[1] - cur[1]) < SHORT * vb:
                run += 1
                total += 1
                best = max(best, run)
            else:
                run = 0
            cur = p
    return best, total


svgs = sorted(glob.glob(os.path.join(SVG_DIR, "*.svg")))
if not svgs:
    errors.append(f"no SVG files in {SVG_DIR}")
for f in svgs:
    name = os.path.basename(f)
    s = open(f).read()
    if re.search(r"[Aa]\s*0[ ,]+0[ ,]", s):
        errors.append(f"{name}: zero radius arc")
    if re.search(r"stroke=|<mask|clip-path|<text|<image", s):
        errors.append(f"{name}: not fill-only")
    for c in re.findall(r'fill="(#[0-9A-Fa-f]{6})"', s):
        if c.upper() not in {a.upper() for a in ALLOWED}:
            errors.append(f"{name}: colour {c} outside the palette")
    paths = re.findall(r' d="([^"]*)"', s)
    if re.search(r"[mlhvcsqtz]", "".join(paths)):
        errors.append(f"{name}: relative path commands (the segment check expects absolute ones)")
    vb = float(re.search(r'viewBox="[-\d.]+ [-\d.]+ ([\d.]+)', s).group(1))
    for i, d in enumerate(paths):
        run, total = short_lines(d, vb)
        if run > MAX_SHORT_RUN or total > MAX_SHORT_TOTAL:
            errors.append(f"{name}: path {i} has {total} tiny straight segments (run of {run}), a flattened curve")

    # colour roles: a mono master is one black path; a colour master pairs HERB with OAT, MINT with NIGHT
    if 'class="mono"' in s:
        if re.search(r'class="(plate|glyph|today)"', s) or b.PAPRIKA.upper() in s.upper():
            errors.append(f"{name}: mono master mixes in colour paths")
        continue
    plates = {c.upper() for c in re.findall(r'class="plate" fill="(#[0-9A-Fa-f]{6})"', s)}
    glyphs = {c.upper() for c in re.findall(r'class="glyph" fill="(#[0-9A-Fa-f]{6})"', s)}
    if len(plates) != 1 or len(glyphs) != 1:
        errors.append(f"{name}: expected exactly one plate and one glyph colour, got {plates} / {glyphs}")
        continue
    p, g = plates.pop(), glyphs.pop()
    if PAIR.get(p) != g:
        errors.append(f"{name}: glyph {g} on plate {p} (rule: HERB on OAT, MINT on NIGHT)")
    if 'class="today"' not in s:
        errors.append(f"{name}: colour master without the paprika today section")

# ---------------------------------------------------------------- completeness

if SVG_DIR == HERE:
    SUFFIXES = ("", "-light", "-16", "-mono-16", "-mono", "-mono-small", "-maskable", "-square", "-transparent", "-transparent-light")
    for v in b.GLYPHS:
        for suffix in SUFFIXES:
            if not os.path.exists(os.path.join(HERE, f"{v}{suffix}.svg")):
                errors.append(f"missing {v}{suffix}.svg")
        stem = "lockup" if v == "mark" else f"lockup-{v}"
        for suffix in ("", "-light", "-transparent", "-transparent-light"):
            if not os.path.exists(os.path.join(HERE, f"{stem}{suffix}.svg")):
                errors.append(f"missing {stem}{suffix}.svg")

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"ok: {len(svgs)} SVG masters")
