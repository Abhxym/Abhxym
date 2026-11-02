"""
Builds the SVG artwork used by the profile README, in the bright ShopEase palette.

    python scripts/build_assets.py

Edit HANDLE / SECTIONS below and re-run; assets/ is regenerated.
Every SVG carries its own background, so it reads the same in GitHub's light and dark themes.
"""
from __future__ import annotations

import random
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
FONT = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"

HANDLE = "Abhxym"

# ShopEase storefront colours (web-ui/src/styles.css)
ORANGE, ORANGE_DARK = "#ff8a3d", "#f25c05"
GREEN, GREEN_DARK, GREEN_UP = "#12805c", "#0c6447", "#22a06b"
YELLOW, YELLOW_LIGHT = "#f7c600", "#ffe27a"
PINK, PINK_LIGHT = "#f2679a", "#ffc2d6"
BLUE, BLUE_LIGHT = "#3b6cf6", "#dfe8ff"
INK, BG, LINE = "#1c1f24", "#f6f7f9", "#e7e9ee"

# slug, title, pill colour, text colour, icon path (16x16 viewBox)
SECTIONS = [
    ("about", "About me", ORANGE_DARK, "#fff", "M8 8a3.5 3.5 0 100-7 3.5 3.5 0 000 7zm0 1.5c-3.3 0-6 1.8-6 4v1.5h12V13.5c0-2.2-2.7-4-6-4z"),
    ("projects", "Featured projects", GREEN, "#fff", "M1.5 3A1.5 1.5 0 013 1.5h3.6l1.5 1.8H13A1.5 1.5 0 0114.5 4.8v7.7A1.5 1.5 0 0113 14H3a1.5 1.5 0 01-1.5-1.5z"),
    ("cloud", "Cloud & DevOps", BLUE, "#fff", "M4.5 13.5a3.5 3.5 0 01-.6-6.95A4.5 4.5 0 0112.6 6a3.75 3.75 0 01-.35 7.5z"),
    ("spotlight", "In action", PINK, "#fff", "M1 4.5A1.5 1.5 0 012.5 3h7A1.5 1.5 0 0111 4.5v1.3l4-2.3v9l-4-2.3v1.3A1.5 1.5 0 019.5 13h-7A1.5 1.5 0 011 11.5z"),
    ("stack", "Technologies", YELLOW, INK, "M5.7 3.3L1 8l4.7 4.7 1.1-1.1L3.2 8l3.6-3.6zm4.6 0L9.2 4.4 12.8 8l-3.6 3.6 1.1 1.1L15 8z"),
    ("more", "More projects", ORANGE_DARK, "#fff", "M2 2.5h5v5H2zm7 0h5v5H9zM2 9.5h5v5H2zm7 0h5v5H9z"),
]


def banner_svg() -> str:
    """A storefront-style header: top bar with brand mark, then three hero panels (green, yellow, pink)."""
    w, h = 1200, 360
    title = f"Welcome to {HANDLE}'s GitHub"
    cursor_x = 66 + len(title) * 21.2
    dots = "".join(
        f'<circle cx="{x}" cy="78" r="4" fill="{GREEN_UP}"><animate attributeName="opacity" values="1;.35;1" dur="2.4s" begin="{i * 0.6}s" repeatCount="indefinite"/></circle>'
        f'<text x="{x + 10}" y="82" style="font:500 12px {FONT};fill:#6b7280">{label}</text>'
        for i, (x, label) in enumerate([(30, "ai-ml"), (100, "full-stack"), (196, "cloud-devops")])
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">
  <defs>
    <linearGradient id="mark" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{ORANGE}"/><stop offset="1" stop-color="{ORANGE_DARK}"/></linearGradient>
    <linearGradient id="green" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{GREEN}"/><stop offset="1" stop-color="{GREEN_DARK}"/></linearGradient>
    <linearGradient id="yellow" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{YELLOW_LIGHT}"/><stop offset="1" stop-color="{YELLOW}"/></linearGradient>
    <linearGradient id="pink" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffe0ea"/><stop offset="1" stop-color="{PINK_LIGHT}"/></linearGradient>
    <clipPath id="clip"><rect width="{w}" height="{h}" rx="16"/></clipPath>
    <clipPath id="pg"><rect x="24" y="104" width="640" height="232" rx="18"/></clipPath>
    <clipPath id="py"><rect x="680" y="104" width="240" height="232" rx="18"/></clipPath>
    <clipPath id="pp"><rect x="936" y="104" width="240" height="232" rx="18"/></clipPath>
  </defs>
  <g clip-path="url(#clip)">
    <rect width="{w}" height="{h}" fill="{BG}"/>
    <rect width="{w}" height="60" fill="#fff"/>
    <rect y="60" width="{w}" height="36" fill="#fff"/>
    <line x1="0" y1="60" x2="{w}" y2="60" stroke="{LINE}"/>
    <line x1="0" y1="96" x2="{w}" y2="96" stroke="{LINE}"/>
  </g>
  <rect x="24" y="12" width="36" height="36" rx="10" fill="url(#mark)"/>
  <text x="42" y="37" text-anchor="middle" style="font:800 20px {FONT};fill:#fff">A</text>
  <text x="70" y="38" style="font:700 22px {FONT};fill:{INK};letter-spacing:-.5px">Abh<tspan style="font-weight:800;fill:{ORANGE_DARK}">xym</tspan></text>
  <rect x="1040" y="12" width="136" height="36" rx="10" fill="{GREEN}"/>
  <text x="1108" y="35" text-anchor="middle" style="font:700 13px {FONT};fill:#fff">View projects ↓</text>
  {dots}

  <g clip-path="url(#pg)">
    <rect x="24" y="104" width="640" height="232" fill="url(#green)"/>
    <circle cx="590" cy="300" r="150" fill="#fff" opacity=".1"><animate attributeName="r" values="150;162;150" dur="7s" repeatCount="indefinite"/></circle>
  </g>
  <text x="60" y="176" style="font:800 36px {FONT};fill:#fff;letter-spacing:-.5px">{escape(title)}</text>
  <rect x="{cursor_x:.0f}" y="148" width="4" height="34" rx="2" fill="#fff"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect>
  <text x="60" y="214" style="font:500 17px {FONT};fill:#e7f5ef">AI/ML engineer · models, APIs and the apps people use</text>
  <rect x="60" y="250" width="148" height="38" rx="8" fill="#fff"/>
  <text x="134" y="274" text-anchor="middle" style="font:700 14px {FONT};fill:{GREEN_DARK}">Agents · RAG · Web</text>

  <g clip-path="url(#py)">
    <rect x="680" y="104" width="240" height="232" fill="url(#yellow)"/>
    <circle cx="890" cy="300" r="110" fill="#fff" opacity=".25"><animate attributeName="r" values="110;120;110" dur="6s" repeatCount="indefinite"/></circle>
  </g>
  <text x="704" y="148" style="font:800 23px {FONT};fill:{INK}">Search &amp; ML</text>
  <text x="704" y="174" style="font:500 14px {FONT};fill:#3a3f47">Ranking · Vision · NLP</text>
  <text x="850" y="290" text-anchor="middle" style="font:800 64px {FONT};fill:{INK}">&lt;/&gt;</text>
  <rect x="704" y="196" width="96" height="30" rx="7" fill="{INK}"/>
  <text x="752" y="216" text-anchor="middle" style="font:700 13px {FONT};fill:#fff">Explore</text>

  <g clip-path="url(#pp)">
    <rect x="936" y="104" width="240" height="232" fill="url(#pink)"/>
    <circle cx="1146" cy="300" r="110" fill="#fff" opacity=".35"><animate attributeName="r" values="110;120;110" dur="6.5s" repeatCount="indefinite"/></circle>
  </g>
  <text x="960" y="148" style="font:800 23px {FONT};fill:{INK}">Cloud &amp; DevOps</text>
  <text x="960" y="174" style="font:500 14px {FONT};fill:#3a3f47">Docker · K8s · CI/CD</text>
  <g transform="translate(1066 230)">
    <animateTransform attributeName="transform" type="translate" values="1066 230;1066 222;1066 230" dur="4s" repeatCount="indefinite" additive="replace"/>
    <path transform="scale(4.2)" d="M4.5 13.5a3.5 3.5 0 01-.6-6.95A4.5 4.5 0 0112.6 6a3.75 3.75 0 01-.35 7.5z" fill="{PINK}"/>
  </g>
  <rect x="960" y="196" width="96" height="30" rx="7" fill="{INK}"/>
  <text x="1008" y="216" text-anchor="middle" style="font:700 13px {FONT};fill:#fff">Deploy</text>
</svg>
'''


def astronaut_svg() -> str:
    """A small astronaut drifting past a bright planet (About me illustration)."""
    w, h = 320, 320
    rnd = random.Random(7)
    colours = ["#fff", "#fff", YELLOW_LIGHT, PINK_LIGHT]
    stars = "".join(
        f'<circle cx="{rnd.uniform(6, w - 6):.1f}" cy="{rnd.uniform(6, h - 6):.1f}" r="{rnd.choice([0.7, 1.0, 1.3, 1.7])}" fill="{rnd.choice(colours)}">'
        f'<animate attributeName="opacity" values="1;.2;1" dur="{rnd.uniform(1.8, 4.5):.1f}s" begin="{rnd.uniform(0, 3):.1f}s" repeatCount="indefinite"/></circle>'
        for _ in range(70)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="An astronaut floating among the stars">
  <defs>
    <linearGradient id="space" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{GREEN}"/><stop offset="1" stop-color="{GREEN_DARK}"/></linearGradient>
    <linearGradient id="planet" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{ORANGE}"/><stop offset="1" stop-color="{ORANGE_DARK}"/></linearGradient>
  </defs>
  <rect width="{w}" height="{h}" rx="18" fill="url(#space)"/>
  {stars}
  <circle cx="262" cy="262" r="34" fill="url(#planet)"/>
  <ellipse cx="262" cy="262" rx="56" ry="12" fill="none" stroke="{YELLOW}" stroke-width="3" transform="rotate(-18 262 262)"/>
  <circle cx="58" cy="60" r="14" fill="{PINK}"/><circle cx="54" cy="56" r="4" fill="#fff" opacity=".45"/>
  <g>
    <animateTransform attributeName="transform" type="translate" values="0 0; 8 -12; 0 0" dur="6s" repeatCount="indefinite"/>
    <g transform="translate(150 150) rotate(-20)">
      <animateTransform attributeName="transform" type="rotate" values="-20 0 0;-8 0 0;-20 0 0" dur="9s" additive="sum" repeatCount="indefinite"/>
      <!-- tether -->
      <path d="M-26 26 C -70 60 -90 110 -150 120" fill="none" stroke="#ffffffaa" stroke-width="1.5" stroke-dasharray="3 4"/>
      <!-- backpack -->
      <rect x="-24" y="-10" width="48" height="54" rx="10" fill="{ORANGE_DARK}"/>
      <!-- legs -->
      <rect x="-20" y="34" width="16" height="34" rx="7" fill="#f4f4f4" transform="rotate(12 -12 34)"/>
      <rect x="4" y="34" width="16" height="34" rx="7" fill="#f4f4f4" transform="rotate(-18 12 34)"/>
      <!-- body -->
      <rect x="-20" y="-6" width="40" height="48" rx="12" fill="#fff"/>
      <rect x="-9" y="8" width="18" height="12" rx="2" fill="{INK}"/>
      <circle cx="-4" cy="14" r="1.6" fill="{GREEN_UP}"/><circle cx="3" cy="14" r="1.6" fill="{YELLOW}"/>
      <rect x="-20" y="30" width="40" height="5" fill="{BLUE}"/>
      <!-- arms -->
      <rect x="-38" y="0" width="16" height="34" rx="7" fill="#f4f4f4" transform="rotate(38 -30 4)">
        <animateTransform attributeName="transform" type="rotate" values="38 -30 4;20 -30 4;38 -30 4" dur="4s" repeatCount="indefinite"/>
      </rect>
      <rect x="22" y="0" width="16" height="34" rx="7" fill="#f4f4f4" transform="rotate(-48 30 4)"/>
      <!-- helmet -->
      <circle cx="0" cy="-26" r="24" fill="#fff"/>
      <ellipse cx="2" cy="-26" rx="16" ry="12" fill="{INK}"/>
      <ellipse cx="-4" cy="-31" rx="6" ry="3" fill="{YELLOW_LIGHT}" opacity=".8"/>
    </g>
  </g>
</svg>
'''


def section_svg(title: str, fill: str, ink: str, icon: str) -> str:
    w, h = 900, 56
    tw = len(title) * 11.5 + 66
    x0 = (w - tw) / 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">
  <line x1="40" y1="28" x2="{x0 - 16:.0f}" y2="28" stroke="{fill}" stroke-opacity=".45" stroke-width="2" stroke-linecap="round" stroke-dasharray="2 8"/>
  <line x1="{x0 + tw + 16:.0f}" y1="28" x2="{w - 40}" y2="28" stroke="{fill}" stroke-opacity=".45" stroke-width="2" stroke-linecap="round" stroke-dasharray="2 8"/>
  <rect x="{x0:.1f}" y="8" width="{tw:.1f}" height="40" rx="12" fill="{fill}"/>
  <g transform="translate({x0 + 18:.1f} 18) scale(1.25)"><path d="{icon}" fill="{ink}"/></g>
  <text x="{x0 + 48:.1f}" y="34" style="font:800 19px {FONT};fill:{ink}">{escape(title)}</text>
</svg>
'''


def footer_svg() -> str:
    w, h = 1200, 120

    def wave(fill: str, a: str, b: str) -> str:
        return f'''<path fill="{fill}" d="{a}"><animate attributeName="d" dur="12s" repeatCount="indefinite" values="{a};{b};{a}"/></path>'''

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="">
  {wave(PINK_LIGHT, "M0 40 C 200 10 400 80 600 40 S 1000 10 1200 40 V120 H0Z", "M0 50 C 200 80 400 15 600 50 S 1000 80 1200 30 V120 H0Z")}
  {wave(YELLOW, "M0 62 C 200 32 400 102 600 62 S 1000 32 1200 62 V120 H0Z", "M0 72 C 200 102 400 32 600 72 S 1000 102 1200 52 V120 H0Z")}
  {wave(GREEN, "M0 86 C 300 58 500 112 800 82 S 1100 66 1200 86 V120 H0Z", "M0 80 C 300 104 500 62 800 88 S 1100 104 1200 78 V120 H0Z")}
  <text x="600" y="110" text-anchor="middle" style="font:800 13px {FONT};fill:#fff;letter-spacing:3px">THANKS FOR VISITING</text>
</svg>
'''


def main() -> None:
    for old in ASSETS.glob("section-*.svg"):
        old.unlink()
    (ASSETS / "header.svg").unlink(missing_ok=True)
    (ASSETS / "banner.svg").write_text(banner_svg(), encoding="utf-8")
    (ASSETS / "astronaut.svg").write_text(astronaut_svg(), encoding="utf-8")
    (ASSETS / "footer.svg").write_text(footer_svg(), encoding="utf-8")
    for slug, title, fill, ink, icon in SECTIONS:
        (ASSETS / f"section-{slug}.svg").write_text(section_svg(title, fill, ink, icon), encoding="utf-8")
    print(f"wrote banner, astronaut, footer, {len(SECTIONS)} section titles to {ASSETS}")


if __name__ == "__main__":
    main()
