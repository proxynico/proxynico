"""Draws the profile header: a container ship whose stacks are merged pull requests by month.

Run `python3 assets/ship.py` from the repository root to rewrite ship-light.svg and ship-dark.svg.
"""

import random
from pathlib import Path

MONTHS = [("Apr", 1, "1"), ("May", 9, "9"), ("Jun", 76, "76"), ("Jul", 262, "262"),
          ("Aug", 679, "679"), ("Sep", 763, "763"), ("Oct", 1036, "1,000+")]
TOTAL = "2,800+"
SUBTITLE = "pull requests my agents have merged since April 2026"
PER_BOX = 100

W, H = 680, 392
DECK = 306
BOX_W, BOX_H, BAY_STEP, BAY_X = 64, 15, 70, 116
FONT = "ui-sans-serif, -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
BOXES = ["#b5533c", "#2f5d9a", "#2b7a78", "#d09a32", "#7d8590", "#4f7d4c", "#3b8fc4", "#8c3f3f"]

THEMES = {
    "light": dict(text="#1f2328", muted="#59636e", hull="#1d2b47", hull_text="#f6f8fa", boot="#a63d2f",
                  house="#eef1f4", house_line="#8c959f", window="#2b3445", hatch="#4a5262",
                  water="#2f81c7", water_op="0.10", wave="#2f81c7", funnel="#2b3445"),
    "dark": dict(text="#e6edf3", muted="#9198a1", hull="#2c3d5e", hull_text="#f0f3f6", boot="#b4463a",
                 house="#d9dee4", house_line="#d9dee4", window="#1f2733", hatch="#5b6475",
                 water="#388bfd", water_op="0.14", wave="#58a6ff", funnel="#3a4352"),
}


def boxes():
    rnd = random.Random(7)
    out = []
    for bay, (_, count, _) in enumerate(MONTHS):
        x = BAY_X + bay * BAY_STEP
        prev = None
        for tier in range(round(count / PER_BOX)):
            colour = rnd.choice([c for c in BOXES if c != prev])
            prev = colour
            y = DECK - 4 - (tier + 1) * BOX_H
            ribs = "".join(f'<line x1="{x + i}" y1="{y + 2.5}" x2="{x + i}" y2="{y + BOX_H - 3.5}"/>'
                           for i in range(5, BOX_W - 3, 4))
            out.append(f'<rect x="{x}" y="{y}" width="{BOX_W - 1}" height="{BOX_H - 1}" rx="1" fill="{colour}"/>'
                       f'<g stroke="#000" stroke-opacity=".16" stroke-width=".8">{ribs}</g>'
                       f'<rect x="{x}" y="{y}" width="{BOX_W - 1}" height="{BOX_H - 1}" rx="1" fill="none" '
                       f'stroke="#000" stroke-opacity=".22"/>')
    return "".join(out)


def labels(t):
    out = []
    for bay, (month, count, label) in enumerate(MONTHS):
        cx = BAY_X + bay * BAY_STEP + BOX_W / 2
        top = DECK - 4 - round(count / PER_BOX) * BOX_H
        out.append(f'<text x="{cx}" y="{top - 8}" text-anchor="middle" font-size="20" font-weight="700" '
                   f'fill="{t["text"]}">{label}</text>')
        out.append(f'<text x="{cx}" y="386" text-anchor="middle" font-size="18" fill="{t["muted"]}">{month}</text>')
    return "".join(out)


def svg(t):
    hull = "M22 306 L642 306 L666 297 L640 362 L58 362 Q34 362 30 344 Z"
    portholes = "".join(f'<rect x="{x}" y="{y}" width="9" height="5" rx="1" fill="{t["window"]}"/>'
                        for y in range(168, 296, 20) for x in (46, 58, 70, 82))
    hatches = "".join(f'<rect x="{BAY_X + b * BAY_STEP - 1}" y="{DECK - 4}" width="{BOX_W + 1}" height="4" '
                      f'fill="{t["hatch"]}"/>' for b in range(len(MONTHS)))
    waves = "".join(f'<path d="M{x} {y} q6 -3 12 0 t12 0" fill="none" stroke="{t["wave"]}" stroke-opacity=".45" '
                    f'stroke-width="1.4" stroke-linecap="round"/>'
                    for x, y in [(52, 374), (171, 372), (311, 376), (451, 372), (603, 375)])
    alt = ("A container ship named Not a Developer. Each stack is a month of pull requests merged by Nico's agents "
           "in 2026: 1 in April, 9 in May, 76 in June, 262 in July, 679 in August, 763 in September and over 1,000 "
           "in October. One container is about 100.")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{alt}">
<title>{alt}</title>
<g font-family="{FONT}">
<text x="27" y="62" font-size="56" font-weight="800" letter-spacing="-1" fill="{t["text"]}">{TOTAL}</text>
<text x="30" y="96" font-size="21" fill="{t["muted"]}">{SUBTITLE}</text>
<rect x="556" y="47" width="34" height="13" rx="1" fill="{BOXES[0]}"/>
<text x="652" y="60" text-anchor="end" font-size="19" fill="{t["muted"]}">= {PER_BOX}</text>
<rect x="60" y="126" width="18" height="15" fill="{t["house"]}" stroke="{t["house_line"]}"/>
<line x1="52" y1="120" x2="86" y2="120" stroke="{t["muted"]}" stroke-width="3" stroke-linecap="round"/>
<line x1="69" y1="126" x2="69" y2="120" stroke="{t["muted"]}" stroke-width="2"/>
<rect x="40" y="154" width="58" height="{DECK - 154}" fill="{t["house"]}" stroke="{t["house_line"]}"/>
<rect x="28" y="140" width="82" height="16" rx="1" fill="{t["house"]}" stroke="{t["house_line"]}"/>
<rect x="32" y="145" width="74" height="5" rx="1" fill="{t["window"]}"/>
{portholes}
{hatches}
{boxes()}
<clipPath id="hull"><path d="{hull}"/></clipPath>
<path d="{hull}" fill="{t["hull"]}"/>
<rect x="0" y="348" width="{W}" height="20" fill="{t["boot"]}" clip-path="url(#hull)"/>
<line x1="636" y1="306" x2="636" y2="272" stroke="{t["muted"]}" stroke-width="2"/>
<text x="358" y="336" text-anchor="middle" font-size="22" font-weight="800" letter-spacing="4" fill="{t["hull_text"]}">NOT A DEVELOPER</text>
<linearGradient id="sea"><stop offset="0" stop-color="{t["water"]}" stop-opacity="0"/>
<stop offset=".12" stop-color="{t["water"]}" stop-opacity="{t["water_op"]}"/>
<stop offset=".88" stop-color="{t["water"]}" stop-opacity="{t["water_op"]}"/>
<stop offset="1" stop-color="{t["water"]}" stop-opacity="0"/></linearGradient>
<rect x="0" y="352" width="{W}" height="{H - 352}" fill="url(#sea)"/>
{waves}
{labels(t)}
</g>
</svg>
'''


here = Path(__file__).parent
for name, theme in THEMES.items():
    (here / f"ship-{name}.svg").write_text(svg(theme))
