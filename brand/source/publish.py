"""Copy the generated Week Dial set into brand/ under its public names (mealie-atelier-*).

Run after make.sh: venv/bin/python publish.py
Reads ./*.svg and ./out/, writes ../svg/ and ../png/. Social previews are made by social.sh.
"""
import glob
import os
import re
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.dirname(HERE)
FAMILIES = ("cards", "bridge", "webapp")
P = "mealie-atelier"


def svg_name(stem):
    fam = ""
    rest = stem
    if stem.startswith("lockup"):
        parts = stem.split("-")[1:]
        if parts and parts[0] in FAMILIES:
            fam = parts.pop(0) + "-"
        rest = "-".join(parts)
        rest = {"": "dark", "transparent": "dark-transparent", "light": "light",
                "transparent-light": "light-transparent"}[rest]
        return f"{P}-{fam}lockup-{rest}.svg"
    parts = stem.split("-")
    if parts[0] in FAMILIES:
        fam = parts.pop(0) + "-"
    elif parts[0] == "mark":
        parts.pop(0)
    rest = "-".join(parts)
    rest = {"transparent-light": "light-transparent"}.get(rest, rest)
    return f"{P}-{fam}mark" + (f"-{rest}" if rest else "") + ".svg"


HA = {"icon.png": "ha-icon.png", "icon@2x.png": "ha-icon@2x.png",
      "dark_icon.png": "ha-dark-icon.png", "dark_icon@2x.png": "ha-dark-icon@2x.png",
      "logo.png": "ha-logo.png", "logo@2x.png": "ha-logo@2x.png",
      "dark_logo.png": "ha-dark-logo.png", "dark_logo@2x.png": "ha-dark-logo@2x.png"}


def png_name(name):
    fam = ""
    base = name
    for f in FAMILIES:
        if name.startswith(f + "-"):
            fam, base = f + "-", name[len(f) + 1:]
    if base == "avatar-500.png":
        return f"{P}-avatar-500.png"
    base = HA.get(base, base)
    return f"{P}-{fam}{base}"


for sub in ("svg", "png"):
    d = os.path.join(BRAND, sub)
    os.makedirs(d, exist_ok=True)
    for f in glob.glob(os.path.join(d, f"{P}-*")):
        os.remove(f)
for f in sorted(glob.glob(os.path.join(HERE, "*.svg"))):
    shutil.copy(f, os.path.join(BRAND, "svg", svg_name(os.path.basename(f)[:-4])))
for f in sorted(glob.glob(os.path.join(HERE, "out", "*"))):
    n = os.path.basename(f)
    if re.search(r"\.(png|ico)$", n) and not n.endswith("-sheet.png"):
        shutil.copy(f, os.path.join(BRAND, "png", png_name(n)))
    elif n.endswith("favicon.svg") or n.endswith("-favicon.svg"):
        shutil.copy(f, os.path.join(BRAND, "svg", f"{P}-{png_name(n)[len(P) + 1:]}"))
print("published", len(os.listdir(os.path.join(BRAND, "svg"))), "svg,",
      len(os.listdir(os.path.join(BRAND, "png"))), "png/ico")
