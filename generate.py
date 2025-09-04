import json, os, shutil
from datetime import datetime

SRC = os.path.dirname(__file__)
DIST = os.path.join(SRC, "dist")
TEMPLATES = os.path.join(SRC, "templates")
ASSETS = os.path.join(SRC, "assets")

# Reset dist folder
if os.path.exists(DIST):
    shutil.rmtree(DIST)
os.makedirs(os.path.join(DIST, "players"), exist_ok=True)
shutil.copytree(ASSETS, os.path.join(DIST, "assets"))

# Load data
with open(os.path.join(SRC, "players.json"), encoding="utf-8") as f:
    players = json.load(f)

# Load templates
with open(os.path.join(TEMPLATES, "index.html")) as f:
    index_tpl = f.read()
with open(os.path.join(TEMPLATES, "player.html")) as f:
    player_tpl = f.read()

# Generate player pages
cards = []
for p in players:
    # Stats table
    stats_rows = "\n".join(
        f"<tr><td>{s['season']}</td><td>{s['team']}</td><td>{s['gp']}</td>"
        f"<td>{s['g']}</td><td>{s['a']}</td><td>{s['pts']}</td>"
        f"<td>{s['plusminus']}</td><td>{s['pim']}</td></tr>"
        for s in p["seasons"]
    )

    # Fill template
    html = player_tpl.replace("{{stats_rows}}", stats_rows)
    for key, val in p.items():
        if not isinstance(val, list):
            html = html.replace(f"{{{{{key}}}}}", str(val))
    html = html.replace("{{year}}", str(datetime.utcnow().year))

    # Save page
    with open(os.path.join(DIST, "players", f"{p['id']}.html"), "w", encoding="utf-8") as f:
        f.write(html)

    # Card for index
    cards.append(f"""
    <a class="card" href="players/{p['id']}.html">
      <div class="top">
        <img alt="{p['name']} headshot" src="{p['headshot']}">
        <div class="meta">
          <div class="name">{p['name']}</div>
          <div class="sub">{p['team_abbr']} • #{p['number']} • {p['position']}</div>
        </div>
      </div>
    </a>
    """)

# Generate index
index_html = index_tpl.replace("{{player_cards}}", "\n".join(cards))
index_html = index_html.replace("{{count}}", str(len(players)))
index_html = index_html.replace("{{year}}", str(datetime.utcnow().year))

with open(os.path.join(DIST, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)

print("✅ Site built in dist/. Upload dist/ to GitHub Pages.")
