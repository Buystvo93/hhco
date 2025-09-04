import json, os
from datetime import datetime

# Load data
with open("players.json", "r", encoding="utf-8") as f:
    players = json.load(f)

# Load templates
with open("templates/index.html") as f:
    index_tpl = f.read()
with open("templates/player.html") as f:
    player_tpl = f.read()

# Ensure folders
os.makedirs("players", exist_ok=True)

# Generate player pages
cards = []
for p in players:
    stats_rows = "\n".join(
        f"<tr><td>{s['season']}</td><td>{s['team']}</td><td>{s['gp']}</td><td>{s['g']}</td><td>{s['a']}</td><td>{s['pts']}</td><td>{s['plusminus']}</td><td>{s['pim']}</td></tr>"
        for s in p["seasons"]
    )
    html = player_tpl
    for key, val in p.items():
        if not isinstance(val, list):
            html = html.replace(f"{{{{{key}}}}}", str(val))
    html = html.replace("{{stats_rows}}", stats_rows)
    with open(f"players/{p['id']}.html", "w", encoding="utf-8") as f:
        f.write(html)
    cards.append(f"<a class='card' href='players/{p['id']}.html'><img src='{p['headshot']}'><div>{p['name']}</div></a>")

# Generate index
index_html = index_tpl.replace("{{player_cards}}", "\n".join(cards))
index_html = index_html.replace("{{count}}", str(len(players)))
with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_html)

print("✅ Site generated! Open index.html in your browser.")
