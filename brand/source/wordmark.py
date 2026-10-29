"""Set 'Mealie Atelier' in Bricolage Grotesque (SIL OFL) and write lockups with outlined text.

Run with the local venv: venv/bin/python wordmark.py (make.sh does this)
"""
import io
import os
import sys

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as b  # noqa: E402

SRC = os.path.join(HERE, "font", "BricolageGrotesque.ttf")
_cache = {}


def instance(wght, wdth=90, opsz=48):
    key = (wght, wdth, opsz)
    if key not in _cache:
        font = instantiateVariableFont(TTFont(SRC), {"wght": wght, "wdth": wdth, "opsz": opsz})
        buf = io.BytesIO()
        font.save(buf)
        data = buf.getvalue()
        _cache[key] = (TTFont(io.BytesIO(data)), hb.Font(hb.Face(data)))
    return _cache[key]


def set_text(text, size, x, y, wght, tracking=-0.02, wdth=90, opsz=48):
    """Return (svg path data, advance width in px) for text with baseline at y."""
    tt, hbfont = instance(wght, wdth, opsz)
    upem = tt["head"].unitsPerEm
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hbfont, buf, {"kern": True, "liga": True})
    glyphs = tt.getGlyphSet()
    order = tt.getGlyphOrder()
    scale = size / upem
    track = tracking * upem
    pen = SVGPathPen(glyphs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
    pen_x = 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = order[info.codepoint]
        t = TransformPen(pen, (scale, 0, 0, -scale, x + (pen_x + pos.x_offset) * scale, y - pos.y_offset * scale))
        glyphs[name].draw(t)
        pen_x += pos.x_advance + track
    return pen.getCommands(), (pen_x - track) * scale


WGHT, WDTH, OPSZ, TRACK = 520, 100, 96, -0.012


def lockup(variant, product=None, dark=True, transparent=False):
    """Bare plate plus wordmark. Both themes use the same bare plate (no tile): cream plate on dark,
    night plate on light, exactly like mark-transparent.svg and mark-transparent-light.svg. With
    transparent=True there is no background and the viewBox is cropped to the plate height and the ink."""
    bg = b.NIGHT if dark else b.OAT
    ink = b.OAT if dark else b.NIGHT
    accent = b.MINT if dark else b.HERB
    h = 400
    u = 14  # plate radius 140 px
    cx, cy = 60 + 10 * u, h / 2
    mark = b.plate(variant, cx, cy, u, "dark" if dark else "light")
    tx = cx + 10 * u + 60
    size = 128
    base_y = h / 2 + size * 0.35
    d1, w1 = set_text("Mealie Atelier", size, tx, base_y, WGHT, TRACK, WDTH, OPSZ)
    parts = [f'<path class="wordmark" fill="{ink}" d="{d1}"/>']
    width = tx + w1
    if product:
        gap = size * 0.3
        d2, w2 = set_text(product, size, width + gap, base_y, 380, TRACK, WDTH, OPSZ)
        parts.append(f'<path class="product" fill="{accent}" d="{d2}"/>')
        width += gap + w2
    comment = (
        f"  <!-- Wordmark: Bricolage Grotesque (SIL Open Font License 1.1), wght {WGHT} / 380, wdth {WDTH}, "
        f"opsz {OPSZ}, tracking {TRACK:.1%}, outlined to paths -->\n"
    )
    if transparent:
        x0, y0 = cx - 10 * u, cy - 10 * u
        w, hh = width - x0, 20 * u
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:g} {y0:g} {w:.1f} {hh:g}" '
            f'width="{w:.1f}" height="{hh:g}">\n' + comment + f"  {mark}\n  " + "\n  ".join(parts) + "\n</svg>\n"
        )
    w = int(width + 80)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">\n'
        + comment
        + f'  <rect class="bg" width="{w}" height="{h}" fill="{bg}"/>\n  {mark}\n  '
        + "\n  ".join(parts)
        + "\n</svg>\n"
    )


PRODUCTS = {"mark": None, "cards": "Cards", "bridge": "Bridge", "webapp": "App"}


def main():
    """lockup[-<variant>][-transparent][-light].svg: '-light' is the version for light backgrounds (night
    plate, night text), without it the version for dark backgrounds (cream plate, cream text)."""
    out = {}
    for v, product in PRODUCTS.items():
        stem = "lockup" if v == "mark" else f"lockup-{v}"
        out[f"{stem}.svg"] = lockup(v, product)
        out[f"{stem}-light.svg"] = lockup(v, product, dark=False)
        out[f"{stem}-transparent.svg"] = lockup(v, product, transparent=True)
        out[f"{stem}-transparent-light.svg"] = lockup(v, product, dark=False, transparent=True)
    for name, text in out.items():
        with open(os.path.join(HERE, name), "w") as fh:
            fh.write(text)


if __name__ == "__main__":
    main()
