"""
Builds the SVG assets used by the profile README.

    python scripts/build_assets.py

Edit PROJECTS / ROLES below and re-run; everything in assets/ is regenerated.
SVGs use only inline styles and system fonts so they render inside GitHub's <img> sandbox.
"""
from __future__ import annotations

import textwrap
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
FONT = "'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif"
MONO = "'Cascadia Code', 'SFMono-Regular', Consolas, 'Liberation Mono', monospace"

HANDLE = "Abhxym"
ROLES = [
    "AI / ML Engineer",
    "Agentic &amp; RAG systems",
    "Big-data pipelines",
    "Full-stack apps that ship",
]

# slug, title, category, accent (start, end), description, highlight, chips, badge
PROJECTS = [
    ("clipmind", "ClipMind AI", "GENERATIVE AI · AGENTS", ("#a855f7", "#f59e0b"),
     "13-agent LangGraph pipeline that turns raw video clips and a one-line brief into a captioned, platform-ready reel.",
     "RAG brand rules · review loop · live agent graph",
     ["LangGraph", "Gemini", "Whisper", "FAISS", "FFmpeg", "React"], None),
    ("supplychain-x", "SUPPLYCHAIN-X", "BIG DATA · GRAPHS", ("#06b6d4", "#3b82f6"),
     "Distributed platform that traces how a disaster cascades through global supply chains, hop by hop.",
     "48,827 disasters · 330k trade rows · Kafka live",
     ["HDFS", "Spark", "Kafka", "Neo4j", "FastAPI", "D3"], None),
    ("redrob-ai", "RedRob AI", "SEARCH · RANKING", ("#ef4444", "#f97316"),
     "Explainable candidate ranking over 100k profiles: BM25 + FAISS fused with RRF, JD-aware signals and a cross-encoder rerank.",
     "No LLM · CPU only · every score explained",
     ["BM25", "FAISS", "Cross-encoder", "FastAPI", "React"], None),
    ("insightflow", "InsightFlow", "NLP · RAG ANALYTICS", ("#10b981", "#06b6d4"),
     "Survey analytics where non-technical users ask questions in plain English and get cited answers.",
     "Themes + sentiment · RAG agent with citations",
     ["Gemini", "Pinecone", "FastAPI", "React", "Node.js", "MySQL"], None),
    ("glaucoma-ai", "Glaucoma AI", "MEDICAL IMAGING", ("#3b82f6", "#a855f7"),
     "Multi-stage clinical decision support that screens retinal fundus images for glaucoma, with a dashboard for doctors.",
     "YOLOv8 → UNet++ / transformer → XGBoost",
     ["PyTorch", "YOLOv8", "UNet++", "XGBoost", "Next.js"], None),
    ("aquaalert", "AquaAlert AI", "CLIMATE · EXPLAINABLE ML", ("#0ea5e9", "#22d3ee"),
     "Flood detection and early warning from telemetry, rainfall and satellite imagery, with explanations for every prediction.",
     "XGBoost · LSTM · U-Net · SHAP + Grad-CAM",
     ["TensorFlow", "XGBoost", "SHAP", "FastAPI", "React"], None),
    ("schoolmonitor", "School Monitor", "FULL-STACK · GOV-TECH", ("#f59e0b", "#ef4444"),
     "Monitoring system for 12 Zilla Parishad schools: attendance, events, reports, GR publishing and a public transparency page.",
     "Role-based access · Google OAuth · deployed",
     ["Next.js", "Express", "MongoDB", "JWT"], "LIVE"),
    ("system-design-atlas", "System Design Atlas", "INTERACTIVE REFERENCE", ("#8b5cf6", "#ec4899"),
     "Animated, interactive reference for 111 system design concepts with trade-offs, real examples and interview prep.",
     "16 domains · 10 classic systems, step by step",
     ["HTML", "Canvas", "JavaScript"], "LIVE"),
]


def chip_width(text: str) -> float:
    return len(text) * 6.9 + 22


def card_svg(slug, title, category, accent, desc, highlight, chips, badge) -> str:
    w, h = 440, 236
    a1, a2 = accent
    lines = textwrap.wrap(desc, 56)[:3]
    desc_svg = "".join(
        f'<text x="28" y="{104 + i * 20}" class="desc">{escape(line)}</text>' for i, line in enumerate(lines)
    )
    hl_y = 104 + len(lines) * 20 + 10
    x = 28.0
    chips_svg = ""
    for c in chips:
        cw = chip_width(c)
        if x + cw > w - 24:
            break
        chips_svg += (
            f'<rect x="{x:.1f}" y="194" width="{cw:.1f}" height="24" rx="12" class="chip"/>'
            f'<text x="{x + cw / 2:.1f}" y="210.5" class="chipt" text-anchor="middle">{escape(c)}</text>'
        )
        x += cw + 8
    badge_svg = ""
    if badge:
        badge_svg = (
            f'<rect x="{w - 84}" y="22" width="58" height="22" rx="11" fill="#10b98122" stroke="#10b981" stroke-width="1"/>'
            f'<circle cx="{w - 72}" cy="33" r="3.5" fill="#10b981"><animate attributeName="opacity" values="1;.25;1" dur="1.8s" repeatCount="indefinite"/></circle>'
            f'<text x="{w - 46}" y="37.5" text-anchor="middle" style="font:700 10.5px {FONT};fill:#34d399;letter-spacing:1px">{badge}</text>'
        )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}: {escape(desc)}">
  <defs>
    <linearGradient id="acc" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a1}"/><stop offset="1" stop-color="{a2}"/></linearGradient>
    <radialGradient id="glow" cx="1" cy="0" r="1"><stop offset="0" stop-color="{a1}" stop-opacity=".28"/><stop offset=".6" stop-color="{a2}" stop-opacity="0"/></radialGradient>
    <clipPath id="clip"><rect width="{w}" height="{h}" rx="18"/></clipPath>
    <style>
      .cat{{font:700 10.5px {FONT};letter-spacing:1.6px;fill:{a1}}}
      .title{{font:800 25px {FONT};fill:#f8fafc}}
      .desc{{font:400 13.5px {FONT};fill:#a8b3c7}}
      .hl{{font:600 12px {MONO};fill:{a2}}}
      .chip{{fill:#ffffff0d;stroke:#ffffff1f;stroke-width:1}}
      .chipt{{font:600 11.5px {FONT};fill:#dbe3ef}}
    </style>
  </defs>
  <g clip-path="url(#clip)">
    <rect width="{w}" height="{h}" fill="#0b1020"/>
    <rect width="{w}" height="{h}" fill="url(#glow)"/>
    <rect width="5" height="{h}" fill="url(#acc)"/>
  </g>
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="17.5" fill="none" stroke="#ffffff1a"/>
  <text x="28" y="38" class="cat">{escape(category)}</text>
  {badge_svg}
  <text x="28" y="74" class="title">{escape(title)}</text>
  {desc_svg}
  <text x="28" y="{hl_y}" class="hl">▸ {escape(highlight)}</text>
  {chips_svg}
</svg>
'''


def header_svg() -> str:
    w, h = 1200, 340
    n = len(ROLES)
    period = n * 3
    role_svg = ""
    fade = 0.25 / period  # 0.25 s cross-fade
    for i, role in enumerate(ROLES):
        start, end = i / n, (i + 1) / n
        if i == 0:
            kt, vals = f"0;{fade:.4f};{end - fade:.4f};{end:.4f};1", "0;1;1;0;0"
        elif i == n - 1:
            kt, vals = f"0;{start:.4f};{start + fade:.4f};{1 - fade:.4f};1", "0;0;1;1;0"
        else:
            kt, vals = f"0;{start:.4f};{start + fade:.4f};{end - fade:.4f};{end:.4f};1", "0;0;1;1;0;0"
        role_svg += (
            f'<text x="80" y="226" class="role" opacity="0">{role}'
            f'<animate attributeName="opacity" values="{vals}" keyTimes="{kt}" dur="{period}s" repeatCount="indefinite"/>'
            f'</text>'
        )

    # Constellation of nodes on the right: an "agent graph"
    nodes = [(820, 90), (930, 60), (1050, 100), (1110, 190), (990, 170), (880, 200), (960, 270), (1080, 280), (800, 260)]
    edges = [(0, 1), (1, 2), (2, 3), (1, 4), (4, 3), (0, 5), (5, 4), (5, 6), (6, 7), (4, 7), (8, 5), (8, 6), (2, 4)]
    edges_svg = "".join(
        f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" class="edge"/>' for a, b in edges
    )
    pulses = "".join(
        f'<circle r="3.2" fill="#fbbf24"><animateMotion dur="{2.6 + (i % 4) * 0.7:.1f}s" begin="{i * 0.45:.2f}s" repeatCount="indefinite" '
        f'path="M{nodes[a][0]},{nodes[a][1]} L{nodes[b][0]},{nodes[b][1]}"/></circle>'
        for i, (a, b) in enumerate(edges[::2])
    )
    nodes_svg = "".join(
        f'<circle cx="{x}" cy="{y}" r="{7 if i % 3 else 10}" class="node">'
        f'<animate attributeName="r" values="{7 if i % 3 else 10};{9 if i % 3 else 13};{7 if i % 3 else 10}" dur="{3 + i % 3}s" repeatCount="indefinite"/></circle>'
        for i, (x, y) in enumerate(nodes)
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Hi, I'm {HANDLE}. AI/ML engineer building agentic, retrieval and data systems.">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#070b18"/><stop offset="1" stop-color="#130a26"/></linearGradient>
    <linearGradient id="name" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#c084fc"/><stop offset=".5" stop-color="#f472b6"/><stop offset="1" stop-color="#fbbf24"/>
      <animateTransform attributeName="gradientTransform" type="translate" values="-0.3 0;0.3 0;-0.3 0" dur="8s" repeatCount="indefinite"/>
    </linearGradient>
    <radialGradient id="b1"><stop offset="0" stop-color="#7c3aed" stop-opacity=".55"/><stop offset="1" stop-color="#7c3aed" stop-opacity="0"/></radialGradient>
    <radialGradient id="b2"><stop offset="0" stop-color="#f59e0b" stop-opacity=".35"/><stop offset="1" stop-color="#f59e0b" stop-opacity="0"/></radialGradient>
    <radialGradient id="b3"><stop offset="0" stop-color="#06b6d4" stop-opacity=".35"/><stop offset="1" stop-color="#06b6d4" stop-opacity="0"/></radialGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#ffffff" stroke-opacity=".045"/></pattern>
    <clipPath id="clip"><rect width="{w}" height="{h}" rx="24"/></clipPath>
    <style>
      .hi{{font:600 22px {FONT};fill:#94a3b8;letter-spacing:.5px}}
      .name{{font:900 76px {FONT};fill:url(#name);letter-spacing:-1.5px}}
      .role{{font:600 28px {FONT};fill:#e2e8f0}}
      .tag{{font:500 15px {MONO};fill:#64748b}}
      .edge{{stroke:#a78bfa;stroke-opacity:.35;stroke-width:1.5}}
      .node{{fill:#0b1020;stroke:#c084fc;stroke-width:2.5}}
    </style>
  </defs>
  <g clip-path="url(#clip)">
    <rect width="{w}" height="{h}" fill="url(#bg)"/>
    <rect width="{w}" height="{h}" fill="url(#grid)"/>
    <circle cx="180" cy="40" r="260" fill="url(#b1)"><animate attributeName="cx" values="180;260;180" dur="14s" repeatCount="indefinite"/></circle>
    <circle cx="1050" cy="320" r="240" fill="url(#b2)"><animate attributeName="cy" values="320;270;320" dur="11s" repeatCount="indefinite"/></circle>
    <circle cx="700" cy="-20" r="220" fill="url(#b3)"><animate attributeName="cx" values="700;620;700" dur="13s" repeatCount="indefinite"/></circle>
    {edges_svg}
    {pulses}
    {nodes_svg}
  </g>
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="23.5" fill="none" stroke="#ffffff1f"/>
  <text x="82" y="104" class="hi">Hi there, I'm</text>
  <text x="76" y="180" class="name">{HANDLE}</text>
  {role_svg}
  <text x="82" y="282" class="tag">// LLM agents · RAG &amp; search · data platforms · full-stack</text>
</svg>
'''


def section_svg(title: str, slug: str, a1: str, a2: str) -> str:
    w, h = 900, 64
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}">
  <defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{a1}"/><stop offset="1" stop-color="{a2}"/></linearGradient></defs>
  <rect x="0" y="24" width="6" height="22" rx="3" fill="url(#g)"/>
  <text x="20" y="42" style="font:800 24px {FONT};fill:url(#g)">{escape(title)}</text>
  <rect x="{20 + len(title) * 14.5 + 18:.0f}" y="34" width="{max(0, w - (20 + len(title) * 14.5 + 18)):.0f}" height="2" rx="1" fill="url(#g)" opacity=".35"/>
</svg>
'''


def footer_svg() -> str:
    w, h = 1200, 120
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Thanks for visiting">
  <defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#7c3aed"/><stop offset=".5" stop-color="#ec4899"/><stop offset="1" stop-color="#f59e0b"/></linearGradient></defs>
  <path fill="url(#g)" opacity=".9" d="M0 60 C 200 10 400 110 600 60 S 1000 10 1200 60 V120 H0Z">
    <animate attributeName="d" dur="10s" repeatCount="indefinite" values="
      M0 60 C 200 10 400 110 600 60 S 1000 10 1200 60 V120 H0Z;
      M0 70 C 200 110 400 20 600 70 S 1000 110 1200 50 V120 H0Z;
      M0 60 C 200 10 400 110 600 60 S 1000 10 1200 60 V120 H0Z"/>
  </path>
  <path fill="#0b1020" opacity=".55" d="M0 85 C 300 55 500 115 800 80 S 1100 60 1200 85 V120 H0Z"/>
</svg>
'''


SECTIONS = [
    ("Featured projects", "projects", "#c084fc", "#f59e0b"),
    ("In action", "spotlight", "#22d3ee", "#a78bfa"),
    ("Tech I work with", "stack", "#f472b6", "#fbbf24"),
    ("More on my GitHub", "more", "#34d399", "#22d3ee"),
    ("How I build", "approach", "#fbbf24", "#f472b6"),
]


def main() -> None:
    (ASSETS / "cards").mkdir(parents=True, exist_ok=True)
    (ASSETS / "header.svg").write_text(header_svg(), encoding="utf-8")
    (ASSETS / "footer.svg").write_text(footer_svg(), encoding="utf-8")
    for title, slug, a1, a2 in SECTIONS:
        (ASSETS / f"section-{slug}.svg").write_text(section_svg(title, slug, a1, a2), encoding="utf-8")
    for p in PROJECTS:
        if len(p[5]) > 50:
            raise SystemExit(f"highlight too long for the card ({len(p[5])} > 50 chars): {p[5]}")
        (ASSETS / "cards" / f"{p[0]}.svg").write_text(card_svg(*p), encoding="utf-8")
    print(f"wrote {len(PROJECTS)} cards, header, footer and {len(SECTIONS)} section titles to {ASSETS}")


if __name__ == "__main__":
    main()
