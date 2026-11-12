#!/usr/bin/env python3
"""Generate the profile header SVGs (light/dark) from the Sungwoo Log design tokens.

Run:  python3 scripts/generate_header.py
"""
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"

def oklch(L, C, h, a=1.0):
    hr = math.radians(h)
    A, B = C * math.cos(hr), C * math.sin(hr)
    l_ = L + 0.3963377774 * A + 0.2158037573 * B
    m_ = L - 0.1055613458 * A - 0.0638541728 * B
    s_ = L - 0.0894841775 * A - 1.2914855480 * B
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    rgb = (
        4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
        -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
        -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s,
    )
    def enc(x):
        x = max(0.0, min(1.0, x))
        return x * 12.92 if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055
    return "#" + "".join(f"{round(enc(c) * 255):02X}" for c in rgb)

THEMES = {
    "light": dict(
        bg="#FFFFFF", line="#E1E2E4", elevated="#FFFFFF",
        label="#000000", neutral="#2E2F33", alt="#70737C", primary="#0066FF",
        blue_soft=oklch(.90, .085, 248), blue=oklch(.70, .19, 248),
        cyan_soft=oklch(.90, .09, 205), cyan=oklch(.73, .18, 205), mint=oklch(.75, .20, 158),
        lime_soft=oklch(.91, .105, 132), lime=oklch(.76, .22, 132),
        purple_soft=oklch(.89, .085, 305), purple=oklch(.72, .19, 305), pink=oklch(.75, .21, 335),
        ro_soft=oklch(.91, .095, 48), ro=oklch(.72, .22, 48), ro_muted=oklch(.78, .16, 55),
        glow=oklch(.80, .20, 328),
    ),
    "dark": dict(
        bg="#1B1C1E", line="#37383C", elevated="#212225",
        label="#FFFFFF", neutral="#C2C4C8", alt="#989BA2", primary="#3385FF",
        blue_soft=oklch(.48, .085, 248), blue=oklch(.74, .19, 248),
        cyan_soft=oklch(.47, .09, 205), cyan=oklch(.75, .18, 205), mint=oklch(.74, .19, 158),
        lime_soft=oklch(.48, .1, 132), lime=oklch(.77, .21, 132),
        purple_soft=oklch(.48, .085, 305), purple=oklch(.76, .18, 305), pink=oklch(.77, .20, 335),
        ro_soft=oklch(.49, .1, 48), ro=oklch(.76, .21, 48), ro_muted=oklch(.68, .16, 55),
        glow=oklch(.76, .19, 328),
    ),
}

def poly(spec):
    pts = []
    for p in spec.split(","):
        x, y = p.split()
        pts.append(f"{float(x.rstrip('%')):g},{float(y.rstrip('%')):g}")
    return " ".join(pts)

POLYS = {
    "cross": "31% 0, 50% 19%, 69% 0, 100% 31%, 81% 50%, 100% 69%, 69% 100%, 50% 81%, 31% 100%, 0 69%, 19% 50%, 0 31%",
    "plus": "34% 0, 66% 0, 66% 34%, 100% 34%, 100% 66%, 66% 66%, 66% 100%, 34% 100%, 34% 66%, 0 66%, 0 34%, 34% 34%",
    "stack": "0 0, 100% 0, 100% 22%, 82% 36%, 100% 36%, 100% 58%, 72% 78%, 0 78%, 28% 58%, 0 58%, 0 36%, 18% 22%, 0 22%",
    "triangle": "50% 0, 100% 100%, 0 100%",
    "steps": "0 0, 33% 0, 33% 33%, 66% 33%, 66% 66%, 100% 66%, 100% 100%, 0 100%",
    "asterisk": "43% 0, 57% 0, 57% 35%, 83% 10%, 93% 20%, 68% 45%, 100% 45%, 100% 59%, 67% 59%, 93% 85%, 83% 95%, 57% 69%, 57% 100%, 43% 100%, 43% 69%, 17% 95%, 7% 85%, 33% 59%, 0 59%, 0 45%, 32% 45%, 7% 20%, 17% 10%, 43% 35%",
    "diamond": "50% 0, 100% 50%, 50% 100%, 0 50%",
    "dome": "0 100%, 100% 100%, 86% 55%, 100% 55%, 100% 50%, 99% 42%, 96% 34%, 92% 26%, 85% 18%, 77% 11%, 67% 6%, 55% 3%, 45% 3%, 33% 6%, 23% 11%, 15% 18%, 8% 26%, 4% 34%, 1% 42%, 0 50%, 0 55%, 14% 55%",
}

def defs(t):
    lin = lambda id_, stops, diag=True: (
        f'<linearGradient id="{id_}" x1="0" y1="0" x2="{1 if diag else 0}" y2="1">'
        + "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
        + "</linearGradient>"
    )
    return "".join([
        lin("g-default", [(0, t["cyan"]), (.48, t["lime"]), (1, t["pink"])]),
        f'<radialGradient id="g-glow" cx=".5" cy=".52" r=".5"><stop offset=".12" stop-color="{t["glow"]}" stop-opacity=".84"/><stop offset=".6" stop-color="{t["glow"]}" stop-opacity="0"/></radialGradient>',
        lin("g-square", [(0, t["blue_soft"]), (.78, t["blue"])]),
        lin("g-plus", [(0, t["cyan"]), (.48, t["mint"]), (1, t["lime"])]),
        lin("g-arch", [(0, t["purple_soft"]), (.72, t["purple"])], False),
        lin("g-dome", [(0, t["lime_soft"]), (.52, t["cyan"]), (1, t["blue"])], False),
        lin("g-triangle", [(0, t["pink"]), (.76, t["purple_soft"])], False),
        lin("g-capsule", [(0, t["blue"]), (1, t["blue_soft"])], False),
        f'<radialGradient id="g-circle" cx=".5" cy=".45" r=".7"><stop offset="0" stop-color="{t["ro"]}"/><stop offset=".28" stop-color="{t["ro_muted"]}"/><stop offset=".62" stop-color="{t["ro_soft"]}"/><stop offset="1" stop-color="{t["elevated"]}"/></radialGradient>',
        lin("g-steps", [(0, t["purple"]), (.58, t["cyan_soft"]), (1, t["blue_soft"])], False),
        lin("g-diamond", [(0, t["ro_soft"]), (1, t["ro"])]),
        lin("g-ring", [(0, t["ro"]), (1, t["ro_muted"])]),
    ])

def shape(kind, t):
    """Return SVG markup for a shape drawn in a 100x100 box."""
    if kind == "square":
        return '<rect width="100" height="100" rx="8" fill="url(#g-square)"/>'
    if kind == "arch":
        return '<path d="M0 100V50a50 50 0 0 1 100 0v44a6 6 0 0 1-6 6H6a6 6 0 0 1-6-6z" fill="url(#g-arch)"/>'
    if kind == "capsule":
        return '<circle cx="50" cy="50" r="50" fill="url(#g-capsule)"/>'
    if kind == "circle":
        return '<circle cx="50" cy="50" r="50" fill="url(#g-circle)"/>'
    if kind == "ring":
        return f'<circle cx="50" cy="50" r="50" fill="url(#g-ring)"/><circle cx="50" cy="50" r="24" fill="none" stroke="{t["elevated"]}" stroke-width="8.5"/>'
    pts = poly(POLYS[kind])
    fill = {"plus": "g-plus", "dome": "g-dome", "triangle": "g-triangle", "steps": "g-steps", "diamond": "g-diamond"}.get(kind)
    if fill:
        return f'<polygon points="{pts}" fill="url(#{fill})"/>'
    return f'<polygon points="{pts}" fill="url(#g-default)"/><polygon points="{pts}" fill="url(#g-glow)"/>'

ROW_A = ["square", "cross", "plus", "arch", "dome", "stack", "triangle", "capsule", "circle"]

def squircle(cx, cy, r, n=5, steps=96):
    """Superellipse |x|^n + |y|^n = r^n as an SVG path (iOS-style rounded square)."""
    pts = []
    for i in range(steps):
        a = 2 * math.pi * i / steps
        c, s = math.cos(a), math.sin(a)
        x = cx + r * math.copysign(abs(c) ** (2 / n), c)
        y = cy + r * math.copysign(abs(s) ** (2 / n), s)
        pts.append(f"{x:.2f} {y:.2f}")
    return "M" + " L".join(pts) + " Z"
ROW_B = ["steps", "asterisk", "diamond", "ring", "square", "cross", "plus", "arch", "dome", "stack"]

W, H = 1280, 480
SIZE, GAP = 60, 44
PITCH = SIZE + GAP

def row(kinds, y, t, cls):
    copies = math.ceil(W / (len(kinds) * PITCH)) + 1
    items = []
    for i, k in enumerate(kinds * copies):
        x = i * PITCH
        items.append(f'<g transform="translate({x} {y}) scale({SIZE / 100})">{shape(k, t)}</g>')
    return f'<g class="{cls}">' + "".join(items) + "</g>", len(kinds) * PITCH

def build(name):
    t = THEMES[name]
    row_a, dist_a = row(ROW_A, 286, t, "row-a")
    row_b, dist_b = row(ROW_B, 378, t, "row-b")
    font = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Apple SD Gothic Neo', 'Malgun Gothic', Helvetica, Arial, sans-serif"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">
<title id="title">Sungwoo Jang</title>
<desc id="desc">Semiconductor research, automated with AI agents. Dongguk University, Semiconductor Science.</desc>
<style>
  text {{ font-family: {font}; }}
  .row-a {{ animation: slide-a 42s linear infinite; }}
  .row-b {{ animation: slide-b 48s linear infinite; }}
  @keyframes slide-a {{ from {{ transform: translateX(0); }} to {{ transform: translateX(-{dist_a}px); }} }}
  @keyframes slide-b {{ from {{ transform: translateX(-{dist_b}px); }} to {{ transform: translateX(0); }} }}
  @media (prefers-reduced-motion: reduce) {{ .row-a, .row-b {{ animation: none; }} }}
</style>
<defs>
  {defs(t)}
  <linearGradient id="fade" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".1" stop-color="#fff"/>
    <stop offset=".9" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
  <mask id="edge"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
  <clipPath id="card"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="24"/></clipPath>
</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="24" fill="{t["bg"]}" stroke="{t["line"]}" stroke-width="2"/>
<g clip-path="url(#card)">
  <text x="72" y="96" fill="{t["primary"]}" font-size="19" font-weight="600" letter-spacing="1.6">DONGGUK UNIVERSITY · SEMICONDUCTOR SCIENCE</text>
  <text x="68" y="176" fill="{t["label"]}" font-size="72" font-weight="800" letter-spacing="-2">Sungwoo Jang</text>
  <text x="72" y="230" fill="{t["neutral"]}" font-size="30" font-weight="500" letter-spacing="-0.4">Semiconductor research, automated with AI agents.</text>
  <g transform="translate({W - 72 - 64} 56)">
    <path d="{squircle(32, 32, 31)}" fill="#FFFFFF" stroke="#000000" stroke-width="2.5"/>
    <text x="32" y="42" text-anchor="middle" fill="#000000" font-family="'Arial Black', 'Helvetica Neue', Arial, sans-serif" font-size="27" font-weight="900" letter-spacing="-0.5">Sj.</text>
  </g>
  <g mask="url(#edge)">{row_a}{row_b}</g>
</g>
</svg>
'''
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"header-{name}.svg").write_text(svg, encoding="utf-8")

if __name__ == "__main__":
    for theme in THEMES:
        build(theme)
    print("wrote", ", ".join(f"assets/header-{n}.svg" for n in THEMES))

