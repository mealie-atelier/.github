"""Generate the Week Dial SVG masters ("week plate").

The mark is a plate seen from above. Its rim is notched into seven day sections, one of them (today)
in paprika. On the plate sits a glyph: the leaf from the product UI (.demo-brand-mark) for the main mark,
a card grid, a three-arch bridge or a browser window for the family. There is no needle and no gauge.

Geometry lives on a unit grid with the plate radius 10, scaled into a 1024 viewBox. Angles run clockwise
from 12 o'clock. All shapes are filled outlines combined with skia-pathops, so every master is fill-only
(no strokes, no masks) and the mono version is a true knockout.
"""
import math
import os

import pathops

HERE = os.path.dirname(os.path.abspath(__file__))

NIGHT = "#14201A"
NIGHT_RIM = "#2B3B31"  # divider line on the dark plate
OAT = "#F2E9D8"
OAT_RIM = "#DCCDB0"  # divider line on the cream plate
HERB = "#3E6B48"  # glyph on the cream plate
MINT = "#9DCBB2"  # glyph on the dark plate, the --demo-brand colour of the product UI
PAPRIKA = "#B8532E"  # today

R_PLATE, R_WELL, NOTCH, FILLET, LINE = 10.0, 7.6, 0.6, 0.3, 0.3
SEG = 360.0 / 7
# The UI leaf points along 40.6 degrees, so today's section is centred on that axis.
AXIS = math.degrees(math.atan2(12, 14))
KAPPA = 0.5522847498


# ---------------------------------------------------------------- path helpers


def pt(r, a, cx=0.0, cy=0.0):
    a = math.radians(a)
    return cx + r * math.sin(a), cy - r * math.cos(a)


def arc(path, r, a0, a1, cx=0.0, cy=0.0):
    """Append a circular arc (angles clockwise from 12 o'clock) as cubics, starting at the current point."""
    n = max(1, math.ceil(abs(a1 - a0) / 45))
    step = (a1 - a0) / n
    for i in range(n):
        s, e = a0 + i * step, a0 + (i + 1) * step
        k = 4 / 3 * math.tan(math.radians(e - s) / 4) * r
        p0, p3 = pt(r, s, cx, cy), pt(r, e, cx, cy)
        t0 = (math.cos(math.radians(s)), math.sin(math.radians(s)))
        t1 = (math.cos(math.radians(e)), math.sin(math.radians(e)))
        path.cubicTo(p0[0] + k * t0[0], p0[1] + k * t0[1], p3[0] - k * t1[0], p3[1] - k * t1[1], *p3)


def circle(r, cx=0.0, cy=0.0):
    p = pathops.Path()
    p.moveTo(*pt(r, 0, cx, cy))
    arc(p, r, 0, 360, cx, cy)
    p.close()
    return p


def poly(points):
    p = pathops.Path()
    p.moveTo(*points[0])
    for q in points[1:]:
        p.lineTo(*q)
    p.close()
    return p


def rrect(x, y, w, h, r):
    p = pathops.Path()
    k = r * (1 - KAPPA)
    p.moveTo(x + r, y)
    p.lineTo(x + w - r, y)
    p.cubicTo(x + w - k, y, x + w, y + k, x + w, y + r)
    p.lineTo(x + w, y + h - r)
    p.cubicTo(x + w, y + h - k, x + w - k, y + h, x + w - r, y + h)
    p.lineTo(x + r, y + h)
    p.cubicTo(x + k, y + h, x, y + h - k, x, y + h - r)
    p.lineTo(x, y + r)
    p.cubicTo(x, y + k, x + k, y, x + r, y)
    p.close()
    return p


def op(a, b, kind):
    return pathops.op(a, b, kind)


def union(*paths):
    out = pathops.Path()
    for p in paths:
        out = op(out, p, pathops.PathOp.UNION)
    return out


def minus(a, *bs):
    for b in bs:
        a = op(a, b, pathops.PathOp.DIFFERENCE)
    return a


def inter(a, b):
    return op(a, b, pathops.PathOp.INTERSECTION)


def transform(path, s, dx, dy):
    out = pathops.Path()
    for verb, pts in path.segments:
        q = [(x * s + dx, y * s + dy) for x, y in pts]
        if verb == "moveTo":
            out.moveTo(*q[0])
        elif verb == "lineTo":
            out.lineTo(*q[0])
        elif verb == "qCurveTo":
            for i in range(len(q) - 1):
                out.quadTo(*q[i], *q[i + 1])
        elif verb == "curveTo":
            out.cubicTo(*q[0], *q[1], *q[2])
        elif verb == "closePath":
            out.close()
    return out


def fmt(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def d(path):
    out = []
    for verb, pts in path.segments:
        c = " ".join(f"{fmt(x)} {fmt(y)}" for x, y in pts)
        if verb == "moveTo":
            out.append(f"M{c}")
        elif verb == "lineTo":
            out.append(f"L{c}")
        elif verb == "curveTo":
            out.append(f"C{c}")
        elif verb == "qCurveTo":
            out.append(f"Q{c}")
        elif verb == "closePath":
            out.append("Z")
    return "".join(out)


def capsule(a, b, w):
    """Straight stroke from a to b of width w with round caps, as cubics only."""
    l1 = (a[0] + (b[0] - a[0]) / 3, a[1] + (b[1] - a[1]) / 3)
    l2 = (a[0] + (b[0] - a[0]) * 2 / 3, a[1] + (b[1] - a[1]) * 2 / 3)
    return smooth_stroke(a, l1, l2, b, w)


def _unit(x, y):
    ln = math.hypot(x, y) or 1
    return x / ln, y / ln


def _round_cap(path, c, n, h):
    """Append a half circle around c from c + n*h to c - n*h (two quarter cubics), bulging away from the
    stroke direction, starting at the current point."""
    k = KAPPA * h
    t = (n[1], -n[0])  # outward tangent: perpendicular to n, pointing away from the stroke body
    a = (c[0] + n[0] * h, c[1] + n[1] * h)
    m = (c[0] + t[0] * h, c[1] + t[1] * h)
    b = (c[0] - n[0] * h, c[1] - n[1] * h)
    path.cubicTo(a[0] + t[0] * k, a[1] + t[1] * k, m[0] + n[0] * k, m[1] + n[1] * k, *m)
    path.cubicTo(m[0] - n[0] * k, m[1] - n[1] * k, b[0] + t[0] * k, b[1] + t[1] * k, *b)


def smooth_stroke(p0, p1, p2, p3, w):
    """Outline of a gently curved cubic centre line of width w with round caps, as six cubics and no
    straight segments. Each side is the centre cubic offset along its end normals, which is exact enough
    for the shallow curvature of a midrib."""
    h = w / 2
    t0 = _unit(p1[0] - p0[0], p1[1] - p0[1])
    t3 = _unit(p3[0] - p2[0], p3[1] - p2[1])
    n0, n3 = (-t0[1], t0[0]), (-t3[1], t3[0])
    nm = _unit(n0[0] + n3[0], n0[1] + n3[1])

    def off(p, n, sgn):
        return p[0] + sgn * n[0] * h, p[1] + sgn * n[1] * h

    p = pathops.Path()
    p.moveTo(*off(p0, n0, +1))
    p.cubicTo(*off(p1, nm, +1), *off(p2, nm, +1), *off(p3, n3, +1))
    _round_cap(p, p3, n3, h)
    p.cubicTo(*off(p2, nm, -1), *off(p1, nm, -1), *off(p0, n0, -1))
    _round_cap(p, p0, (-n0[0], -n0[1]), h)
    p.close()
    return p


# ---------------------------------------------------------------- the plate


def section(k, r_out=R_PLATE, r_in=R_WELL, gap=NOTCH, rho=FILLET):
    """Rim section k: annular sector with parallel notch edges, filleted outer corners, square inner corners."""
    h = gap / 2
    t1 = AXIS - SEG / 2 + k * SEG
    t2 = t1 + SEG
    a_in1 = t1 + math.degrees(math.asin(h / r_in))
    a_in2 = t2 - math.degrees(math.asin(h / r_in))
    rc = r_out - rho
    ac1 = t1 + math.degrees(math.asin((h + rho) / rc))
    ac2 = t2 - math.degrees(math.asin((h + rho) / rc))

    def edge_pt(theta, side, r_on):
        # point on the notch edge line (offset h from the radius at theta) at distance r_on along it
        n = (math.cos(math.radians(theta)) * side, math.sin(math.radians(theta)) * side)
        base = pt(r_on, theta)
        return base[0] + n[0] * h, base[1] + n[1] * h

    def fillet_line_pt(theta, ac, side):
        c = pt(rc, ac)
        n = (math.cos(math.radians(theta)) * side, math.sin(math.radians(theta)) * side)
        return c[0] - rho * n[0], c[1] - rho * n[1]

    p = pathops.Path()
    p.moveTo(*pt(r_in, a_in1))
    l1 = fillet_line_pt(t1, ac1, +1)
    p.lineTo(*l1)
    # fillet from the notch edge onto the outer circle (quarter-ish arc, approximated by one cubic)
    o1 = pt(r_out, ac1)
    p.cubicTo(*_fillet_ctrl(l1, o1, pt(rc, ac1), rho, +1), *o1)
    arc(p, r_out, ac1, ac2)
    o2 = pt(r_out, ac2)
    l2 = fillet_line_pt(t2, ac2, -1)
    p.cubicTo(*_fillet_ctrl(o2, l2, pt(rc, ac2), rho, +1), *l2)
    p.lineTo(*pt(r_in, a_in2))
    arc(p, r_in, a_in2, a_in1)
    p.close()
    return p


def _fillet_ctrl(a, b, c, r, _):
    """Control points of a cubic approximating the circular arc a->b around centre c."""
    va = (a[0] - c[0], a[1] - c[1])
    vb = (b[0] - c[0], b[1] - c[1])
    ang = math.atan2(va[0] * vb[1] - va[1] * vb[0], va[0] * vb[0] + va[1] * vb[1])
    k = 4 / 3 * math.tan(abs(ang) / 4)
    sgn = 1 if ang > 0 else -1
    ta = (-va[1] * sgn, va[0] * sgn)
    tb = (-vb[1] * sgn, vb[0] * sgn)
    return a[0] + k * ta[0], a[1] + k * ta[1], b[0] - k * tb[0], b[1] - k * tb[1]


def plate_parts(notch=NOTCH):
    """Return (plate without today, today section, divider line) in plate units around (0, 0)."""
    well = circle(R_WELL + 0.02)
    days = union(well, *[section(k, gap=notch) for k in range(1, 7)])
    today = section(0, gap=notch)
    whole = union(days, today)
    divider = inter(minus(circle(R_WELL + LINE / 2), circle(R_WELL - LINE / 2)), whole)
    return days, today, divider


# ---------------------------------------------------------------- glyphs (plate units, centred on 0, 0)


def leaf_glyph():
    """The product UI leaf (24 px icon, path 'M6 19c7-1 10-6 12-14-8 1-13 5-14 12l2 2Z'), filled, with a
    knocked-out midrib and a short stem."""
    s, cx, cy = 0.5, 10.9, 12.6
    blade = pathops.Path()
    blade.moveTo(6, 19)
    blade.cubicTo(13, 18, 16, 13, 18, 5)
    blade.cubicTo(10, 6, 5, 10, 4, 17)
    blade.lineTo(6, 19)
    blade.close()
    rib = smooth_stroke((6.6, 17.4), (9, 14.4), (11.5, 11.4), (15.2, 8.4), 0.95)
    stem = capsule((5.2, 18.2), (3.4, 20.6), 1.5)
    shape = union(minus(blade, rib), stem)
    return transform(shape, s, -cx * s, -cy * s)


def cards_glyph():
    a, g, r = 2.7, 0.9, 0.55
    o = -(a + g / 2)
    return union(*[rrect(o + i * (a + g), o + j * (a + g), a, a, r) for i in (0, 1) for j in (0, 1)])


def bridge_glyph():
    """Stone viaduct seen from the side: one silhouette with a wide centre arch and a smaller arch on
    each side, standing on piers. Three tall arches under one thin deck read as a bridge, where a single
    arch in a block reads as a tunnel mouth and a deck over a block as a bench."""
    w, top, foot, leg = 9.6, -1.8, 1.8, 1.0
    body = rrect(-w / 2, top, w, foot - top, 0.55)

    def opening(r, cx):
        return union(circle(r, cx, foot - leg), poly([(cx - r, foot - leg), (cx + r, foot - leg), (cx + r, foot + 0.1), (cx - r, foot + 0.1)]))

    return minus(body, opening(1.8, 0), opening(0.95, -3.3), opening(0.95, 3.3))


def webapp_glyph():
    w, h, t = 8.2, 6.6, 0.95
    outer = rrect(-w / 2, -h / 2, w, h, 1.1)
    inner = rrect(-w / 2 + t, -h / 2 + 2.2, w - 2 * t, h - 2.2 - t, 0.35)
    return minus(outer, inner)


GLYPHS = {"mark": leaf_glyph, "cards": cards_glyph, "bridge": bridge_glyph, "webapp": webapp_glyph}

THEMES = {
    # plate, divider, glyph
    "dark": (OAT, OAT_RIM, HERB),
    "light": (NIGHT, NIGHT_RIM, MINT),
}


def mono_plate(glyph, accent):
    """Single-colour plate in the original solid style: the disc with its seven notch cuts and the glyph
    knocked out. With `accent` (masters used from 180 px up) a thin knocked-out line, as wide as a notch,
    runs between today's section and the well, so today reads as its own solid block. Below 180 px that
    line would blur into a crack, so the small masters leave it out."""
    days, today, _ = plate_parts(NOTCH if accent else NOTCH_SMALL)
    whole = minus(union(days, today), glyph)
    if accent:
        whole = minus(whole, today_line())
    return whole


# The small mono masters (16 to 179 px) widen the notch so it stays at least a whole pixel at 32 px
# (0.6 plate units would be 0.9 px there and blur into a grey hairline).
NOTCH_SMALL = 0.72


def today_line():
    """The knocked-out line between today and the well (mono accent): NOTCH wide, centred on the well
    radius. Each end is cut on the far edge line of the neighbouring notch (a negative gap moves the
    section's edge lines outward by half a notch), so the notch runs straight into the line and turns
    with one clean corner. Ending on the notch's centre line left a half-notch stair step at both ends."""
    return section(0, r_out=R_WELL + NOTCH / 2, r_in=R_WELL - NOTCH / 2, gap=-NOTCH, rho=0.0001)


def plate(variant, cx, cy, u, theme="dark", mono=None, glyph=None, accent=True):
    """Plate markup. Every path carries a class (plate, today, divider, glyph) so check.py can verify the
    leaf colour pairing: HERB glyph on the OAT plate, MINT glyph on the NIGHT plate. `glyph` overrides
    the vector glyph (plate units), for the pixel-tuned small tiles."""
    glyph = glyph if glyph is not None else GLYPHS[variant]()
    t = lambda p: transform(p, u, cx, cy)  # noqa: E731
    if mono:
        return f'<path class="mono" fill="{mono}" d="{d(t(mono_plate(glyph, accent)))}"/>'
    days, today, divider = plate_parts()
    base, line, ink = THEMES[theme]
    return "\n  ".join(
        [
            f'<path class="plate" fill="{base}" d="{d(t(days))}"/>',
            f'<path class="today" fill="{PAPRIKA}" d="{d(t(today))}"/>',
            f'<path class="divider" fill="{line}" d="{d(t(divider))}"/>',
            f'<path class="glyph" fill="{ink}" d="{d(t(glyph))}"/>',
        ]
    )


def svg(body, vb=1024, extra=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb} {vb}" width="{vb}" height="{vb}"{extra}>\n  '
        + body
        + "\n</svg>\n"
    )


TILE_RX = 232
U_TILE = 37  # plate radius 370 on a 1024 tile
U_MASK = 33  # plate radius 330, inside the 409.6 maskable safe circle
TILE_BG = {"dark": NIGHT, "light": OAT}


def tile(variant, theme="dark", glyph=None):
    return svg(
        f'<rect class="bg" width="1024" height="1024" rx="{TILE_RX}" fill="{TILE_BG[theme]}"/>\n  '
        + plate(variant, 512, 512, U_TILE, theme, glyph=glyph)
    )


# ---------------------------------------------------------------- 32 and 48 px tiles, glyph on the pixel grid

# Scaled from the vector master, the bridge's piers and small arches land on sub-pixel widths and blur
# into a comb at 32 and 48 px. At 48 px the three arches are redrawn in whole pixels (x0, y0, x1, y1 of
# the block; corner radius; centre arch: cx, cy, r; side arches: cx offsets, cy, r).
BRIDGE_PX = {
    (48, "tile"): ((16, 21, 32, 27), 0.9, (24, 25, 3), (-5.5, 5.5), 25.5, 1.5),
    (48, "mono"): ((13, 20, 35, 28), 1.2, (24, 26, 4), (-7, 7), 26, 2),
}

# At 16 and 32 px even whole-pixel arches read as a comb (32) or a tunnel mouth (16), so the bridge is
# simplified: one full-width deck bar and one wide arch under it between two solid piers, every edge on
# the pixel grid. Key: (size, plate) with plate "tile" (colour tile) or "mono" (bare mono plate, larger).
# Values: deck x0, x1, deck top y, deck height, pier inset from the deck end, pier width, foot y.
BRIDGE_SIMPLE = {
    (16, "tile"): (3, 13, 7, 1, 1, 2, 12),
    (32, "tile"): (9, 23, 13, 2, 1, 2, 20),
    (32, "mono"): (8, 24, 11, 2, 1, 3, 21),
}


def bridge_simple(key):
    """Deck bar plus one arch, in px coordinates. The arch void is a circle of half the clear span with
    its crown on the deck's underside, snapped column by column to whole pixels (a stepped arch, no
    anti-aliased curve)."""
    x0, x1, y0, dh, inset, pw, foot = BRIDGE_SIMPLE[key]
    pl, pr = x0 + inset + pw, x1 - inset - pw  # clear span between the piers
    r, cx, yc = (pr - pl) / 2, (pl + pr) / 2, y0 + dh + (pr - pl) / 2
    body = union(poly([(x0, y0), (x1, y0), (x1, y0 + dh), (x0, y0 + dh)]),
                 poly([(x0 + inset, y0 + dh), (x1 - inset, y0 + dh), (x1 - inset, foot), (x0 + inset, foot)]))
    void = []
    for c in range(pl, pr):
        dx = c + 0.5 - cx
        top = max(y0 + dh, round(yc - math.sqrt(max(r * r - dx * dx, 0))))
        void.append(poly([(c, top), (c + 1, top), (c + 1, foot), (c, foot)]))
    return minus(body, union(*void))


def bridge_px(key):
    """The three-arch bridge for a (size, plate) key, in px coordinates: whole-pixel piers and deck."""
    (x0, y0, x1, y1), rr, (cx, cy, r), offs, scy, sr = BRIDGE_PX[key]

    def opening(r, cx, cy):
        return union(circle(r, cx, cy), poly([(cx - r, cy), (cx + r, cy), (cx + r, y1 + 0.5), (cx - r, y1 + 0.5)]))

    return minus(rrect(x0, y0, x1 - x0, y1 - y0, rr), opening(r, cx, cy), *[opening(sr, cx + o, scy) for o in offs])


# Cards and web app: scaled from the vector master, the card gap and the window frame fall between pixels
# and turn into a grey smear at 32 and 48 px. Redrawn in whole pixels per size and plate.
# Cards: x0 = y0 of the grid, card size, gap, corner radius.
CARDS_PX = {
    (32, "tile"): (12, 3, 2, 0.5),
    (48, "tile"): (18, 5, 2, 0.8),
    (32, "mono"): (11, 4, 2, 0.6),
    (48, "mono"): (17, 6, 2, 1.0),
}
# Web app: x0, y0, x1, y1 of the window, frame width, title bar height, outer corner radius.
WEBAPP_PX = {
    (32, "tile"): (11, 12, 21, 20, 1, 2, 1.2),
    (48, "tile"): (17, 18, 31, 30, 2, 4, 1.9),
    (32, "mono"): (10, 11, 22, 21, 1, 3, 1.5),
    (48, "mono"): (15, 17, 33, 31, 2, 5, 2.5),
}


def cards_px(key):
    x0, a, g, r = CARDS_PX[key]
    return union(*[rrect(x0 + i * (a + g), x0 + j * (a + g), a, a, r) for i in (0, 1) for j in (0, 1)])


def webapp_px(key):
    x0, y0, x1, y1, t, bar, r = WEBAPP_PX[key]
    inner = poly([(x0 + t, y0 + bar), (x1 - t, y0 + bar), (x1 - t, y1 - t), (x0 + t, y1 - t)])
    return minus(rrect(x0, y0, x1 - x0, y1 - y0, r), inner)


def px_glyph(variant, n, plate_kind="tile"):
    """Pixel-tuned glyph for an n px rendering in px coordinates, or None where the vector glyph is used."""
    key = (n, plate_kind)
    if variant == "bridge":
        if key in BRIDGE_SIMPLE:
            return bridge_simple(key)
        if key in BRIDGE_PX:
            return bridge_px(key)
    if variant == "cards" and key in CARDS_PX:
        return cards_px(key)
    if variant == "webapp" and key in WEBAPP_PX:
        return webapp_px(key)
    return None


def px_to_plate(path, n):
    """n px tile coordinates to plate units; tile() maps them back exactly (plate unit = U_TILE / 1024 * n px)."""
    k = 1024 / n
    return transform(path, k / U_TILE, -512 / U_TILE, -512 / U_TILE)


# ---------------------------------------------------------------- 16 px masters, drawn on the pixel grid


def glyph16(variant):
    if variant == "cards":
        return union(*[rrect(x, y, 2, 2, 0.4) for x in (5, 9) for y in (5, 9)])
    if variant == "bridge":
        # deck bar and one arch on the pixel grid; the deck sits at row 7 so its right end keeps a cream
        # gap to today's section
        return bridge_simple((16, "tile"))
    if variant == "webapp":
        return minus(rrect(4, 5, 8, 6, 1), poly([(5, 7), (11, 7), (11, 10), (5, 10)]))
    # leaf: the UI leaf redrawn wider for 16 px (at true scale it is a two pixel slash), no midrib
    b, t = (5.4, 10.6), (11.0, 5.0)
    m = ((b[0] + t[0]) / 2, (b[1] + t[1]) / 2)
    n = (0.7071, 0.7071)
    blade = pathops.Path()
    blade.moveTo(*b)
    blade.quadTo(m[0] + 4.4 * n[0], m[1] + 4.4 * n[1], *t)
    blade.quadTo(m[0] - 3.6 * n[0], m[1] - 3.6 * n[1], *b)
    blade.close()
    return union(blade, capsule((5.8, 10.2), (4.3, 11.7), 1.2))


def parts16():
    """Plate radius 7, well radius 4.25. Today's section meets the cream rim without notches: paprika
    against cream is contrast enough, and the six sub-pixel notches would only blur."""
    r_out, r_in = 7.0, 4.25
    today = section(0, r_out=r_out, r_in=r_in, gap=0.9, rho=0.3)
    cut = section(0, r_out=r_out + 1, r_in=r_in, gap=0.9, rho=0.0001)
    plate_ = minus(circle(r_out, 8, 8), transform(cut, 1, 8, 8))
    return plate_, transform(today, 1, 8, 8)


def favicon16(variant="mark", theme="dark"):
    plate_, today = parts16()
    base, _, ink = THEMES[theme]
    glyph = glyph16(variant)
    body = [
        f'<rect class="bg" width="16" height="16" rx="3.5" fill="{TILE_BG[theme]}"/>',
        f'<path class="plate" fill="{base}" d="{d(minus(plate_, glyph))}"/>',
        f'<path class="today" fill="{PAPRIKA}" d="{d(today)}"/>',
        f'<path class="glyph" fill="{ink}" d="{d(inter(glyph, plate_))}"/>',
    ]
    return svg("\n  ".join(body), vb=16)


MONO16_R = 7.0


def mono16(variant="mark"):
    """Single-colour 16 px master (also the Safari mask icon): the plate with the 16 px glyph knocked out,
    no tile, no notches and no today accent. One-pixel cuts only blur at this size and read as a bite."""
    body = minus(circle(MONO16_R, 8, 8), glyph16(variant))
    return svg(f'<path class="mono" fill="#000000" d="{d(body)}"/>', vb=16)


def mono_px(variant, n):
    """Pixel-tuned single-colour n px master (no tile, same plate scale as the 1024 mono master), without
    the today accent."""
    u = 48 * n / 1024
    glyph = transform(px_glyph(variant, n, "mono"), 1 / u, -n / 2 / u, -n / 2 / u)
    return svg(plate(variant, n / 2, n / 2, u, mono="#000000", glyph=glyph, accent=False), vb=n)


def write(name, text):
    with open(os.path.join(HERE, name), "w") as fh:
        fh.write(text)


def main():
    for v in GLYPHS:
        write(f"{v}.svg", tile(v))
        write(f"{v}-light.svg", tile(v, "light"))
        write(f"{v}-16.svg", favicon16(v))
        write(f"{v}-mono-16.svg", mono16(v))
        for n in (32, 48):
            g = px_glyph(v, n)
            if g is not None:
                write(f"{v}-{n}.svg", tile(v, glyph=px_to_plate(g, n)))
            if px_glyph(v, n, "mono") is not None:
                write(f"{v}-mono-{n}.svg", mono_px(v, n))
        # mono: with today's accent line from 180 px, plain solid below
        write(f"{v}-mono.svg", svg(plate(v, 512, 512, 48, mono="#000000")))
        write(f"{v}-mono-small.svg", svg(plate(v, 512, 512, 48, mono="#000000", accent=False)))
        # full-bleed square, plate inside the 80 % safe circle (Android maskable, org avatar)
        write(
            f"{v}-maskable.svg",
            svg(f'<rect class="bg" width="1024" height="1024" fill="{NIGHT}"/>\n  ' + plate(v, 512, 512, U_MASK)),
        )
        # full-bleed square with the tile proportions (apple-touch-icon: iOS rounds the corners itself)
        write(
            f"{v}-square.svg",
            svg(f'<rect class="bg" width="1024" height="1024" fill="{NIGHT}"/>\n  ' + plate(v, 512, 512, U_TILE)),
        )
        # plate without tile, transparent: cream plate for dark backgrounds, night plate for light ones
        write(f"{v}-transparent.svg", svg(plate(v, 512, 512, 48, "dark")))
        write(f"{v}-transparent-light.svg", svg(plate(v, 512, 512, 48, "light")))


if __name__ == "__main__":
    main()
