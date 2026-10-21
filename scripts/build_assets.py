"""
Builds the black & white SVG artwork used by the profile README.

    python scripts/build_assets.py

Edit HANDLE / SECTIONS below and re-run; assets/ is regenerated.
Every SVG carries its own dark background, so it reads the same in GitHub's light and dark themes.
"""
from __future__ import annotations

import random
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
FONT = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "'Courier New', Consolas, 'Liberation Mono', monospace"

HANDLE = "Abhxym"

# slug, title, icon path (16x16 viewBox)
SECTIONS = [
    ("about", "About me", "M8 8a3.5 3.5 0 100-7 3.5 3.5 0 000 7zm0 1.5c-3.3 0-6 1.8-6 4v1.5h12V13.5c0-2.2-2.7-4-6-4z"),
    ("projects", "Featured projects", "M1.5 3A1.5 1.5 0 013 1.5h3.6l1.5 1.8H13A1.5 1.5 0 0114.5 4.8v7.7A1.5 1.5 0 0113 14H3a1.5 1.5 0 01-1.5-1.5z"),
    ("spotlight", "In action", "M1 4.5A1.5 1.5 0 012.5 3h7A1.5 1.5 0 0111 4.5v1.3l4-2.3v9l-4-2.3v1.3A1.5 1.5 0 019.5 13h-7A1.5 1.5 0 011 11.5z"),
    ("stack", "Technologies", "M5.7 3.3L1 8l4.7 4.7 1.1-1.1L3.2 8l3.6-3.6zm4.6 0L9.2 4.4 12.8 8l-3.6 3.6 1.1 1.1L15 8z"),
    ("more", "More projects", "M2 2.5h5v5H2zm7 0h5v5H9zM2 9.5h5v5H2zm7 0h5v5H9z"),
]


def banner_svg() -> str:
    """Misty monochrome landscape with a winding river, like a black & white photograph."""
    w, h = 1200, 340
    title = f"Welcome to {HANDLE}'s GitHub"
    cursor_x = 600 + len(title) * 10.9
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">
  <defs>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#e9e9e9"/><stop offset=".55" stop-color="#bdbdbd"/><stop offset="1" stop-color="#8c8c8c"/>
    </linearGradient>
    <linearGradient id="river" x1="0" y1="1" x2="0" y2="0">
      <stop offset="0" stop-color="#f2f2f2"/><stop offset="1" stop-color="#9a9a9a"/>
    </linearGradient>
    <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".85"/>
    </linearGradient>
    <filter id="blur"><feGaussianBlur stdDeviation="6"/></filter>
    <clipPath id="clip"><rect width="{w}" height="{h}" rx="6"/></clipPath>
  </defs>
  <g clip-path="url(#clip)">
    <rect width="{w}" height="{h}" fill="url(#sky)"/>
    <path fill="#a6a6a6" d="M0 230 L120 196 L230 214 L360 172 L470 204 L600 166 L740 200 L860 176 L980 206 L1100 182 L1200 200 V340 H0Z"/>
    <g filter="url(#blur)" opacity=".7">
      <ellipse cx="300" cy="215" rx="380" ry="22" fill="#e6e6e6"><animate attributeName="cx" values="300;380;300" dur="18s" repeatCount="indefinite"/></ellipse>
      <ellipse cx="920" cy="208" rx="340" ry="18" fill="#e6e6e6"><animate attributeName="cx" values="920;840;920" dur="22s" repeatCount="indefinite"/></ellipse>
    </g>
    <path fill="#6e6e6e" d="M0 262 C 140 226 260 248 380 232 S 620 216 760 238 S 1020 222 1200 240 V340 H0Z"/>
    <path fill="#3c3c3c" d="M0 290 C 160 262 300 280 460 268 S 760 256 900 276 S 1100 268 1200 282 V340 H0Z"/>
    <path fill="#161616" d="M0 316 C 200 298 380 312 600 304 S 1000 296 1200 312 V340 H0Z"/>
    <path fill="url(#river)" opacity=".95" d="M598 236 C 640 248 560 262 610 276 C 680 294 520 306 600 322 C 660 334 700 340 720 340 L 470 340 C 520 330 560 318 530 306 C 480 290 640 280 580 266 C 540 256 600 244 590 236 Z"/>
    <rect width="{w}" height="{h}" fill="url(#fade)" opacity=".35"/>
  </g>
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="6" fill="none" stroke="#ffffff33"/>
  <text x="600" y="108" text-anchor="middle" style="font:700 34px {MONO};fill:#111;letter-spacing:1px">{escape(title)}</text>
  <rect x="{cursor_x:.0f}" y="84" width="14" height="28" fill="#111"><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect>
  <text x="600" y="150" text-anchor="middle" style="font:700 24px {MONO};fill:#111">&lt;/&gt;</text>
</svg>
'''


def astronaut_svg() -> str:
    """A small astronaut drifting through a star field (About me illustration)."""
    w, h = 320, 320
    rnd = random.Random(7)
    stars = "".join(
        f'<circle cx="{rnd.uniform(6, w - 6):.1f}" cy="{rnd.uniform(6, h - 6):.1f}" r="{rnd.choice([0.6, 0.9, 1.2, 1.6])}" fill="#fff">'
        f'<animate attributeName="opacity" values="1;.15;1" dur="{rnd.uniform(1.8, 4.5):.1f}s" begin="{rnd.uniform(0, 3):.1f}s" repeatCount="indefinite"/></circle>'
        for _ in range(70)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="An astronaut floating among the stars">
  <rect width="{w}" height="{h}" rx="6" fill="#000"/>
  {stars}
  <circle cx="262" cy="262" r="34" fill="#1b1b1b" stroke="#ffffff40"/>
  <ellipse cx="262" cy="262" rx="56" ry="12" fill="none" stroke="#ffffff55" stroke-width="2" transform="rotate(-18 262 262)"/>
  <g>
    <animateTransform attributeName="transform" type="translate" values="0 0; 8 -12; 0 0" dur="6s" repeatCount="indefinite"/>
    <g transform="translate(150 150) rotate(-20)">
      <animateTransform attributeName="transform" type="rotate" values="-20 0 0;-8 0 0;-20 0 0" dur="9s" additive="sum" repeatCount="indefinite"/>
      <!-- tether -->
      <path d="M-26 26 C -70 60 -90 110 -150 120" fill="none" stroke="#ffffff66" stroke-width="1.5" stroke-dasharray="3 4"/>
      <!-- backpack -->
      <rect x="-24" y="-10" width="48" height="54" rx="10" fill="#9e9e9e"/>
      <!-- legs -->
      <rect x="-20" y="34" width="16" height="34" rx="7" fill="#e8e8e8" transform="rotate(12 -12 34)"/>
      <rect x="4" y="34" width="16" height="34" rx="7" fill="#e8e8e8" transform="rotate(-18 12 34)"/>
      <!-- body -->
      <rect x="-20" y="-6" width="40" height="48" rx="12" fill="#f4f4f4"/>
      <rect x="-9" y="8" width="18" height="12" rx="2" fill="#2b2b2b"/>
      <circle cx="-4" cy="14" r="1.6" fill="#fff"/><circle cx="3" cy="14" r="1.6" fill="#bdbdbd"/>
      <!-- arms -->
      <rect x="-38" y="0" width="16" height="34" rx="7" fill="#e8e8e8" transform="rotate(38 -30 4)">
        <animateTransform attributeName="transform" type="rotate" values="38 -30 4;20 -30 4;38 -30 4" dur="4s" repeatCount="indefinite"/>
      </rect>
      <rect x="22" y="0" width="16" height="34" rx="7" fill="#e8e8e8" transform="rotate(-48 30 4)"/>
      <!-- helmet -->
      <circle cx="0" cy="-26" r="24" fill="#f4f4f4"/>
      <ellipse cx="2" cy="-26" rx="16" ry="12" fill="#111"/>
      <ellipse cx="-4" cy="-31" rx="6" ry="3" fill="#ffffff" opacity=".6"/>
    </g>
  </g>
</svg>
'''


def section_svg(title: str, icon: str) -> str:
    w, h = 900, 56
    tw = len(title) * 13.2 + 66
    x0 = (w - tw) / 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">
  <line x1="40" y1="28" x2="{x0 - 16:.0f}" y2="28" stroke="#80808066"/>
  <line x1="{x0 + tw + 16:.0f}" y1="28" x2="{w - 40}" y2="28" stroke="#80808066"/>
  <rect x="{x0:.1f}" y="8" width="{tw:.1f}" height="40" rx="6" fill="#000" stroke="#ffffff40"/>
  <g transform="translate({x0 + 18:.1f} 18) scale(1.25)"><path d="{icon}" fill="#fff"/></g>
  <text x="{x0 + 48:.1f}" y="34" style="font:700 20px {MONO};fill:#fff">{escape(title)}</text>
</svg>
'''


def footer_svg() -> str:
    w, h = 1200, 110
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="">
  <path fill="#2a2a2a" d="M0 55 C 200 15 400 95 600 55 S 1000 15 1200 55 V110 H0Z">
    <animate attributeName="d" dur="12s" repeatCount="indefinite" values="
      M0 55 C 200 15 400 95 600 55 S 1000 15 1200 55 V110 H0Z;
      M0 65 C 200 95 400 25 600 65 S 1000 95 1200 45 V110 H0Z;
      M0 55 C 200 15 400 95 600 55 S 1000 15 1200 55 V110 H0Z"/>
  </path>
  <path fill="#000" d="M0 80 C 300 50 500 105 800 74 S 1100 58 1200 80 V110 H0Z"/>
  <text x="600" y="100" text-anchor="middle" style="font:700 13px {MONO};fill:#bdbdbd;letter-spacing:2px">THANKS FOR VISITING</text>
</svg>
'''


def main() -> None:
    for old in ASSETS.glob("section-*.svg"):
        old.unlink()
    (ASSETS / "header.svg").unlink(missing_ok=True)
    (ASSETS / "banner.svg").write_text(banner_svg(), encoding="utf-8")
    (ASSETS / "astronaut.svg").write_text(astronaut_svg(), encoding="utf-8")
    (ASSETS / "footer.svg").write_text(footer_svg(), encoding="utf-8")
    for slug, title, icon in SECTIONS:
        (ASSETS / f"section-{slug}.svg").write_text(section_svg(title, icon), encoding="utf-8")
    print(f"wrote banner, astronaut, footer, {len(SECTIONS)} section titles to {ASSETS}")


if __name__ == "__main__":
    main()
