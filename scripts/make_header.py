"""Generate assets/header.svg, one SVG that adapts to GitHub's light and dark themes.

Run: python scripts/make_header.py
"""

import math
import pathlib
import random

OUT = pathlib.Path(__file__).resolve().parent.parent / "assets" / "header.svg"

# Throughput curve for the right-hand panel: ramps up, then holds near peak.
rnd = random.Random(11)
X0, X1, Y_BASE, Y_TOP = 744, 1108, 222, 120
N = 40
points = []
for i in range(N):
    t = i / (N - 1)
    level = 1 - math.exp(-5 * t)
    noise = rnd.uniform(-0.05, 0.05) * (0.4 + t)
    y = Y_BASE - (Y_BASE - Y_TOP) * min(1, max(0, level + noise))
    points.append((X0 + (X1 - X0) * t, y))
line = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
area = f"M{X0},{Y_BASE} L" + " L".join(f"{x:.1f},{y:.1f}" for x, y in points) + f" L{X1},{Y_BASE} Z"
end_x, end_y = points[-1]
P99_Y = 200

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="300" viewBox="0 0 1200 300" role="img" aria-labelledby="t d">
  <title id="t">Suhan Ramani, Software Engineer</title>
  <desc id="d">Suhan Ramani, software engineer and CS undergraduate at IIT Jodhpur. Builds backends that stay fast under load, and AI systems. Panel: Orbit, 17.4 million deliveries per second, p99 0.20 ms.</desc>
  <style>
    .bg {{ fill: #ffffff; }} .frame {{ fill: none; stroke: #d0d7de; }}
    .ink {{ fill: #1f2328; }} .soft {{ fill: #59636e; }} .faint {{ fill: #818b98; }}
    .panel {{ fill: #f6f8fa; stroke: #d0d7de; }} .grid {{ stroke: #d8dee4; }}
    .accent {{ fill: #0969da; }} .accentS {{ stroke: #0969da; }} .area {{ fill: #0969da; fill-opacity: .08; }}
    .ok {{ fill: #1a7f37; }} .p99 {{ stroke: #bc4c00; }} .p99t {{ fill: #bc4c00; }}
    @media (prefers-color-scheme: dark) {{
      .bg {{ fill: #0d1117; }} .frame {{ stroke: #30363d; }}
      .ink {{ fill: #f0f6fc; }} .soft {{ fill: #9198a1; }} .faint {{ fill: #6e7681; }}
      .panel {{ fill: #151b23; stroke: #30363d; }} .grid {{ stroke: #21262d; }}
      .accent {{ fill: #4493f8; }} .accentS {{ stroke: #4493f8; }} .area {{ fill: #4493f8; fill-opacity: .12; }}
      .ok {{ fill: #3fb950; }} .p99 {{ stroke: #f0883e; }} .p99t {{ fill: #f0883e; }}
    }}
    .sans {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif; }}
    .mono {{ font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace; }}
    .draw {{ stroke-dasharray: 900; stroke-dashoffset: 900; animation: draw 3.2s ease-out forwards; }}
    .fade {{ opacity: 0; animation: fade .6s ease-out 2.6s forwards; }}
    .pulse {{ animation: pulse 1.8s ease-in-out infinite; }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
    @keyframes fade {{ to {{ opacity: 1; }} }}
    @keyframes pulse {{ 50% {{ opacity: .3; }} }}
    @media (prefers-reduced-motion: reduce) {{ .draw, .fade {{ animation: none; stroke-dashoffset: 0; opacity: 1; }} .pulse {{ animation: none; }} }}
  </style>

  <rect class="bg" width="1200" height="300" rx="12"/>
  <rect class="frame" x=".5" y=".5" width="1199" height="299" rx="11.5"/>

  <!-- identity -->
  <text class="mono faint" x="64" y="64" font-size="13" letter-spacing="1.6">SOFTWARE ENGINEER · IIT JODHPUR</text>
  <text class="sans ink" x="62" y="130" font-size="56" font-weight="700" letter-spacing="-1.4">Suhan Ramani</text>
  <text class="sans soft" x="64" y="170" font-size="21">I build backends that stay fast under load,</text>
  <text class="sans soft" x="64" y="198" font-size="21">and AI systems that people actually use.</text>
  <rect class="accent" x="64" y="226" width="32" height="3" rx="1.5"/>
  <text class="mono faint" x="64" y="260" font-size="13">systems · retrieval · full-stack  —  open to SDE and AI/ML internships</text>

  <!-- live metrics panel -->
  <rect class="panel" x="712" y="40" width="428" height="220" rx="10"/>
  <circle class="ok pulse" cx="736" cy="66" r="4"/>
  <text class="mono soft" x="748" y="70" font-size="12" letter-spacing=".6">orbit · fan-out, 100 clients</text>
  <text class="mono faint" x="1116" y="70" font-size="12" text-anchor="end">bench</text>
  <text class="sans ink" x="736" y="108" font-size="30" font-weight="700" letter-spacing="-.6">17.4M<tspan class="soft" font-size="16" font-weight="400"> deliveries/s</tspan></text>
  <g stroke-width="1">
    <line class="grid" x1="{X0}" y1="{Y_TOP}" x2="{X1}" y2="{Y_TOP}"/>
    <line class="grid" x1="{X0}" y1="{(Y_TOP + Y_BASE) / 2:.0f}" x2="{X1}" y2="{(Y_TOP + Y_BASE) / 2:.0f}"/>
    <line class="grid" x1="{X0}" y1="{Y_BASE}" x2="{X1}" y2="{Y_BASE}"/>
  </g>
  <path class="area fade" d="{area}"/>
  <polyline class="accentS draw" points="{line}" fill="none" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>
  <circle class="accent fade" cx="{end_x:.1f}" cy="{end_y:.1f}" r="4"/>
  <text class="mono faint" x="{X0}" y="246" font-size="11">p99 <tspan class="p99t">0.20 ms</tspan> at 1k clients  ·  0 messages lost to kill -9</text>
</svg>
'''

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(svg)
print("wrote", OUT)
