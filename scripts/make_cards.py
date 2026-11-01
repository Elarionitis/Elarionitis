"""Generate the project card SVGs in assets/cards/. Run: python scripts/make_cards.py"""

import pathlib
from html import escape

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "cards"

PROJECTS = [
    ("signease", "01", "SignEase", "Computer vision",
     ["Reads American Sign Language from a", "webcam and replies in real time."],
     ["TensorFlow", "MediaPipe", "FastAPI", "React"], "#60a5fa", "wave"),
    ("carequeue", "02", "CareQueue", "Health · risk modelling",
     ["Keeps watching an ER waiting room", "for the patients who quietly get worse."],
     ["TypeScript", "Next.js", "Risk models"], "#f472b6", "pulse"),
    ("spendly", "03", "Spendly", "Mobile · event sourcing",
     ["Splits group expenses on an append-only", "ledger, so edits never collide."],
     ["Flutter", "Dart", "Riverpod", "Firestore"], "#34d399", "ledger"),
    ("aeris", "04", "Aeris", "Environmental ML",
     ["Forecasts city air quality and explains", "where the pollution is coming from."],
     ["Python", "XGBoost", "FastAPI", "React"], "#fbbf24", "forecast"),
    ("repo-context-mcp", "05", "repo-context-mcp", "AI tooling",
     ["An MCP server that gives coding agents", "the context of a repository up front."],
     ["TypeScript", "MCP", "GitHub API"], "#a78bfa", "graph"),
    ("orbit", "06", "Orbit", "Systems · networking",
     ["A multi-client TCP chat server in C++,", "one thread per connection."],
     ["C++17", "POSIX sockets", "CMake"], "#22d3ee", "orbit"),
]

W, H = 440, 200
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Inter, Helvetica, Arial, sans-serif"


def motif(kind, c):
    x0, y0 = 330, 34  # motif box: 330..410 x 34..114
    if kind == "wave":
        pts = " ".join(f"{x0 + i * 8},{y0 + 40 + (18 if i % 2 else -18) * (0.4 + (i % 3) * 0.3)}" for i in range(11))
        dots = "".join(f'<circle cx="{x0 + i * 8}" cy="{y0 + 40 + (18 if i % 2 else -18) * (0.4 + (i % 3) * 0.3)}" r="2.2" fill="{c}"/>' for i in range(11))
        return f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-opacity=".5" stroke-width="1.5"/>{dots}'
    if kind == "pulse":
        return (f'<path d="M{x0} {y0+40} h18 l6 -22 l10 44 l8 -34 l6 12 h32" fill="none" stroke="{c}" stroke-width="2" '
                f'stroke-linejoin="round" stroke-dasharray="160" stroke-dashoffset="160">'
                f'<animate attributeName="stroke-dashoffset" values="160;0;0" dur="3s" repeatCount="indefinite"/></path>')
    if kind == "ledger":
        rows = "".join(f'<rect x="{x0}" y="{y0 + i * 16}" width="{80 - i * 9}" height="9" rx="2" fill="{c}" fill-opacity="{0.85 - i * 0.15}"/>' for i in range(5))
        return rows
    if kind == "forecast":
        bars = [22, 34, 28, 46, 38, 56, 44]
        out = ""
        for i, h in enumerate(bars):
            out += f'<rect x="{x0 + i * 12}" y="{y0 + 76 - h}" width="8" height="{h}" rx="2" fill="{c}" fill-opacity="{0.35 + i * 0.09}"/>'
        return out
    if kind == "graph":
        nodes = [(x0 + 8, y0 + 12), (x0 + 60, y0 + 6), (x0 + 36, y0 + 40), (x0 + 74, y0 + 58), (x0 + 12, y0 + 70)]
        edges = [(0, 2), (1, 2), (2, 3), (2, 4), (1, 3)]
        out = "".join(f'<line x1="{nodes[a][0]}" y1="{nodes[a][1]}" x2="{nodes[b][0]}" y2="{nodes[b][1]}" stroke="{c}" stroke-opacity=".45" stroke-width="1.5"/>' for a, b in edges)
        out += "".join(f'<circle cx="{x}" cy="{y}" r="{6 if i == 2 else 4}" fill="{c}"/>' for i, (x, y) in enumerate(nodes))
        return out
    if kind == "orbit":
        cx, cy = x0 + 40, y0 + 40
        return (f'<circle cx="{cx}" cy="{cy}" r="34" fill="none" stroke="{c}" stroke-opacity=".35" stroke-dasharray="3 5"/>'
                f'<circle cx="{cx}" cy="{cy}" r="7" fill="{c}"/>'
                f'<g><circle cx="{cx + 34}" cy="{cy}" r="4" fill="{c}"/>'
                f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="8s" repeatCount="indefinite"/></g>'
                f'<g><circle cx="{cx - 34}" cy="{cy}" r="3" fill="{c}" fill-opacity=".7"/>'
                f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="13s" repeatCount="indefinite"/></g>')
    return ""


def chips(stack, c):
    x, out = 24, []
    for s in stack:
        w = int(len(s) * 6.6 + 18)
        out.append(f'<rect x="{x}" y="152" width="{w}" height="22" rx="11" fill="{c}" fill-opacity=".1" stroke="{c}" stroke-opacity=".35"/>'
                   f'<text x="{x + w / 2}" y="167" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{c}">{escape(s)}</text>')
        x += w + 8
    return "".join(out)


def card(slug, idx, name, domain, lines, stack, c, kind):
    desc = "".join(f'<text x="24" y="{104 + i * 20}" font-family="{SANS}" font-size="14" fill="#9aa7b8">{escape(l)}</text>' for i, l in enumerate(lines))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(name)}: {escape(' '.join(lines))}">
  <title>{escape(name)}</title>
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c}" stop-opacity=".14"/><stop offset=".55" stop-color="{c}" stop-opacity="0"/></linearGradient></defs>
  <rect width="{W}" height="{H}" rx="14" fill="#0b0f14"/>
  <rect width="{W}" height="{H}" rx="14" fill="url(#g)"/>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="13.5" fill="none" stroke="#263241"/>
  <rect x="24" y="0" width="36" height="3" rx="1.5" fill="{c}"/>
  <text x="24" y="38" font-family="{MONO}" font-size="12" fill="{c}">{idx}</text>
  <text x="48" y="38" font-family="{MONO}" font-size="12" fill="#64748b">/ {escape(domain.upper())}</text>
  <text x="24" y="74" font-family="{SANS}" font-size="26" font-weight="700" fill="#f8fafc" letter-spacing="-.4">{escape(name)}</text>
  {desc}
  {motif(kind, c)}
  {chips(stack, c)}
</svg>
'''


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for p in PROJECTS:
        (OUT / f"{p[0]}.svg").write_text(card(*p))
    print("wrote", len(PROJECTS), "cards")
