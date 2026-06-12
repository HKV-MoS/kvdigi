"""WM 2026 v3 — SVG-Umrisskarte (Parlament-Stil), Spielplan permanent live.

Änderungen ggü. v2:
- Leaflet raus → stilisierte SVG-Karte (USA/Mexiko/Kanada + Great Lakes)
- Live-Daten werden IMMER geladen (60s-Intervall), Spielplan-Tab zeigt immer echte Resultate
- Kippschalter steuert nur noch: echte Resultate in die Tipp-Tabellen übernehmen
- Live-Spiele: approximierte Spielminute + Halbzeitstand
"""
import json
from wm2026_data import TEAMS, GROUPS_ORDER, STADIONS, MATCHES_GROUP
from wm2026_map import USA, MEXICO, CANADA, LAKES, project, poly_points

# ─── Mappings (wie v2) ───────────────────────────────────────────────────
LAND_WIKI = {
    "MEX": "Mexiko", "RSA": "Südafrika", "KOR": "Südkorea", "CZE": "Tschechien",
    "CAN": "Kanada", "BIH": "Bosnien_und_Herzegowina", "QAT": "Katar", "SUI": "Schweiz",
    "BRA": "Brasilien", "MAR": "Marokko", "HAI": "Haiti", "SCO": "Schottland",
    "USA": "Vereinigte_Staaten", "PAR": "Paraguay", "AUS": "Australien", "TUR": "Türkei",
    "GER": "Deutschland", "CUW": "Curaçao", "CIV": "Elfenbeinküste", "ECU": "Ecuador",
    "NED": "Niederlande", "JPN": "Japan", "SWE": "Schweden", "TUN": "Tunesien",
    "BEL": "Belgien", "EGY": "Ägypten", "IRN": "Iran", "NZL": "Neuseeland",
    "ESP": "Spanien", "CPV": "Kap_Verde", "KSA": "Saudi-Arabien", "URU": "Uruguay",
    "FRA": "Frankreich", "SEN": "Senegal", "IRQ": "Irak", "NOR": "Norwegen",
    "ARG": "Argentinien", "ALG": "Algerien", "AUT": "Österreich", "JOR": "Jordanien",
    "POR": "Portugal", "COD": "Demokratische_Republik_Kongo", "UZB": "Usbekistan", "COL": "Kolumbien",
    "ENG": "England", "CRO": "Kroatien", "GHA": "Ghana", "PAN": "Panama",
}
VERBAND_WIKI = {
    "MEX": "Federación_Mexicana_de_Fútbol", "RSA": "South_African_Football_Association",
    "KOR": "Korea_Football_Association", "CZE": "Fotbalová_asociace_České_republiky",
    "CAN": "Canadian_Soccer_Association", "BIH": "Nogometni/Fudbalski_savez_Bosne_i_Hercegovine",
    "QAT": "Qatar_Football_Association", "SUI": "Schweizerischer_Fussballverband",
    "BRA": "Confederação_Brasileira_de_Futebol", "MAR": "Fédération_Royale_Marocaine_de_Football",
    "HAI": "Fédération_Haïtienne_de_Football", "SCO": "Scottish_Football_Association",
    "USA": "United_States_Soccer_Federation", "PAR": "Asociación_Paraguaya_de_Fútbol",
    "AUS": "Football_Australia", "TUR": "Türkiye_Futbol_Federasyonu",
    "GER": "Deutscher_Fußball-Bund", "CUW": "Federashon_Futbol_Kòrsou",
    "CIV": "Fédération_Ivoirienne_de_Football", "ECU": "Federación_Ecuatoriana_de_Fútbol",
    "NED": "Koninklijke_Nederlandse_Voetbalbond", "JPN": "Japan_Football_Association",
    "SWE": "Svenska_Fotbollförbundet", "TUN": "Fédération_Tunisienne_de_Football",
    "BEL": "Königlicher_Belgischer_Fußballverband", "EGY": "Egyptian_Football_Association",
    "IRN": "Football_Federation_Islamic_Republic_of_Iran", "NZL": "New_Zealand_Football",
    "ESP": "Real_Federación_Española_de_Fútbol", "CPV": "Federação_Caboverdiana_de_Futebol",
    "KSA": "Saudi_Arabian_Football_Federation", "URU": "Asociación_Uruguaya_de_Fútbol",
    "FRA": "Fédération_Française_de_Football", "SEN": "Fédération_Sénégalaise_de_Football",
    "IRQ": "Iraq_Football_Association", "NOR": "Norges_Fotballforbund",
    "ARG": "Asociación_del_Fútbol_Argentino", "ALG": "Fédération_Algérienne_de_Football",
    "AUT": "Österreichischer_Fußball-Bund", "JOR": "Jordan_Football_Association",
    "POR": "Federação_Portuguesa_de_Futebol", "COD": "Fédération_Congolaise_de_Football-Association",
    "UZB": "Uzbekistan_Football_Association", "COL": "Federación_Colombiana_de_Fútbol",
    "ENG": "Football_Association", "CRO": "Hrvatski_nogometni_savez",
    "GHA": "Ghana_Football_Association", "PAN": "Federación_Panameña_de_Fútbol",
}
STADION_WIKI = {
    "atl": "Mercedes-Benz_Stadium", "bos": "Gillette_Stadium", "dal": "AT&T_Stadium",
    "hou": "NRG_Stadium", "kan": "Arrowhead_Stadium", "los": "SoFi_Stadium",
    "mia": "Hard_Rock_Stadium", "nyc": "MetLife_Stadium", "phi": "Lincoln_Financial_Field",
    "sfo": "Levi’s_Stadium", "sea": "Lumen_Field", "azt": "Aztekenstadion",
    "gua": "Estadio_Akron", "mty": "Estadio_BBVA", "tor": "BMO_Field", "van": "BC_Place",
}
OLDB_ALIAS = {
    "mexiko": "MEX", "südafrika": "RSA", "suedafrika": "RSA", "südkorea": "KOR",
    "suedkorea": "KOR", "korea republik": "KOR", "korea, süd": "KOR", "republik korea": "KOR",
    "tschechien": "CZE", "tschechische republik": "CZE", "kanada": "CAN",
    "bosnien-herzegowina": "BIH", "bosnien und herzegowina": "BIH", "bosnien": "BIH",
    "katar": "QAT", "schweiz": "SUI", "brasilien": "BRA", "marokko": "MAR",
    "haiti": "HAI", "schottland": "SCO", "usa": "USA", "vereinigte staaten": "USA",
    "vereinigte staaten von amerika": "USA",
    "paraguay": "PAR", "australien": "AUS", "türkei": "TUR", "tuerkei": "TUR",
    "deutschland": "GER", "curacao": "CUW", "curaçao": "CUW",
    "elfenbeinküste": "CIV", "elfenbeinkueste": "CIV", "cote d'ivoire": "CIV",
    "côte d'ivoire": "CIV", "ecuador": "ECU",
    "niederlande": "NED", "japan": "JPN", "schweden": "SWE", "tunesien": "TUN",
    "belgien": "BEL", "ägypten": "EGY", "aegypten": "EGY", "iran": "IRN", "ir iran": "IRN",
    "neuseeland": "NZL", "spanien": "ESP", "kap verde": "CPV", "kapverde": "CPV",
    "cabo verde": "CPV",
    "saudi-arabien": "KSA", "saudi arabien": "KSA", "uruguay": "URU",
    "frankreich": "FRA", "senegal": "SEN", "irak": "IRQ", "norwegen": "NOR",
    "argentinien": "ARG", "algerien": "ALG", "österreich": "AUT", "oesterreich": "AUT",
    "jordanien": "JOR", "portugal": "POR", "dr kongo": "COD", "kongo dr": "COD",
    "demokratische republik kongo": "COD", "kongo, demokratische republik": "COD",
    "usbekistan": "UZB", "kolumbien": "COL",
    "england": "ENG", "kroatien": "CRO", "ghana": "GHA", "panama": "PAN",
    # Englische Namen (TheSportsDB)
    "mexico": "MEX", "south africa": "RSA", "south korea": "KOR", "korea republic": "KOR",
    "czech republic": "CZE", "czechia": "CZE", "canada": "CAN",
    "bosnia and herzegovina": "BIH", "bosnia herzegovina": "BIH", "switzerland": "SUI", "brazil": "BRA",
    "morocco": "MAR", "scotland": "SCO", "united states": "USA",
    "australia": "AUS", "turkey": "TUR", "türkiye": "TUR", "germany": "GER",
    "ivory coast": "CIV", "netherlands": "NED", "sweden": "SWE", "tunisia": "TUN",
    "belgium": "BEL", "egypt": "EGY", "new zealand": "NZL", "spain": "ESP",
    "cape verde": "CPV", "saudi arabia": "KSA", "france": "FRA",
    "iraq": "IRQ", "norway": "NOR", "argentina": "ARG", "algeria": "ALG",
    "austria": "AUT", "jordan": "JOR", "dr congo": "COD", "congo dr": "COD",
    "uzbekistan": "UZB", "colombia": "COL", "croatia": "CRO", "qatar": "QAT",
}
R32_BRACKET = [
    {"id": "r32_1", "a": "1E", "b": "3:ABCDF"}, {"id": "r32_2", "a": "1I", "b": "3:CDFGH"},
    {"id": "r32_3", "a": "2A", "b": "2B"}, {"id": "r32_4", "a": "1F", "b": "2C"},
    {"id": "r32_5", "a": "1C", "b": "2F"}, {"id": "r32_6", "a": "2E", "b": "2I"},
    {"id": "r32_7", "a": "1A", "b": "3:CEFHI"}, {"id": "r32_8", "a": "1L", "b": "3:EHIJK"},
    {"id": "r32_9", "a": "2K", "b": "2L"}, {"id": "r32_10", "a": "1H", "b": "2J"},
    {"id": "r32_11", "a": "1D", "b": "3:BEFIJ"}, {"id": "r32_12", "a": "1G", "b": "3:AEHIJ"},
    {"id": "r32_13", "a": "1J", "b": "2H"}, {"id": "r32_14", "a": "2D", "b": "2G"},
    {"id": "r32_15", "a": "1B", "b": "3:EFGIJ"}, {"id": "r32_16", "a": "1K", "b": "3:DEIJL"},
]

# Heimtrikot-Farben (fill, Nummernfarbe) für die grafische Aufstellung
JERSEY = {
    "MEX": ["#006847", "#FFFFFF"], "RSA": ["#FFB612", "#007749"], "KOR": ["#CD2E3A", "#FFFFFF"],
    "CZE": ["#D7141A", "#FFFFFF"], "CAN": ["#C8102E", "#FFFFFF"], "BIH": ["#002F6C", "#F8C300"],
    "QAT": ["#8A1538", "#FFFFFF"], "SUI": ["#D52B1E", "#FFFFFF"], "BRA": ["#FFDC00", "#009C3B"],
    "MAR": ["#C1272D", "#006233"], "HAI": ["#00209F", "#FFFFFF"], "SCO": ["#0B1C45", "#FFFFFF"],
    "USA": ["#FFFFFF", "#0A3161"], "PAR": ["#D52B1E", "#FFFFFF"], "AUS": ["#FFCD00", "#00843D"],
    "TUR": ["#E30A17", "#FFFFFF"], "GER": ["#FFFFFF", "#000000"], "CUW": ["#002B7F", "#F9E814"],
    "CIV": ["#FF8200", "#FFFFFF"], "ECU": ["#FFDD00", "#003DA5"], "NED": ["#F36C21", "#FFFFFF"],
    "JPN": ["#003DA5", "#FFFFFF"], "SWE": ["#FECC02", "#005293"], "TUN": ["#E70013", "#FFFFFF"],
    "BEL": ["#E30613", "#FFFFFF"], "EGY": ["#CE1126", "#FFFFFF"], "IRN": ["#FFFFFF", "#DA0000"],
    "NZL": ["#FFFFFF", "#000000"], "ESP": ["#C60B1E", "#FFC400"], "CPV": ["#003893", "#FFFFFF"],
    "KSA": ["#FFFFFF", "#006C35"], "URU": ["#5CB8E6", "#0A3161"], "FRA": ["#21304B", "#FFFFFF"],
    "SEN": ["#FFFFFF", "#00853F"], "IRQ": ["#007A3D", "#FFFFFF"], "NOR": ["#EF2B2D", "#002868"],
    "ARG": ["#75AADB", "#1A1A1A"], "ALG": ["#FFFFFF", "#006233"], "AUT": ["#ED2939", "#FFFFFF"],
    "JOR": ["#CE1126", "#FFFFFF"], "POR": ["#A50021", "#FFD700"], "COD": ["#007FFF", "#CE1021"],
    "UZB": ["#FFFFFF", "#0099B5"], "COL": ["#FCD116", "#003893"], "ENG": ["#FFFFFF", "#0A3161"],
    "CRO": ["#FFFFFF", "#E63946"], "GHA": ["#FFFFFF", "#1A1A1A"], "PAN": ["#DA121A", "#FFFFFF"],
}

# FIFA-Ranglistenpunkte (approximiert, Stand Anfang 2026) für die Simulation
STRENGTH = {
    "ESP": 1880, "ARG": 1870, "FRA": 1860, "ENG": 1815, "BRA": 1780,
    "POR": 1770, "NED": 1755, "BEL": 1735, "GER": 1720, "CRO": 1705,
    "MAR": 1695, "URU": 1675, "COL": 1670, "USA": 1665, "MEX": 1655,
    "SUI": 1648, "JPN": 1640, "SEN": 1625, "IRN": 1615, "KOR": 1590,
    "ECU": 1588, "AUT": 1575, "AUS": 1565, "NOR": 1560, "TUR": 1552,
    "CAN": 1548, "ALG": 1520, "EGY": 1512, "CZE": 1502, "SWE": 1500,
    "TUN": 1495, "CIV": 1490, "SCO": 1483, "PAR": 1478, "UZB": 1452,
    "QAT": 1442, "KSA": 1438, "RSA": 1435, "COD": 1395, "JOR": 1389,
    "BIH": 1385, "PAN": 1378, "GHA": 1370, "IRQ": 1352, "CPV": 1330,
    "NZL": 1303, "CUW": 1312, "HAI": 1290,
}

# ─── SVG-Karte bauen ─────────────────────────────────────────────────────
def build_map_svg():
    usa_pts = poly_points(USA)
    mex_pts = poly_points(MEXICO)
    can_pts = poly_points(CANADA)
    lakes_svg = "".join(
        f'<polygon points="{poly_points(coords)}" fill="#fafbfc" stroke="#C8D8E8" stroke-width="1"/>'
        for coords in LAKES.values()
    )
    # Stadien-Punkte
    dots = []
    colors = {"USA": "#1F4E78", "MEX": "#0E9F6E", "CAN": "#DC2626"}
    for sid, s in STADIONS.items():
        x, y = project(s["lng"], s["lat"])
        c = colors[s["land"]]
        dots.append(
            f'<circle class="stadion-dot" cx="{x}" cy="{y}" r="9" fill="{c}" stroke="white" '
            f'stroke-width="2.5" data-sid="{sid}"/>'
        )
    # Länderbeschriftungen
    labels = (
        '<text x="430" y="300" class="land-label">USA</text>'
        '<text x="380" y="560" class="land-label">MEXIKO</text>'
        '<text x="490" y="70" class="land-label">KANADA</text>'
    )
    return f'''<svg viewBox="0 0 1000 640" xmlns="http://www.w3.org/2000/svg" id="na-map">
  <polygon points="{can_pts}" fill="#FBE9E9" stroke="#E3B9B9" stroke-width="1.5"/>
  <polygon points="{usa_pts}" fill="#E4EDF6" stroke="#A9C2DA" stroke-width="1.5"/>
  <polygon points="{mex_pts}" fill="#E2F4EC" stroke="#A7D8C2" stroke-width="1.5"/>
  {lakes_svg}
  {labels}
  {dots and "".join(dots)}
</svg>'''

MAP_SVG = build_map_svg()

# ─── JS-Daten ────────────────────────────────────────────────────────────
teams_js = {c: {"name": n, "flag": f, "konf": k, "gruppe": g,
                "landWiki": LAND_WIKI[c], "verbandWiki": VERBAND_WIKI[c]}
            for c, (n, f, k, g) in TEAMS.items()}
matches_js = [{"id": m[0], "datum": m[1], "uhrzeit": m[2],
               "heim": m[3], "gast": m[4], "stadion": m[5], "spieltag": m[6]}
              for m in MATCHES_GROUP]
stadions_js = {k: {**v, "wiki": STADION_WIKI[k]} for k, v in STADIONS.items()}

# ═══ HTML-TEMPLATE ═══════════════════════════════════════════════════════
HTML = r"""<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>WM 2026 — interaktiver Spielplan</title>
<style>
:root {
  --hkv-blue: #1F4E78; --hkv-light: #EAF1F8; --fifa-purple: #8B5CF6;
  --bg: #fafbfc; --text: #1a1a1a; --muted: #6b7280; --border: #e5e7eb;
  --live-red: #DC2626; --real-green: #059669;
}
* { box-sizing: border-box; }
body { margin: 0; font-family: 'Aptos', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: var(--bg); color: var(--text); line-height: 1.5; }
.container { max-width: 1500px; margin: 0 auto; padding: 16px; }

header { background: linear-gradient(135deg, var(--hkv-blue) 0%, var(--fifa-purple) 100%);
  color: white; padding: 18px 22px; border-radius: 12px; margin-bottom: 14px;
  display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; }
header h1 { margin: 0; font-size: 22px; font-weight: 700; }
header .subtitle { font-size: 12px; opacity: 0.9; margin-top: 2px; }
.header-controls { display: flex; align-items: center; gap: 14px; flex-wrap: wrap; }
.live-toggle { display: flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.15);
  padding: 8px 14px; border-radius: 8px; cursor: pointer; user-select: none;
  border: 1px solid rgba(255,255,255,0.25); font-size: 13px; font-weight: 600; }
.live-toggle .switch { width: 38px; height: 20px; background: rgba(255,255,255,0.3);
  border-radius: 10px; position: relative; transition: background 0.2s; }
.live-toggle .switch::after { content: ''; position: absolute; width: 16px; height: 16px;
  background: white; border-radius: 50%; top: 2px; left: 2px; transition: left 0.2s; }
.live-toggle.on .switch { background: #10B981; }
.live-toggle.on .switch::after { left: 20px; }
.live-status { font-size: 11px; opacity: 0.85; }
header .reset { background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.3);
  color: white; padding: 7px 14px; border-radius: 6px; cursor: pointer; font-size: 12px; }
header .reset:hover { background: rgba(255,255,255,0.3); }

.tabs { display: flex; gap: 4px; margin-bottom: 14px; background: white; padding: 4px;
  border-radius: 10px; border: 1px solid var(--border); flex-wrap: wrap; }
.tab { flex: 1; min-width: 120px; padding: 9px 14px; border: none; background: transparent;
  cursor: pointer; font-size: 13px; font-weight: 500; color: var(--muted); border-radius: 6px; }
.tab:hover { background: var(--hkv-light); }
.tab.active { background: var(--hkv-blue); color: white; }
.tab-content { display: none; }
.tab-content.active { display: block; }

/* ── TEAM VERFOLGEN (⭐) ── */
.follow-select { padding: 7px 10px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.35);
  background: rgba(255,255,255,0.15); color: white; font-size: 12px; font-weight: 600; cursor: pointer; }
.follow-select option { color: #1a1a1a; }
.followed-row td { background: #FEF9C3 !important; }
.followed-row td:first-child { border-left: 3px solid #EAB308 !important; }
.followed-row .team-name { font-weight: 700; }
.match.followed { outline: 2px solid #EAB308; background: #FEFCE8; }
.bk-team.followed { background: #FEF9C3 !important; box-shadow: inset 0 0 0 2px #EAB308;
  border-radius: 4px; font-weight: 700; }
.group-card.followed { border: 2px solid #EAB308; box-shadow: 0 0 0 3px rgba(234,179,8,0.18); }

.team-flag-link, .team-name-link { cursor: pointer; text-decoration: none; color: inherit; }
.team-name-link:hover { text-decoration: underline; color: var(--hkv-blue); }

/* ── GRUPPEN ── */
.groups-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(380px, 1fr)); gap: 14px; }
.group-card { background: white; border: 1px solid var(--border); border-radius: 10px; padding: 13px; }
.group-header { font-weight: 700; font-size: 15px; color: var(--hkv-blue);
  margin-bottom: 9px; padding-bottom: 7px; border-bottom: 2px solid var(--hkv-light); }
.group-table { width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 11px; }
.group-table th { text-align: left; padding: 3px 5px; font-weight: 600; color: var(--muted);
  font-size: 10px; text-transform: uppercase; }
.group-table th.num { text-align: center; width: 26px; }
.group-table td { padding: 5px; border-top: 1px solid var(--border); }
.group-table td.num { text-align: center; font-variant-numeric: tabular-nums; }
.group-table tr.qualified td { background: #ECFDF5; }
.group-table tr.qualified td:first-child { border-left: 3px solid #10B981; }
.group-table tr.third-pos td { background: #FEF3C7; }
.group-table tr.third-pos td:first-child { border-left: 3px solid #F59E0B; }
.team-cell { display: flex; align-items: center; gap: 5px; }
.team-flag { font-size: 15px; }
.team-name { font-size: 13px; font-weight: 500; }

.match-list { display: flex; flex-direction: column; gap: 5px; }
.match { display: grid; grid-template-columns: 1fr auto 1fr; gap: 8px; align-items: center;
  padding: 6px 8px; background: #f9fafb; border-radius: 6px; font-size: 13px; }
.match .home { text-align: right; }
.match .away { text-align: left; }
.match .vs { display: flex; align-items: center; gap: 4px; font-weight: 600; color: var(--muted); }
.match .score-input { width: 30px; height: 23px; border: 1px solid var(--border); border-radius: 4px;
  text-align: center; font-size: 13px; font-weight: 600; background: white; }
.match .score-input:focus { outline: 2px solid var(--hkv-blue); outline-offset: -1px; }
.match .score-input:disabled { background: #D1FAE5; color: var(--real-green); border-color: #6EE7B7; font-weight: 700; }
.match.has-tip { background: #EFF6FF; }
.match.is-real { background: #ECFDF5; }
.match.is-live { background: #FEF2F2; border: 1px solid #FECACA; animation: livepulse 1.6s ease-in-out infinite; }
@keyframes livepulse { 0%,100% { box-shadow: 0 0 0 0 rgba(220,38,38,0.35);} 50% { box-shadow: 0 0 0 5px rgba(220,38,38,0);} }
.live-badge { display: inline-block; background: var(--live-red); color: white; font-size: 9px;
  font-weight: 700; padding: 1px 6px; border-radius: 4px; animation: blink 1.2s step-start infinite; }
@keyframes blink { 50% { opacity: 0.35; } }
.match .meta { font-size: 10px; color: var(--muted); text-align: center; grid-column: 1 / -1; margin-top: 2px; }
.goals-line { grid-column: 1 / -1; font-size: 10px; color: var(--muted); text-align: center; margin-top: 1px; }

/* ── BRACKET ── */
.bracket-wrap { overflow-x: auto; padding-bottom: 10px; }
.bracket { display: grid; grid-template-columns: repeat(9, minmax(150px, 1fr)); gap: 8px; min-width: 1420px; }
.bracket-col { display: flex; flex-direction: column; justify-content: space-around; gap: 8px; }
.bracket-col h4 { font-size: 10px; text-transform: uppercase; letter-spacing: 0.4px;
  color: var(--muted); margin: 0 0 4px; text-align: center; }
.bk-match { background: white; border: 1px solid var(--border); border-radius: 7px;
  padding: 5px; font-size: 11.5px; }
.bk-match.final { border: 2px solid #FFD700; box-shadow: 0 2px 8px rgba(255,215,0,0.3); }
.bk-team { padding: 4px 5px; display: flex; justify-content: space-between; align-items: center;
  border-radius: 4px; cursor: pointer; }
.bk-team:hover { background: var(--hkv-light); }
.bk-team.winner { background: #ECFDF5; font-weight: 700; }
.bk-team.tbd { color: var(--muted); font-style: italic; cursor: default; font-size: 10.5px; }
.bk-team .nm { display: flex; align-items: center; gap: 4px; overflow: hidden; white-space: nowrap; }
.bk-info { font-size: 9px; color: var(--muted); text-align: center; margin-top: 2px; }
.champion-box { text-align: center; padding: 8px; background: linear-gradient(135deg, #FFF7DB, #FFE9A8);
  border: 2px solid #FFD700; border-radius: 8px; margin-top: 8px; font-weight: 700; font-size: 13px; }

/* ── SPIELPLAN ── */
.day-section { background: white; border: 1px solid var(--border); border-radius: 10px;
  padding: 13px; margin-bottom: 11px; }
.day-header { font-weight: 700; color: var(--hkv-blue); margin-bottom: 9px; font-size: 14px; }
.day-header.today { color: var(--live-red); }
.day-matches { display: flex; flex-direction: column; gap: 5px; }

/* ── SVG-KARTE ── */
.map-card { background: white; border: 1px solid var(--border); border-radius: 10px;
  padding: 14px; max-width: 640px; margin: 0 auto; }
#na-map { width: 100%; height: auto; display: block; }
.land-label { font-size: 26px; font-weight: 800; fill: rgba(31,78,120,0.25);
  letter-spacing: 3px; font-family: inherit; pointer-events: none; }
.stadion-dot { cursor: pointer; transition: r 0.15s; }
.stadion-dot:hover { r: 13; }
.map-legend { display: flex; gap: 16px; margin-top: 10px; font-size: 13px; flex-wrap: wrap; }
.map-legend span { display: flex; align-items: center; gap: 6px; }
.dot { width: 12px; height: 12px; border-radius: 50%; display: inline-block; }
#stadion-panel { margin-top: 12px; padding: 14px; background: var(--hkv-light);
  border: 1px solid #BFD4E8; border-radius: 8px; display: none; }
#stadion-panel.show { display: block; }
#stadion-panel .pname { font-weight: 700; color: var(--hkv-blue); font-size: 16px; }
#stadion-panel .pmeta { font-size: 13px; color: var(--muted); margin: 4px 0 10px; }
#stadion-panel .pbtn { display: inline-block; padding: 7px 14px; border-radius: 6px;
  font-size: 13px; font-weight: 600; text-decoration: none; margin-right: 8px; }
#stadion-panel .pbtn.wiki { background: var(--hkv-blue); color: white; }
#stadion-panel .pbtn.maps { background: white; color: var(--hkv-blue); border: 1px solid var(--hkv-blue); }
.map-tooltip { position: fixed; background: rgba(20,20,30,0.92); color: white;
  padding: 6px 10px; border-radius: 6px; font-size: 12px; pointer-events: none;
  z-index: 3000; display: none; white-space: nowrap; text-align: center; }
.map-tooltip img { width: 58px; height: 58px; object-fit: cover; border-radius: 6px;
  display: block; margin: 5px auto 0; background: #2a2a35; }

/* ── TORSCHÜTZEN ── */
.scorer-card { background: white; border: 1px solid var(--border); border-radius: 10px;
  padding: 14px; max-width: 700px; margin: 0 auto; }
.scorer-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.scorer-table th { text-align: left; padding: 6px 8px; font-weight: 600; color: var(--muted);
  font-size: 10px; text-transform: uppercase; border-bottom: 2px solid var(--hkv-light); }
.scorer-table th.num, .scorer-table td.num { text-align: center; }
.scorer-table td { padding: 7px 8px; border-bottom: 1px solid var(--border); }
.scorer-table tr:nth-child(-n+3) td { background: #FFFBEB; }
.scorer-table .rank { font-weight: 700; color: var(--hkv-blue); width: 36px; }
.scorer-table .player { font-weight: 600; }
.scorer-table .goals-num { font-weight: 700; font-size: 15px; color: var(--hkv-blue); }

footer { margin-top: 22px; padding: 14px; text-align: center; color: var(--muted);
  font-size: 12px; border-top: 1px solid var(--border); }

/* ── MODAL (Kader & Spiel-Details) ── */
#modal-overlay { display: none; position: fixed; inset: 0; background: rgba(15,23,42,0.55);
  z-index: 2000; padding: 20px; overflow-y: auto; }
#modal-overlay.show { display: flex; align-items: flex-start; justify-content: center; }
.modal-box { background: white; border-radius: 12px; max-width: 780px; width: 100%;
  padding: 18px; margin-top: 30px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }
.modal-head { display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 12px; padding-bottom: 10px; border-bottom: 2px solid var(--hkv-light); }
.modal-head h3 { margin: 0; color: var(--hkv-blue); font-size: 17px; }
.modal-close { border: none; background: var(--hkv-light); color: var(--hkv-blue);
  width: 30px; height: 30px; border-radius: 6px; cursor: pointer; font-size: 15px; font-weight: 700; }
.modal-close:hover { background: #d3e2f0; }
.roster-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0 16px; }
@media (max-width: 560px) { .roster-grid { grid-template-columns: 1fr; } }
.roster-table { width: 100%; border-collapse: collapse; font-size: 11.5px; }
.roster-table th { text-align: left; padding: 3px 5px; font-size: 9px; text-transform: uppercase;
  color: var(--muted); border-bottom: 2px solid var(--hkv-light); }
.roster-table td { padding: 3px 5px; border-bottom: 1px solid var(--border); }
.roster-table .jersey { font-weight: 700; color: var(--hkv-blue); width: 26px; text-align: center; }
.roster-table .pos-abbr { width: 22px; text-align: center; color: var(--muted); }
.roster-table a { color: inherit; text-decoration: none; }
.roster-table a:hover { color: var(--hkv-blue); text-decoration: underline; }
.lineup-cols { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.lineup-col { min-width: 0; text-align: center; }
.lineup-col h4 { margin: 0 0 6px; font-size: 14px; color: var(--hkv-blue); }
.pitch-svg { width: 100%; max-width: 235px; height: auto; border-radius: 10px;
  display: block; margin: 0 auto; box-shadow: 0 2px 8px rgba(0,0,0,0.15); }
.formation-badge { display: inline-block; background: var(--hkv-blue); color: white;
  padding: 2px 10px; border-radius: 12px; font-size: 12px; font-weight: 700; margin-left: 6px; }
.lineup-list { font-size: 12.5px; line-height: 1.8; }
.lineup-list .pos { display: inline-block; width: 22px; color: var(--muted); font-size: 10px; }
.lineup-list .nr { display: inline-block; width: 24px; font-weight: 700; color: var(--hkv-blue); }
.bench-title { font-size: 10px; text-transform: uppercase; color: var(--muted); margin-top: 8px; }
.bench-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2px 8px;
  font-size: 10.5px; text-align: left; opacity: 0.8; max-width: 235px; margin: 4px auto 0; }
.bench-grid span { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.bench-grid .nr { font-weight: 700; color: var(--hkv-blue); margin-right: 3px; }
.kader-btn { border: none; background: transparent; cursor: pointer; font-size: 12px;
  padding: 0 2px; opacity: 0.55; }
.kader-btn:hover { opacity: 1; }
.modal-hint { background: #FEF3C7; border: 1px solid #FDE68A; border-radius: 8px;
  padding: 10px; font-size: 13px; margin-bottom: 12px; }
.modal-loading { text-align: center; color: var(--muted); padding: 24px; font-size: 13px; }
@media (max-width: 600px) { .lineup-cols { grid-template-columns: 1fr; } }

@media (max-width: 600px) {
  .groups-grid { grid-template-columns: 1fr; }
  header h1 { font-size: 17px; }
}
</style>
</head>
<body>
<div class="container">

<header>
  <div>
    <h1>⚽ WM 2026 — interaktiver Spielplan</h1>
    <div class="subtitle">11. Juni – 19. Juli 2026 · USA · Kanada · Mexiko · 48 Teams · 104 Spiele</div>
  </div>
  <div class="header-controls">
    <select id="follow-select" class="follow-select" onchange="setFollow(this.value)">
      <option value="">⭐ Team verfolgen…</option>
    </select>
    <div class="live-toggle" id="live-toggle" onclick="toggleLive()">
      <div class="switch"></div>
      <span>Echte Resultate in Tipps</span>
    </div>
    <span class="live-status" id="live-status">lädt…</span>
    <button class="reset" onclick="simulateAll()" title="Realistische Zufallsresultate nach FIFA-Rangliste — inkl. KO-Baum bis zum Weltmeister">🎲 Simulieren</button>
    <button class="reset" onclick="resetAllTips()">↻ Tipps zurücksetzen</button>
  </div>
</header>

<div class="tabs">
  <button class="tab active" data-tab="groups">12 Gruppen + Tipps</button>
  <button class="tab" data-tab="ko">KO-Baum</button>
  <button class="tab" data-tab="schedule">Spielplan live 🔴</button>
  <button class="tab" data-tab="scorers">⚽ Torschützen</button>
  <button class="tab" data-tab="map">Stadien-Karte</button>
</div>

<div class="tab-content active" id="tab-groups">
  <div style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:8px;padding:11px;margin-bottom:14px;font-size:13px;">
    💡 <strong>Tippen:</strong> Resultat eingeben → Tabelle aktualisiert sich. Grün = Top 2, Gelb = unter den 8 besten Dritten.
    Schalter <strong>«Echte Resultate in Tipps»</strong>: gespielte Partien werden mit dem echten Resultat fixiert (grün) —
    offene Spiele tippst du weiter: «Was wäre wenn» ab dem echten Stand.
    🔗 Flagge = Land · Teamname = Fussballverband (Wikipedia).
  </div>
  <div class="groups-grid" id="groups-grid"></div>
</div>

<div class="tab-content" id="tab-ko">
  <div style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:8px;padding:11px;margin-bottom:14px;font-size:13px;">
    🏆 Offizieller FIFA-Turnierbaum: links und rechts je 8 Sechzehntelfinals, das Finale in der Mitte.
    Teams erscheinen automatisch aus der Gruppenphase. <strong>Klicke auf ein Team, um es als Sieger weiterzuschicken.</strong>
    <br>📍 <strong>Die Position eines Teams hängt von seinem Gruppenrang ab</strong> — z.B. spielt der Sieger der Gruppe B (1B)
    unten rechts, der Gruppenzweite (2B) oben links. Ändert sich der Tabellenstand, wandert das Team im Baum.
  </div>
  <div class="bracket-wrap"><div class="bracket" id="bracket"></div></div>
</div>

<div class="tab-content" id="tab-schedule">
  <div style="background:#FEF2F2;border:1px solid #FECACA;border-radius:8px;padding:11px;margin-bottom:14px;font-size:13px;">
    🔴 <strong>Immer live:</strong> Diese Ansicht zeigt automatisch die echten Resultate und aktualisiert sich jede Minute —
    unabhängig vom Schalter oben. Laufende Spiele blinken rot mit ungefährer Spielminute, Torschützen werden angezeigt.
  </div>
  <div id="schedule-list"></div>
</div>

<div class="tab-content" id="tab-scorers">
  <div class="scorer-card">
    <div style="background:#EFF6FF;border:1px solid #BFDBFE;border-radius:8px;padding:11px;margin-bottom:14px;font-size:13px;">
      ⚽ <strong>Torschützenliste</strong> — aggregiert live aus allen gespielten Partien, Aktualisierung jede Minute.
      Elfmetertore sind mit (P) gekennzeichnet, Eigentore zählen nicht.
    </div>
    <div id="scorer-list"></div>
    <details style="margin-top:14px;font-size:12px;color:var(--muted);">
      <summary style="cursor:pointer;">🔧 Datenquellen-Diagnose</summary>
      <div id="scorer-diag" style="padding:8px 4px;line-height:1.7;"></div>
    </details>
  </div>
</div>

<div class="tab-content" id="tab-map">
  <div class="map-card">
    __MAP_SVG__
    <div class="map-legend">
      <span><span class="dot" style="background:#1F4E78"></span> USA (11 Stadien)</span>
      <span><span class="dot" style="background:#0E9F6E"></span> Mexiko (3 Stadien)</span>
      <span><span class="dot" style="background:#DC2626"></span> Kanada (2 Stadien)</span>
      <span style="color:var(--muted)">Klick auf Punkt → Details & Spiele · ⭐ Goldring = Spielort des verfolgten Teams</span>
    </div>
    <div id="stadion-panel"></div>
  </div>
</div>

<footer>
  © 2026 S. Mollet · HKV Aarau · realisiert mit Claude (Anthropic) · Datenquellen: FIFA, UEFA, Wikipedia, OpenLigaDB, TheSportsDB, ESPN
</footer>

</div>
<div id="modal-overlay" onclick="if(event.target===this)closeModal()">
  <div class="modal-box">
    <div class="modal-head">
      <h3 id="modal-title">…</h3>
      <button class="modal-close" onclick="closeModal()">✕</button>
    </div>
    <div id="modal-body"></div>
  </div>
</div>
<div class="map-tooltip" id="map-tooltip"></div>

<script>
// ═══ DATEN ═══
const TEAMS = __TEAMS__;
const MATCHES = __MATCHES__;
const STADIONS = __STADIONS__;
const GROUPS = __GROUPS__;
const R32 = __R32__;
const OLDB_ALIAS = __ALIAS__;
const STRENGTH = __STRENGTH__;
const JERSEY = __JERSEY__;

// ═══ STATE ═══
let tips = {};
let koPicks = {};
let liveInTips = false;   // Kippschalter: echte Resultate in Tipp-Tabellen
let liveResults = {};     // immer befüllt (Spielplan nutzt es immer)
let liveSchedule = {};    // echte Anstosszeiten aus OpenLigaDB (auch für künftige Spiele)
let scorerStats = {};     // Spielername → {goals, pens, team}
let scorerCovered = {};   // Spiel-Key → true, wenn Schützen bereits aus einer Quelle gezählt
let diag = { oldb: '–', oldbGames: 0, oldbGoals: 0, oldbNamed: 0,
             tsdb: '–', tsdbEvents: 0, tsdbScored: 0, tsdbDetails: 0, lookups: 0,
             unmatched: [] };
let espnTeamIds = {};     // Teamcode → ESPN-Team-ID (für Kader-Abruf)
let espnEventByKey = {};  // minKey → {id, dateIso} (für Aufstellungs-Abruf)
let rosterCache = {};     // Teamcode → Roster-Daten
let summaryCache = {};    // eventId → Summary-Daten
let followTeam = null;    // ⭐ hervorgehobenes Team
let oldbShortcut = null;

try {
  followTeam = localStorage.getItem('wm2026_follow') || null;
} catch (e) {}

function setFollow(code) {
  followTeam = code || null;
  try { localStorage.setItem('wm2026_follow', followTeam || ''); } catch (e) {}
  renderAll();
  updateMapHighlights();
}

function updateMapHighlights() {
  document.querySelectorAll('.stadion-dot').forEach(dot => {
    const sid = dot.dataset.sid;
    const has = followTeam && MATCHES.some(m =>
      m.stadion === sid && (m.heim === followTeam || m.gast === followTeam));
    dot.setAttribute('stroke', has ? '#EAB308' : 'white');
    dot.setAttribute('stroke-width', has ? '4.5' : '2.5');
  });
}

try {
  tips = JSON.parse(localStorage.getItem('wm2026_tips') || '{}');
  koPicks = JSON.parse(localStorage.getItem('wm2026_kopicks') || '{}');
  liveInTips = localStorage.getItem('wm2026_liveintips') === '1';
} catch (e) {}

function persist() {
  try {
    localStorage.setItem('wm2026_tips', JSON.stringify(tips));
    localStorage.setItem('wm2026_kopicks', JSON.stringify(koPicks));
    localStorage.setItem('wm2026_liveintips', liveInTips ? '1' : '0');
  } catch (e) {}
}

function resetAllTips() {
  if (!confirm('Alle Tipps & KO-Auswahlen zurücksetzen? (Echte Resultate bleiben)')) return;
  tips = {}; koPicks = {};
  persist(); renderAll();
}

// ═══ 🎲 SIMULATION (FIFA-Rangliste, Poisson-Modell) ═══
function poisson(lambda) {
  const L = Math.exp(-lambda);
  let k = 0, p = 1;
  do { k++; p *= Math.random(); } while (p > L);
  return k - 1;
}
function simScore(codeA, codeB) {
  const ra = STRENGTH[codeA] || 1450, rb = STRENGTH[codeB] || 1450;
  let d = (ra - rb) / 400;
  d = Math.max(-1.1, Math.min(1.1, d));
  const la = Math.max(0.25, 1.30 + 0.95 * d);
  const lb = Math.max(0.25, 1.30 - 0.95 * d);
  return [Math.min(7, poisson(la)), Math.min(7, poisson(lb))];
}
function eloWin(codeA, codeB) {
  const ra = STRENGTH[codeA] || 1450, rb = STRENGTH[codeB] || 1450;
  const p = 1 / (1 + Math.pow(10, (rb - ra) / 400));
  return Math.random() < p ? codeA : codeB;
}

function simulateAll() {
  if (Object.keys(tips).length > 0 || Object.keys(koPicks).length > 0) {
    if (!confirm('Bestehende Tipps mit Zufallsresultaten überschreiben?')) return;
  }
  // 1) Gruppenspiele: alle ohne echtes fixiertes Resultat
  MATCHES.forEach(m => {
    if (liveInTips) {
      const lr = liveResults[liveKey(m)];
      if (lr && lr.home !== null && lr.finished) return;  // echtes Resultat bleibt
    }
    const [h, a] = simScore(m.heim, m.gast);
    tips[m.id] = { home: h, away: a };
  });
  // 2) KO-Baum komplett durchwürfeln
  koPicks = {};
  const r32 = computeR32();
  r32.forEach(m => {
    if (m.teamA && m.teamB) koPicks[m.id] = eloWin(m.teamA, m.teamB);
  });
  const pairs = {
    af_1: ['r32_1','r32_2'], af_2: ['r32_3','r32_4'], af_3: ['r32_5','r32_6'], af_4: ['r32_7','r32_8'],
    af_5: ['r32_9','r32_10'], af_6: ['r32_11','r32_12'], af_7: ['r32_13','r32_14'], af_8: ['r32_15','r32_16'],
    vf_1: ['af_1','af_2'], vf_2: ['af_3','af_4'], vf_3: ['af_5','af_6'], vf_4: ['af_7','af_8'],
    hf_1: ['vf_1','vf_2'], hf_2: ['vf_3','vf_4'],
    final: ['hf_1','hf_2'],
  };
  Object.entries(pairs).forEach(([id, [p1, p2]]) => {
    const a = koPicks[p1], b = koPicks[p2];
    if (a && b) koPicks[id] = eloWin(a, b);
  });
  persist(); renderAll();
  // Weltmeister kurz feiern
  const champ = koPicks['final'];
  if (champ) {
    document.getElementById('live-status').textContent =
      '🎲 Simulation: ' + TEAMS[champ].flag + ' ' + TEAMS[champ].name + ' wird Weltmeister!';
  }
}

function toggleLive() {
  liveInTips = !liveInTips;
  document.getElementById('live-toggle').classList.toggle('on', liveInTips);
  persist(); renderAll();
}

// ═══ EFFEKTIVES RESULTAT ═══
function liveKey(m) { return m.heim + '_' + m.gast; }
function getResult(m, forceLive) {
  const useLive = forceLive || liveInTips;
  if (useLive) {
    const lr = liveResults[liveKey(m)];
    if (lr && lr.home !== null) return { ...lr, real: true };
  }
  const t = tips[m.id];
  if (t && t.home !== null && t.home !== undefined && t.away !== null && t.away !== undefined && t.home !== '' && t.away !== '')
    return { home: t.home, away: t.away, real: false, live: false, finished: false, goals: [], hz: null, kickoff: null };
  return null;
}

// ═══ LIVE: OpenLigaDB (läuft IMMER) ═══
async function fetchLive() {
  let srcs = [];
  scorerStats = {};    // frisch aggregieren über beide Quellen
  scorerCovered = {};
  diag = { oldb: 'nicht erreichbar', oldbGames: 0, oldbGoals: 0, oldbNamed: 0,
           tsdb: 'nicht erreichbar', tsdbEvents: 0, tsdbScored: 0, tsdbDetails: 0,
           lookups: 0, espn: 'nicht abgefragt', espnGoals: 0,
           unmatched: diag.unmatched || [] };
  // Quelle 1: OpenLigaDB (Shortcut 'wm26') — liefert Live-Stände & Torschützen
  const base = oldbShortcut ? [oldbShortcut] : ['wm26', 'wm2026', 'WM26', 'wm'];
  const candidates = [];
  base.forEach(sc => { candidates.push(sc + '/2026'); candidates.push(sc); });
  for (const path of candidates) {
    try {
      const r = await fetch('https://api.openligadb.de/getmatchdata/' + path);
      if (!r.ok) continue;
      const data = await r.json();
      if (!Array.isArray(data) || data.length === 0) continue;
      oldbShortcut = path;
      diag.oldb = path + ' (' + data.length + ' Spiele)';
      parseLive(data);
      srcs.push('OpenLigaDB');
      break;
    } catch (e) {}
  }
  // Quelle 2: TheSportsDB — Saison-Varianten + letzte gespielte Partien
  const needDetails = [];
  for (const season of ['2026', '2025-2026']) {
    try {
      const r2 = await fetch('https://www.thesportsdb.com/api/v1/json/3/eventsseason.php?id=4429&s=' + season);
      if (!r2.ok) continue;
      const j = await r2.json();
      if (j && Array.isArray(j.events) && j.events.length) {
        diag.tsdb = 'Saison ' + season + ' (' + j.events.length + ' Events)';
        parseTSDB(j.events, needDetails);
        srcs.push('TheSportsDB');
        break;
      }
    } catch (e) {}
  }
  // Zusätzlich: die letzten 15 gespielten Partien (immer aktuell, ohne Saison-Raterei)
  try {
    const r3 = await fetch('https://www.thesportsdb.com/api/v1/json/3/eventspastleague.php?id=4429');
    if (r3.ok) {
      const j3 = await r3.json();
      if (j3 && Array.isArray(j3.events) && j3.events.length) {
        parseTSDB(j3.events, needDetails);
        if (!srcs.includes('TheSportsDB')) { srcs.push('TheSportsDB'); diag.tsdb = 'pastleague (' + j3.events.length + ')'; }
      }
    }
  } catch (e) {}
  // Detail-Nachladung: für gespielte Partien ohne Schützen einzeln nachschlagen (max 8)
  for (const ev of needDetails.slice(0, 8)) {
    if (scorerCovered[ev.minKey]) continue;
    try {
      const r4 = await fetch('https://www.thesportsdb.com/api/v1/json/3/lookupevent.php?id=' + ev.id);
      if (!r4.ok) continue;
      const j4 = await r4.json();
      const e4 = j4 && j4.events && j4.events[0];
      if (!e4) continue;
      diag.lookups++;
      const n = parseGoalDetails(e4.strHomeGoalDetails, ev.c1) +
                parseGoalDetails(e4.strAwayGoalDetails, ev.c2);
      if (n > 0) { scorerCovered[ev.minKey] = true; diag.tsdbDetails += n; }
    } catch (e) {}
  }
  // Quelle 3: ESPN — zuverlässige Torschützen (live gepflegt)
  // Nur Tage abfragen, an denen Tore gefallen sind, deren Schützen noch fehlen — plus heute
  const espnDays = new Set();
  const todayIso = new Date().toLocaleDateString('sv-SE');
  espnDays.add(todayIso.replace(/-/g, ''));
  MATCHES.forEach(m => {
    const r = liveResults[liveKey(m)];
    if (!r || r.home === null) return;
    if ((r.home + r.away) === 0) return;
    const minKey = [m.heim, m.gast].sort().join('_');
    if (scorerCovered[minKey]) return;
    const lk = liveSchedule[liveKey(m)];
    const d = lk ? new Date(lk).toLocaleDateString('sv-SE') : m.datum;
    espnDays.add(d.replace(/-/g, ''));
  });
  let espnOk = false;
  for (const day of Array.from(espnDays).slice(0, 6)) {
    try {
      const r5 = await fetch('https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard?dates=' + day);
      if (!r5.ok) continue;
      const j5 = await r5.json();
      if (j5 && Array.isArray(j5.events)) {
        parseESPN(j5.events);
        espnOk = true;
      }
    } catch (e) {}
  }
  diag.espn = espnOk ? (espnDays.size + ' Tag(e) abgefragt') : 'nicht erreichbar';
  if (espnOk && diag.espnGoals > 0 && !srcs.includes('ESPN')) srcs.push('ESPN');
  // Status
  if (srcs.length) {
    const fin = Object.values(liveResults).filter(r => r.finished).length / 2;
    const liv = Object.values(liveResults).filter(r => r.live).length / 2;
    document.getElementById('live-status').textContent =
      '✓ ' + fin + ' gespielt' + (liv ? ' · ' + liv + ' LIVE' : '') + ' · ' +
      srcs.join(' + ') + ' · ' +
      new Date().toLocaleTimeString('de-CH', {hour: '2-digit', minute: '2-digit'});
    return true;
  }
  document.getElementById('live-status').textContent = '⚠ Live-Quellen nicht erreichbar';
  return false;
}

// TheSportsDB-Events: Resultate, Anstosszeiten & Torschützen ergänzen (OpenLigaDB hat Vorrang)
function parseTSDB(events, needDetails) {
  events.forEach(e => {
    // Nur Endrunde (ab 11. Juni 2026) — Quali-Spiele derselben Liga ausschliessen
    if (!e.dateEvent || e.dateEvent < '2026-06-11') return;
    const c1 = codeFor(e.strHomeTeam);
    const c2 = codeFor(e.strAwayTeam);
    if (!c1 || !c2) return;
    diag.tsdbEvents++;
    const key = c1 + '_' + c2;
    // Anstosszeit (UTC) — nur wenn noch nicht bekannt
    if (e.dateEvent && !liveSchedule[key]) {
      const t = (e.strTime && e.strTime.length >= 5) ? e.strTime : '00:00:00';
      const k = new Date(e.dateEvent + 'T' + t + 'Z').getTime();
      if (k && !isNaN(k)) { liveSchedule[key] = k; liveSchedule[c2 + '_' + c1] = k; }
    }
    // Resultat — nur wenn OpenLigaDB nichts geliefert hat
    const hs = e.intHomeScore, as = e.intAwayScore;
    if (hs === null || hs === undefined || hs === '') return;
    diag.tsdbScored++;
    if (!liveResults[key] || liveResults[key].home === null) {
      const entry = { home: +hs, away: +as, finished: true, live: false,
                      goals: [], kickoff: liveSchedule[key] || null, hz: null };
      liveResults[key] = entry;
      liveResults[c2 + '_' + c1] = { ...entry, home: +as, away: +hs };
    }
    // Torschützen aus Goal-Details — nur wenn dieses Spiel noch nicht gezählt wurde
    const minKey = [c1, c2].sort().join('_');
    if (!scorerCovered[minKey]) {
      const n = parseGoalDetails(e.strHomeGoalDetails, c1) +
                parseGoalDetails(e.strAwayGoalDetails, c2);
      if (n > 0) { scorerCovered[minKey] = true; diag.tsdbDetails += n; }
      else if (needDetails && e.idEvent && (+hs + +as) > 0) {
        // Tore gefallen, aber keine Details im Listen-Endpoint → einzeln nachladen
        needDetails.push({ id: e.idEvent, c1, c2, minKey });
      }
    }
  });
}

// ESPN-Scoreboard: Torschützen (Hauptzweck) + Resultat-Backup
function parseESPN(events) {
  events.forEach(ev => {
    const comp = ev.competitions && ev.competitions[0];
    if (!comp || !Array.isArray(comp.competitors)) return;
    const home = comp.competitors.find(c => c.homeAway === 'home');
    const away = comp.competitors.find(c => c.homeAway === 'away');
    if (!home || !away) return;
    const c1 = codeFor(home.team && (home.team.displayName || home.team.name));
    const c2 = codeFor(away.team && (away.team.displayName || away.team.name));
    if (!c1 || !c2) return;
    const key = c1 + '_' + c2;
    const minKey = [c1, c2].sort().join('_');
    // ESPN-IDs für Kader & Aufstellungen merken
    if (home.team && home.team.id) espnTeamIds[c1] = home.team.id;
    if (away.team && away.team.id) espnTeamIds[c2] = away.team.id;
    if (ev.id) espnEventByKey[minKey] = { id: ev.id, dateIso: (ev.date || '').slice(0, 10) };
    // Resultat-Backup (nur wenn beide anderen Quellen nichts haben)
    const hs = parseInt(home.score, 10), as = parseInt(away.score, 10);
    const finished = !!(ev.status && ev.status.type && ev.status.type.completed);
    if (!isNaN(hs) && !isNaN(as) && (finished || (ev.status && ev.status.type && ev.status.type.state === 'in'))) {
      if (!liveResults[key] || liveResults[key].home === null) {
        const entry = { home: hs, away: as, finished, live: !finished,
                        goals: [], kickoff: liveSchedule[key] || null, hz: null };
        liveResults[key] = entry;
        liveResults[c2 + '_' + c1] = { ...entry, home: as, away: hs };
      }
    }
    // Torschützen aus details
    const details = comp.details || [];
    const matchGoals = [];
    const needScorers = !scorerCovered[minKey];
    let counted = 0;
    details.forEach(d => {
      const txt = (d.type && d.type.text) || '';
      const isGoal = d.scoringPlay === true || /goal/i.test(txt);
      if (!isGoal) return;
      if (/missed|shootout/i.test(txt)) return;          // verschossene Penaltys / Penaltyschiessen
      const ath = d.athletesInvolved && d.athletesInvolved[0];
      const name = ath && (ath.displayName || ath.fullName);
      if (!name) return;
      const teamId = d.team && d.team.id;
      const sideHome = !!(teamId && home.team && String(home.team.id) === String(teamId));
      const og = /own goal/i.test(txt);
      const pen = /penalty/i.test(txt);
      const min = parseInt((d.clock && d.clock.displayValue) || '', 10) || null;
      // Eigentor: Schütze gehört zum Gegner des begünstigten Teams
      matchGoals.push({ min, who: name, pen, og, side: (og ? !sideHome : sideHome) ? 'h' : 'a' });
      if (og || !needScorers) return;                    // Eigentore zählen nicht; keine Doppelzählung
      const team = sideHome ? c1 : c2;
      const e2 = scorerStats[name] || (scorerStats[name] = { goals: 0, pens: 0, team });
      e2.goals++;
      if (pen) e2.pens++;
      e2.team = team;
      counted++;
    });
    if (counted > 0) { scorerCovered[minKey] = true; diag.espnGoals += counted; }
    // Schützen-Namen in die Spiel-Einträge übernehmen, wenn dort keine Namen vorhanden
    if (matchGoals.length) {
      const cur = liveResults[key];
      if (cur && (!cur.goals.length || !cur.goals.some(g => g.who && String(g.who).trim()))) {
        cur.goals = matchGoals;
        const rev = liveResults[c2 + '_' + c1];
        if (rev) rev.goals = matchGoals.map(g => ({ ...g, side: g.side === 'h' ? 'a' : 'h' }));
      }
    }
  });
}

// Parst TSDB-Strings wie "34':J. Musiala;45'+2:K. Havertz (pen);" in scorerStats
function parseGoalDetails(s, team) {
  if (!s) return 0;
  let n = 0;
  s.split(';').forEach(part => {
    const t = part.trim();
    if (!t) return;
    if (/\bo\.?\s?g\b|own goal|eigentor/i.test(t)) return;  // Eigentore überspringen
    const pen = /\bpen|elfmeter|\(p\)/i.test(t);
    const name = t
      .replace(/\d+\s*'(?:\s*\+\s*\d+)?/g, '')   // Minuten-Angaben raus
      .replace(/\([^)]*\)/g, '')                  // Klammerzusätze raus
      .replace(/[:.]/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
    if (!name || name.length < 2) return;
    const e2 = scorerStats[name] || (scorerStats[name] = { goals: 0, pens: 0, team });
    e2.goals++;
    if (pen) e2.pens++;
    e2.team = team;
    n++;
  });
  return n;
}

function normName(s) {
  return (s || '').toLowerCase().replace(/[._]/g, ' ').replace(/\s+/g, ' ').trim();
}
function codeFor(teamName) {
  const n = normName(teamName);
  if (!n) return null;
  const n2 = n.replace(/-/g, ' ');  // "bosnia-herzegovina" → "bosnia herzegovina"
  if (OLDB_ALIAS[n]) return OLDB_ALIAS[n];
  if (OLDB_ALIAS[n2]) return OLDB_ALIAS[n2];
  for (const [alias, code] of Object.entries(OLDB_ALIAS)) {
    const a2 = alias.replace(/-/g, ' ');
    if (n.includes(alias) || alias.includes(n) || n2.includes(a2) || a2.includes(n2)) return code;
  }
  if (!diag.unmatched.includes(n) && diag.unmatched.length < 20) diag.unmatched.push(n);
  return null;
}

function parseLive(data) {
  const now = Date.now();
  data.forEach(m => {
    const c1 = codeFor(m.team1 && m.team1.teamName);
    const c2 = codeFor(m.team2 && m.team2.teamName);
    if (!c1 || !c2) return;
    // Torschützen aggregieren — Team-Zuordnung über Score-Verlauf
    const sorted = (m.goals || []).slice().sort((a, b) =>
      (a.matchMinute ?? 999) - (b.matchMinute ?? 999) || (a.goalID || 0) - (b.goalID || 0));
    let p1 = 0, p2 = 0, counted = 0;
    diag.oldbGames++;
    diag.oldbGoals += sorted.length;
    sorted.forEach(g => {
      let side = null;
      if (g.scoreTeam1 > p1) side = 1;
      else if (g.scoreTeam2 > p2) side = 2;
      p1 = g.scoreTeam1; p2 = g.scoreTeam2;
      const name = (g.goalGetterName || '').trim();
      if (name) diag.oldbNamed++;
      if (!side || !name) return;
      if (g.isOwnGoal) return;  // Eigentore zählen nicht für die Liste
      const team = side === 1 ? c1 : c2;
      const e = scorerStats[name] || (scorerStats[name] = { goals: 0, pens: 0, team });
      e.goals++;
      if (g.isPenalty) e.pens++;
      e.team = team;
      counted++;
    });
    if (counted > 0) scorerCovered[[c1, c2].sort().join('_')] = true;
    let res = null, hz = null;
    if (m.matchResults && m.matchResults.length) {
      res = m.matchResults.find(r => r.resultTypeID === 2) || m.matchResults[m.matchResults.length - 1];
      hz = m.matchResults.find(r => r.resultTypeID === 1) || null;
    }
    const kickoff = new Date(m.matchDateTimeUTC || m.matchDateTime).getTime();
    // Echte Anstosszeit immer merken — auch für künftige Spiele ohne Resultat
    if (kickoff && !isNaN(kickoff)) {
      liveSchedule[c1 + '_' + c2] = kickoff;
      liveSchedule[c2 + '_' + c1] = kickoff;
    }
    const started = now >= kickoff;
    const isLive = started && !m.matchIsFinished && (now - kickoff) < 3 * 3600 * 1000;
    const goals = (m.goals || []).map(g => ({
      min: g.matchMinute, who: g.goalGetterName,
      s1: g.scoreTeam1, s2: g.scoreTeam2, pen: g.isPenalty, og: g.isOwnGoal
    }));
    let home = res ? res.pointsTeam1 : null;
    let away = res ? res.pointsTeam2 : null;
    if (isLive && home === null) {
      home = goals.length ? goals[goals.length-1].s1 : 0;
      away = goals.length ? goals[goals.length-1].s2 : 0;
    }
    if (home === null && !isLive) return;
    const entry = { home, away, finished: !!m.matchIsFinished, live: isLive, goals, kickoff,
                    hz: hz ? hz.pointsTeam1 + ':' + hz.pointsTeam2 : null };
    liveResults[c1 + '_' + c2] = entry;
    liveResults[c2 + '_' + c1] = { ...entry, home: entry.away, away: entry.home,
                                   hz: hz ? hz.pointsTeam2 + ':' + hz.pointsTeam1 : null };
  });
}

function liveMinute(kickoff) {
  if (!kickoff) return '';
  const el = Math.floor((Date.now() - kickoff) / 60000);
  if (el < 0) return '';
  if (el <= 45) return '~' + el + "'";
  if (el <= 62) return 'Halbzeit';
  if (el <= 110) return '~' + (el - 17) + "'";
  return '2. HZ';
}

// ═══ TABELLEN ═══
function computeTable(group) {
  const teams = Object.keys(TEAMS).filter(c => TEAMS[c].gruppe === group);
  const stats = {};
  teams.forEach(c => stats[c] = { code: c, sp: 0, s: 0, u: 0, n: 0, t: 0, gt: 0, td: 0, pkt: 0 });
  MATCHES.filter(m => TEAMS[m.heim].gruppe === group).forEach(m => {
    const r = getResult(m, false);
    if (!r) return;
    const h = stats[m.heim], a = stats[m.gast];
    h.sp++; a.sp++;
    h.t += r.home; h.gt += r.away;
    a.t += r.away; a.gt += r.home;
    if (r.home > r.away) { h.s++; a.n++; h.pkt += 3; }
    else if (r.home < r.away) { a.s++; h.n++; a.pkt += 3; }
    else { h.u++; a.u++; h.pkt++; a.pkt++; }
  });
  return Object.values(stats).map(s => ({ ...s, td: s.t - s.gt })).sort((a, b) =>
    b.pkt - a.pkt || b.td - a.td || b.t - a.t);
}

function compute8BestThirds() {
  const thirds = GROUPS.map(g => {
    const t = computeTable(g);
    return t.length >= 3 && t[2].sp > 0 ? { ...t[2], gruppe: g } : null;
  }).filter(Boolean);
  thirds.sort((a, b) => b.pkt - a.pkt || b.td - a.td || b.t - a.t);
  return thirds.slice(0, 8);
}

// ═══ TEAM-LINKS ═══
function flagLink(code) {
  return '<a class="team-flag-link team-flag" href="https://de.wikipedia.org/wiki/' + TEAMS[code].landWiki +
    '" target="_blank" rel="noopener" title="Wikipedia: Land">' + TEAMS[code].flag + '</a>';
}
function nameLink(code) {
  return '<a class="team-name-link team-name" href="https://de.wikipedia.org/wiki/' +
    encodeURIComponent(TEAMS[code].verbandWiki) +
    '" target="_blank" rel="noopener" title="Wikipedia: Fussballverband">' + TEAMS[code].name + '</a>';
}

// ═══ GRUPPEN ═══
function renderGroups() {
  const grid = document.getElementById('groups-grid');
  const best8 = new Set(compute8BestThirds().map(t => t.code));
  grid.innerHTML = GROUPS.map(g => {
    const table = computeTable(g);
    const matches = MATCHES.filter(m => TEAMS[m.heim].gruppe === g)
      .sort((a, b) => a.spieltag - b.spieltag || a.datum.localeCompare(b.datum));
    const tableHtml = '<table class="group-table"><thead><tr>' +
      '<th class="num">#</th><th>Team</th><th class="num">SP</th><th class="num">S</th>' +
      '<th class="num">U</th><th class="num">N</th><th class="num">TD</th><th class="num">Pkt</th>' +
      '</tr></thead><tbody>' +
      table.map((t, i) => {
        let cls = i < 2 ? 'qualified' : (i === 2 && best8.has(t.code) ? 'third-pos' : '');
        if (t.code === followTeam) cls += ' followed-row';
        return '<tr class="' + cls + '"><td class="num">' + (i + 1) + '</td>' +
          '<td><span class="team-cell">' + flagLink(t.code) + nameLink(t.code) +
          '<button class="kader-btn" title="Kader anzeigen" onclick="openTeamRoster(\'' + t.code + '\')">👥</button></span></td>' +
          '<td class="num">' + t.sp + '</td><td class="num">' + t.s + '</td><td class="num">' + t.u + '</td>' +
          '<td class="num">' + t.n + '</td><td class="num">' + (t.td > 0 ? '+' : '') + t.td + '</td>' +
          '<td class="num"><strong>' + t.pkt + '</strong></td></tr>';
      }).join('') + '</tbody></table>';
    const matchesHtml = matches.map(m => matchRow(m, true, false)).join('');
    const cardCls = (followTeam && TEAMS[followTeam] && TEAMS[followTeam].gruppe === g) ? ' followed' : '';
    return '<div class="group-card' + cardCls + '"><div class="group-header">Gruppe ' + g + '</div>' + tableHtml +
      '<div class="match-list">' + matchesHtml + '</div></div>';
  }).join('');
}

function matchRow(m, withInputs, forceLive) {
  const r = getResult(m, forceLive);
  const isReal = r && r.real;
  const isLive = r && r.live;
  const st = STADIONS[m.stadion];
  let center;
  if (withInputs && !isReal) {
    const t = tips[m.id] || { home: '', away: '' };
    center = '<input class="score-input" type="number" min="0" max="99" value="' + (t.home ?? '') + '"' +
      ' data-match="' + m.id + '" data-side="home" onchange="onTipChange(event)">' +
      '<span>:</span>' +
      '<input class="score-input" type="number" min="0" max="99" value="' + (t.away ?? '') + '"' +
      ' data-match="' + m.id + '" data-side="away" onchange="onTipChange(event)">';
  } else if (isReal) {
    center = '<input class="score-input" disabled value="' + r.home + '"><span>:</span>' +
      '<input class="score-input" disabled value="' + r.away + '">';
  } else {
    center = r ? '<strong>' + r.home + ' : ' + r.away + '</strong>' : '<span>– : –</span>';
  }
  const minTxt = isLive ? liveMinute(r.kickoff) : '';
  const liveBadge = isLive ? ' <span class="live-badge">LIVE' + (minTxt ? ' ' + minTxt : '') + '</span>' : '';
  const hzTxt = (r && r.hz && r.finished) ? ' (HZ ' + r.hz + ')' : '';
  // Echte Anstosszeit (OpenLigaDB) hat Vorrang vor statischem Plan
  const lk = liveSchedule[liveKey(m)];
  const dateIso = lk ? new Date(lk).toLocaleDateString('sv-SE') : m.datum;
  const timeTxt = lk ? new Date(lk).toLocaleTimeString('de-CH', {hour: '2-digit', minute: '2-digit'}) : m.uhrzeit;
  const goalsLine = (r && r.goals && r.goals.length)
    ? '<div class="goals-line">⚽ ' + r.goals.map(g =>
        (g.min ? g.min + "' " : '') + (g.who || '') + (g.pen ? ' (P)' : '') + (g.og ? ' (ET)' : '') +
        (g.s1 != null ? ' [' + g.s1 + ':' + g.s2 + ']' : '')).join(' · ') + '</div>'
    : '';
  let cls = isLive ? 'is-live' : (isReal ? 'is-real' : (r ? 'has-tip' : ''));
  if (followTeam && (m.heim === followTeam || m.gast === followTeam)) cls += ' followed';
  return '<div class="match ' + cls + '" data-mid="' + m.id + '" style="cursor:pointer;" title="Klick: Aufstellung & Details">' +
    '<div class="home">' + nameLink(m.heim) + ' ' + flagLink(m.heim) + '</div>' +
    '<div class="vs">' + center + liveBadge + '</div>' +
    '<div class="away">' + flagLink(m.gast) + ' ' + nameLink(m.gast) + '</div>' +
    '<div class="meta">' + formatDate(dateIso) + ' · ' + timeTxt + ' · ' + st.stadt +
    ' · Spieltag ' + m.spieltag + hzTxt + '</div>' + goalsLine + '</div>';
}

function onTipChange(e) {
  const id = e.target.dataset.match, side = e.target.dataset.side;
  const v = e.target.value === '' ? null : parseInt(e.target.value, 10);
  if (!tips[id]) tips[id] = { home: null, away: null };
  tips[id][side] = v;
  if (tips[id].home === null && tips[id].away === null) delete tips[id];
  persist(); renderAll();
}

// ═══ BRACKET ═══
function slotTeam(slot, quals) {
  const pos = parseInt(slot[0], 10) - 1, grp = slot[1];
  return quals[grp] && quals[grp][pos] ? quals[grp][pos] : null;
}

// Dritten-Zuordnung: vollständiges Matching per Backtracking,
// damit alle 8 Dritten einen Slot bekommen (Greedy liess hintere Slots leer).
function assignThirds(thirds) {
  const slots = R32.filter(m => m.b.startsWith('3:'))
                   .map(m => ({ id: m.id, pool: m.b.slice(2).split('') }));
  const assignment = {};
  if (thirds.length === slots.length) {
    const used = new Set();
    const bt = (i) => {
      if (i === slots.length) return true;
      const s = slots[i];
      for (const t of thirds) {
        if (used.has(t.code) || !s.pool.includes(t.gruppe)) continue;
        used.add(t.code); assignment[s.id] = t.code;
        if (bt(i + 1)) return true;
        used.delete(t.code); delete assignment[s.id];
      }
      return false;
    };
    if (bt(0)) return assignment;
    Object.keys(assignment).forEach(k => delete assignment[k]);
  }
  // Fallback (unvollständige Gruppenphase oder kein perfektes Matching):
  // greedy mit Pool, danach Rest ohne Pool-Bedingung — kein Slot bleibt leer.
  const used = new Set();
  slots.forEach(s => {
    const t = thirds.find(t3 => !used.has(t3.code) && s.pool.includes(t3.gruppe));
    if (t) { used.add(t.code); assignment[s.id] = t.code; }
  });
  slots.forEach(s => {
    if (!assignment[s.id]) {
      const t = thirds.find(t3 => !used.has(t3.code));
      if (t) { used.add(t.code); assignment[s.id] = t.code; }
    }
  });
  return assignment;
}

function computeR32() {
  const quals = {};
  GROUPS.forEach(g => {
    const t = computeTable(g);
    quals[g] = [t[0] && t[0].sp > 0 ? t[0].code : null, t[1] && t[1].sp > 0 ? t[1].code : null];
  });
  const thirds = compute8BestThirds();
  const thirdAssign = assignThirds(thirds);
  return R32.map(m => ({ ...m,
    teamA: m.a.startsWith('3:') ? (thirdAssign[m.id] || null) : slotTeam(m.a, quals),
    teamB: m.b.startsWith('3:') ? (thirdAssign[m.id] || null) : slotTeam(m.b, quals),
  }));
}

function bkTeamHtml(code, matchId, slotLabel) {
  if (!code) return '<div class="bk-team tbd"><span class="nm">⏳ ' + slotLabel + '</span></div>';
  const isWinner = koPicks[matchId] === code;
  const isFollowed = code === followTeam;
  return '<div class="bk-team ' + (isWinner ? 'winner' : '') + (isFollowed ? ' followed' : '') +
    '" onclick="pickWinner(\'' +
    matchId + '\',\'' + code + '\')">' +
    '<span class="nm">' + TEAMS[code].flag + ' ' + TEAMS[code].name + '</span>' +
    '<span style="color:var(--muted);font-size:9px;">' + slotLabel + '</span></div>';
}

function pickWinner(matchId, code) {
  if (koPicks[matchId] === code) delete koPicks[matchId];
  else koPicks[matchId] = code;
  persist(); renderAll();
}

function renderBracket() {
  const el = document.getElementById('bracket');
  const r32 = computeR32();
  const winner = id => koPicks[id] || null;
  
  const afL = [['r32_1','r32_2'],['r32_3','r32_4'],['r32_5','r32_6'],['r32_7','r32_8']];
  const afR = [['r32_9','r32_10'],['r32_11','r32_12'],['r32_13','r32_14'],['r32_15','r32_16']];
  
  function koMatchHtml(id, a, b, la, lb, extra) {
    return '<div class="bk-match ' + (extra || '') + '">' +
      bkTeamHtml(a, id, la) + bkTeamHtml(b, id, lb) + '</div>';
  }
  
  const afTeams = {};
  afL.concat(afR).forEach((p, i) => { afTeams['af_' + (i+1)] = [winner(p[0]), winner(p[1])]; });
  const vfTeams = {
    vf_1: [winner('af_1'), winner('af_2')], vf_2: [winner('af_3'), winner('af_4')],
    vf_3: [winner('af_5'), winner('af_6')], vf_4: [winner('af_7'), winner('af_8')],
  };
  const hfTeams = { hf_1: [winner('vf_1'), winner('vf_2')], hf_2: [winner('vf_3'), winner('vf_4')] };
  const finTeams = [winner('hf_1'), winner('hf_2')];
  const champ = winner('final');
  
  const colR32L = r32.slice(0, 8).map(m => koMatchHtml(m.id, m.teamA, m.teamB, m.a, m.b)).join('');
  const colR32R = r32.slice(8).map(m => koMatchHtml(m.id, m.teamA, m.teamB, m.a, m.b)).join('');
  const colAFL = [1,2,3,4].map(i => koMatchHtml('af_'+i, afTeams['af_'+i][0], afTeams['af_'+i][1], '', '')).join('');
  const colAFR = [5,6,7,8].map(i => koMatchHtml('af_'+i, afTeams['af_'+i][0], afTeams['af_'+i][1], '', '')).join('');
  const colVFL = [1,2].map(i => koMatchHtml('vf_'+i, vfTeams['vf_'+i][0], vfTeams['vf_'+i][1], '', '')).join('');
  const colVFR = [3,4].map(i => koMatchHtml('vf_'+i, vfTeams['vf_'+i][0], vfTeams['vf_'+i][1], '', '')).join('');
  const colHFL = koMatchHtml('hf_1', hfTeams.hf_1[0], hfTeams.hf_1[1], '', '');
  const colHFR = koMatchHtml('hf_2', hfTeams.hf_2[0], hfTeams.hf_2[1], '', '');
  const colFinal = koMatchHtml('final', finTeams[0], finTeams[1], 'HF1', 'HF2', 'final') +
    (champ ? '<div class="champion-box">🏆 Weltmeister:<br>' + TEAMS[champ].flag + ' ' + TEAMS[champ].name + '</div>' : '') +
    '<div class="bk-info">19. Juli · MetLife Stadium<br>New York/New Jersey</div>';
  
  el.innerHTML =
    '<div class="bracket-col"><h4>Sechzehntel</h4>' + colR32L + '<div class="bk-info">28.6.–3.7.</div></div>' +
    '<div class="bracket-col"><h4>Achtelfinale</h4>' + colAFL + '<div class="bk-info">4.–7. Juli</div></div>' +
    '<div class="bracket-col"><h4>Viertelfinale</h4>' + colVFL + '<div class="bk-info">9.–11. Juli</div></div>' +
    '<div class="bracket-col"><h4>Halbfinale</h4>' + colHFL + '<div class="bk-info">14. Juli · Dallas</div></div>' +
    '<div class="bracket-col"><h4>🏆 Finale</h4>' + colFinal + '</div>' +
    '<div class="bracket-col"><h4>Halbfinale</h4>' + colHFR + '<div class="bk-info">15. Juli · Atlanta</div></div>' +
    '<div class="bracket-col"><h4>Viertelfinale</h4>' + colVFR + '<div class="bk-info">9.–11. Juli</div></div>' +
    '<div class="bracket-col"><h4>Achtelfinale</h4>' + colAFR + '<div class="bk-info">4.–7. Juli</div></div>' +
    '<div class="bracket-col"><h4>Sechzehntel</h4>' + colR32R + '<div class="bk-info">28.6.–3.7.</div></div>';
}

// ═══ SPIELPLAN (immer live) ═══
function renderSchedule() {
  const list = document.getElementById('schedule-list');
  const byDate = {};
  MATCHES.forEach(m => {
    const lk = liveSchedule[liveKey(m)];
    const d = lk ? new Date(lk).toLocaleDateString('sv-SE') : m.datum;
    (byDate[d] = byDate[d] || []).push(m);
  });
  const sortTime = m => {
    const lk = liveSchedule[liveKey(m)];
    return lk ? new Date(lk).toLocaleTimeString('sv-SE') : m.uhrzeit;
  };
  const today = new Date().toLocaleDateString('sv-SE');
  list.innerHTML = Object.keys(byDate).sort().map(d => {
    const matches = byDate[d].sort((a, b) => sortTime(a).localeCompare(sortTime(b)));
    const isToday = d === today;
    return '<div class="day-section">' +
      '<div class="day-header ' + (isToday ? 'today' : '') + '">' + formatDate(d, true) +
      (isToday ? ' · HEUTE' : '') + '</div>' +
      '<div class="day-matches">' + matches.map(m => matchRow(m, false, true)).join('') + '</div></div>';
  }).join('');
}

// ═══ SVG-KARTE ═══
const mapTT = document.getElementById('map-tooltip');
document.querySelectorAll('.stadion-dot').forEach(dot => {
  const sid = dot.dataset.sid;
  const s = STADIONS[sid];
  dot.addEventListener('mouseenter', () => {
    mapTT.textContent = s.name + ' · ' + s.stadt;
    mapTT.style.display = 'block';
  });
  dot.addEventListener('mousemove', e => {
    mapTT.style.left = (e.clientX + 14) + 'px';
    mapTT.style.top = (e.clientY + 14) + 'px';
  });
  dot.addEventListener('mouseleave', () => { mapTT.style.display = 'none'; });
  dot.addEventListener('click', () => {
    const panel = document.getElementById('stadion-panel');
    panel.className = 'show';
    const games = MATCHES.filter(m => m.stadion === sid).sort((a, b) => {
      const ka = liveSchedule[liveKey(a)], kb = liveSchedule[liveKey(b)];
      const da = ka ? new Date(ka).toISOString() : a.datum + 'T' + a.uhrzeit;
      const db = kb ? new Date(kb).toISOString() : b.datum + 'T' + b.uhrzeit;
      return da.localeCompare(db);
    });
    const gamesHtml = games.map(m => {
      const lk = liveSchedule[liveKey(m)];
      const dateIso = lk ? new Date(lk).toLocaleDateString('sv-SE') : m.datum;
      const fol = followTeam && (m.heim === followTeam || m.gast === followTeam);
      return '<div style="padding:3px 0;font-size:13px;' + (fol ? 'background:#FEF9C3;border-radius:4px;padding-left:6px;font-weight:700;' : '') + '">' +
        '<span style="color:var(--muted);font-size:11px;">' + formatDate(dateIso) + '</span> · ' +
        TEAMS[m.heim].flag + ' ' + TEAMS[m.heim].name + ' – ' +
        TEAMS[m.gast].name + ' ' + TEAMS[m.gast].flag + '</div>';
    }).join('');
    panel.innerHTML =
      '<div class="pname">' + s.name + '</div>' +
      '<div class="pmeta">' + s.stadt + ', ' + s.land + ' · 👥 ' +
      s.kap.toLocaleString('de-CH') + ' Plätze · ⚽ ' + s.spiele + ' WM-Spiele</div>' +
      '<div style="margin-bottom:10px;"><strong style="font-size:12px;color:var(--hkv-blue);">Gruppenspiele hier:</strong>' +
      gamesHtml + '</div>' +
      '<a class="pbtn wiki" href="https://de.wikipedia.org/wiki/' + encodeURIComponent(s.wiki) +
      '" target="_blank" rel="noopener">📖 Wikipedia</a>' +
      '<a class="pbtn maps" href="https://www.google.com/maps?q=' + s.lat + ',' + s.lng +
      '" target="_blank" rel="noopener">🗺️ Google Maps</a>';
  });
});

// ═══ TORSCHÜTZEN ═══
function renderScorers() {
  const el = document.getElementById('scorer-list');
  const dg = document.getElementById('scorer-diag');
  if (dg) {
    dg.innerHTML =
      '<strong>OpenLigaDB:</strong> ' + diag.oldb +
      ' · ' + diag.oldbGames + ' Spiele gematcht · ' + diag.oldbGoals + ' Tor-Einträge · ' +
      diag.oldbNamed + ' davon mit Schützenname<br>' +
      '<strong>TheSportsDB:</strong> ' + diag.tsdb +
      ' · ' + diag.tsdbEvents + ' Endrunden-Events gematcht · ' + diag.tsdbScored + ' mit Resultat · ' +
      diag.tsdbDetails + ' Schützen aus Details · ' + diag.lookups + ' Einzel-Nachladungen<br>' +
      '<strong>ESPN:</strong> ' + diag.espn + ' · ' + diag.espnGoals + ' Schützen erfasst<br>' +
      '<strong>Nicht erkannte Teamnamen:</strong> ' +
      (diag.unmatched.length ? diag.unmatched.join(', ') : 'keine');
  }
  const list = Object.entries(scorerStats)
    .map(([name, s]) => ({ name, ...s }))
    .sort((a, b) => b.goals - a.goals || a.name.localeCompare(b.name))
    .slice(0, 30);
  if (list.length === 0) {
    const played = Object.values(liveResults).some(r => r.finished);
    el.innerHTML = '<div style="color:var(--muted);font-size:13px;padding:12px;text-align:center;">' +
      (played
        ? 'Die Torschützen-Namen werden ergänzt, sobald sie in den Datenquellen verfügbar sind.'
        : 'Die Liste füllt sich automatisch, sobald Spiele gespielt sind.') +
      '</div>';
    return;
  }
  let rank = 0, prevGoals = -1;
  el.innerHTML = '<table class="scorer-table"><thead><tr>' +
    '<th class="num">#</th><th>Spieler</th><th>Team</th><th class="num">Tore</th></tr></thead><tbody>' +
    list.map((s, i) => {
      if (s.goals !== prevGoals) { rank = i + 1; prevGoals = s.goals; }
      const teamHtml = TEAMS[s.team]
        ? flagLink(s.team) + ' ' + nameLink(s.team)
        : '–';
      const penTxt = s.pens > 0 ? ' <span style="color:var(--muted);font-size:11px;">(' + s.pens + '× P)</span>' : '';
      return '<tr><td class="num rank">' + rank + '</td>' +
        '<td class="player">' + s.name + penTxt + '</td>' +
        '<td>' + teamHtml + '</td>' +
        '<td class="num goals-num">' + s.goals + '</td></tr>';
    }).join('') + '</tbody></table>';
}

// ═══ MODAL: KADER & SPIEL-DETAILS ═══
function openModal(title) {
  document.getElementById('modal-title').innerHTML = title;
  document.getElementById('modal-body').innerHTML = '<div class="modal-loading">Lade Daten…</div>';
  document.getElementById('modal-overlay').classList.add('show');
}
function closeModal() {
  document.getElementById('modal-overlay').classList.remove('show');
}
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

async function ensureTeamIds() {
  if (Object.keys(espnTeamIds).length >= 40) return;
  try {
    const r = await fetch('https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/teams');
    if (!r.ok) return;
    const j = await r.json();
    const list = j && j.sports && j.sports[0] && j.sports[0].leagues &&
                 j.sports[0].leagues[0] && j.sports[0].leagues[0].teams || [];
    list.forEach(t => {
      const tm = t.team || t;
      const code = codeFor(tm.displayName || tm.name);
      if (code && tm.id) espnTeamIds[code] = tm.id;
    });
  } catch (e) {}
}

const POS_ORDER = { G: 0, GK: 0, D: 1, M: 2, F: 3 };
function posKey(p) {
  const a = (p && (p.abbreviation || p.name) || '').toUpperCase().slice(0, 2);
  if (a.startsWith('G')) return 'G';
  if (a.startsWith('D')) return 'D';
  if (a.startsWith('M')) return 'M';
  return 'F';
}

async function fetchRoster(code) {
  if (rosterCache[code]) return rosterCache[code];
  await ensureTeamIds();
  const id = espnTeamIds[code];
  if (!id) return null;
  try {
    const r = await fetch('https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/teams/' + id + '/roster');
    if (!r.ok) return null;
    const j = await r.json();
    const roster = (j && j.athletes) || [];
    if (roster.length) rosterCache[code] = roster;
    return roster.length ? roster : null;
  } catch (e) { return null; }
}

// Wahrscheinliche Startelf aus dem Kader ableiten (Nummern-Heuristik, 4-3-3)
function buildLineupFromRoster(roster) {
  const byNr = arr => arr.slice().sort((a, b) =>
    (parseInt(a.jersey, 10) || 99) - (parseInt(b.jersey, 10) || 99));
  const grp = { G: [], D: [], M: [], F: [] };
  roster.forEach(a => grp[posKey(a.position)].push(a));
  Object.keys(grp).forEach(k => grp[k] = byNr(grp[k]));
  const pick = [];
  const take = (arr, n) => { const t = arr.splice(0, n); pick.push(...t); return t.length; };
  const gkN = take(grp.G, 1);
  let d = take(grp.D, 4), m = take(grp.M, 3), f = take(grp.F, 3);
  // Auffüllen, falls Gruppen zu klein
  let rest = [...grp.M, ...grp.D, ...grp.F];
  while (pick.length < 11 && rest.length) { pick.push(rest.shift()); m++; }
  const toEntry = a => ({ starter: true, jersey: a.jersey,
    position: a.position, athlete: { displayName: a.displayName || a.fullName } });
  return {
    formation: gkN ? (d + '-' + m + '-' + f) : '',
    roster: pick.slice(0, 11).map(toEntry),
  };
}

async function openTeamRoster(code) {
  const t = TEAMS[code];
  openModal(t.flag + ' Kader ' + t.name);
  const body = document.getElementById('modal-body');
  const roster = await fetchRoster(code);
  if (!roster) {
    body.innerHTML = '<div class="modal-hint">Der Kader wird angezeigt, sobald er in der Datenquelle hinterlegt ist.</div>';
    return;
  }
  const sorted = roster.slice().sort((a, b) => {
    const pa = POS_ORDER[posKey(a.position)] ?? 9, pb = POS_ORDER[posKey(b.position)] ?? 9;
    if (pa !== pb) return pa - pb;
    return (parseInt(a.jersey, 10) || 99) - (parseInt(b.jersey, 10) || 99);
  });
  const rowHtml = a => {
    const name = a.displayName || a.fullName || '?';
    const wiki = 'https://de.wikipedia.org/w/index.php?search=' + encodeURIComponent(name + ' Fussball');
    const posFull = (a.position && (a.position.displayName || a.position.name)) || '';
    return '<tr><td class="jersey">' + (a.jersey || '–') + '</td>' +
      '<td><a href="' + wiki + '" target="_blank" rel="noopener">' + name + '</a></td>' +
      '<td class="pos-abbr" title="' + posFull + '">' + posKey(a.position) + '</td>' +
      '<td class="num">' + (a.age || '') + '</td></tr>';
  };
  const half = Math.ceil(sorted.length / 2);
  const tableHtml = rows => '<table class="roster-table"><thead><tr>' +
    '<th>#</th><th>Spieler</th><th>Pos</th><th>Alter</th>' +
    '</tr></thead><tbody>' + rows.map(rowHtml).join('') + '</tbody></table>';
  body.innerHTML = '<div class="roster-grid">' +
    tableHtml(sorted.slice(0, half)) + tableHtml(sorted.slice(half)) + '</div>' +
    '<div style="font-size:10px;color:var(--muted);margin-top:8px;">Klick auf Spieler → Wikipedia · G Tor, D Abwehr, M Mittelfeld, F Sturm</div>';
}

async function fetchSummary(eventId) {
  if (summaryCache[eventId]) return summaryCache[eventId];
  try {
    const r = await fetch('https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/summary?event=' + eventId);
    if (!r.ok) return null;
    const j = await r.json();
    summaryCache[eventId] = j;
    return j;
  } catch (e) { return null; }
}

function lineupColHtml(code, ros, note) {
  const t = TEAMS[code];
  const starters = (ros.roster || []).filter(p => p.starter);
  const bench = (ros.roster || []).filter(p => !p.starter);
  const sortPos = arr => arr.slice().sort((a, b) =>
    (POS_ORDER[posKey(a.position)] ?? 9) - (POS_ORDER[posKey(b.position)] ?? 9) ||
    (parseInt(a.jersey, 10) || 99) - (parseInt(b.jersey, 10) || 99));
  const sorted = sortPos(starters);
  // Formation in Reihen parsen, sonst aus Positionsgruppen ableiten
  let rows = (ros.formation || '').split('-').map(n => parseInt(n, 10)).filter(n => n > 0);
  const field = sorted.filter(p => posKey(p.position) !== 'G');
  const gk = sorted.find(p => posKey(p.position) === 'G') || sorted[0];
  const outfield = sorted.filter(p => p !== gk);
  if (!rows.length || rows.reduce((a, b) => a + b, 0) !== outfield.length) {
    const cnt = { D: 0, M: 0, F: 0 };
    outfield.forEach(p => cnt[posKey(p.position)] = (cnt[posKey(p.position)] || 0) + 1);
    rows = [cnt.D, cnt.M, cnt.F].filter(n => n > 0);
    if (!rows.length && outfield.length) rows = [outfield.length];
  }
  const [fill, txt] = JERSEY[code] || ['#FFFFFF', '#1a1a1a'];
  const YELLOWISH = ['BRA', 'AUS', 'SWE', 'ECU', 'COL', 'RSA'];
  const gkFill = YELLOWISH.includes(code) ? '#FF8A00' : '#FFD400';
  const shortName = p => {
    const n = (p.athlete && (p.athlete.displayName || p.athlete.fullName)) || '';
    const parts = n.split(' ');
    let s = parts[parts.length - 1];
    if (s.length <= 3 && parts.length > 1) s = parts[parts.length - 2] + ' ' + s;
    return s.length > 13 ? s.slice(0, 12) + '…' : s;
  };
  const escA = s => String(s || '').replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/</g, '&lt;');
  const fullName = p => (p.athlete && (p.athlete.displayName || p.athlete.fullName)) || '';
  const shirt = (x, y, p, f, tx) =>
    '<g class="pl" data-pname="' + escA(fullName(p)) + '" style="cursor:pointer;" ' +
    'transform="translate(' + x + ',' + y + ')">' +
    '<path d="M-16,-9 L-7,-15 L-3,-11 L3,-11 L7,-15 L16,-9 L12,-1 L8,-4 L8,13 L-8,13 L-8,-4 L-12,-1 Z" ' +
    'fill="' + f + '" stroke="rgba(0,0,0,0.3)" stroke-width="1"/>' +
    '<text y="7" text-anchor="middle" font-size="12" font-weight="700" fill="' + tx + '">' + (p.jersey || '') + '</text>' +
    '<text y="28" text-anchor="middle" font-size="9" font-weight="600" fill="#fff" ' +
    'stroke="rgba(0,0,0,0.45)" stroke-width="2.5" paint-order="stroke">' + shortName(p) + '</text></g>';
  // Spieler-Positionen berechnen
  let players = '';
  if (gk) players += shirt(150, 388, gk, gkFill, '#1a1a1a');
  let idx = 0;
  const nRows = rows.length;
  rows.forEach((k, ri) => {
    const y = nRows > 1 ? 322 - ri * (252 / (nRows - 1)) : 200;
    for (let j = 0; j < k; j++) {
      const p = outfield[idx++];
      if (!p) continue;
      const x = 300 * (j + 1) / (k + 1);
      players += shirt(x, y, p, fill, txt);
    }
  });
  // Halbfeld: Rasenstreifen, Linien, Strafraum, Mittelkreis-Bogen oben
  let stripes = '';
  for (let i = 0; i < 6; i++) {
    stripes += '<rect x="0" y="' + (i * 71.7) + '" width="300" height="71.7" fill="' +
      (i % 2 ? '#379047' : '#3C9A4E') + '"/>';
  }
  const pitch =
    '<svg class="pitch-svg" viewBox="0 0 300 430" xmlns="http://www.w3.org/2000/svg">' +
    stripes +
    '<rect x="10" y="10" width="280" height="410" fill="none" stroke="white" stroke-width="2"/>' +
    '<path d="M 110,10 A 42,42 0 0 0 190,10" fill="none" stroke="white" stroke-width="2"/>' +
    '<rect x="62" y="348" width="176" height="72" fill="none" stroke="white" stroke-width="2"/>' +
    '<rect x="105" y="392" width="90" height="28" fill="none" stroke="white" stroke-width="2"/>' +
    '<circle cx="150" cy="365" r="2.5" fill="white"/>' +
    players + '</svg>';
  return '<div class="lineup-col"><h4>' + t.flag + ' ' + t.name +
    (ros.formation ? '<span class="formation-badge">' + ros.formation + '</span>' : '') + '</h4>' +
    pitch +
    (note ? '<div style="font-size:10px;color:var(--muted);margin-top:4px;">' + note + '</div>' : '') +
    (bench.length ? '<div class="bench-title">Bank</div><div class="bench-grid">' +
      sortPos(bench).slice(0, 15).map(p => '<span><span class="nr">' + (p.jersey || '') + '</span>' +
        shortName(p) + '</span>').join('') + '</div>' : '') +
    '</div>';
}

async function openMatchDetail(matchId) {
  const m = MATCHES.find(x => x.id === matchId);
  if (!m) return;
  const minKey = [m.heim, m.gast].sort().join('_');
  const r = getResult(m, true);
  const title = TEAMS[m.heim].flag + ' ' + TEAMS[m.heim].name +
    (r ? ' <span style="color:var(--hkv-blue)">' + r.home + ' : ' + r.away + '</span> ' : ' – ') +
    TEAMS[m.gast].name + ' ' + TEAMS[m.gast].flag;
  openModal(title);
  const body = document.getElementById('modal-body');
  // Event-ID besorgen (notfalls Scoreboard des Spieltags abfragen)
  let evInfo = espnEventByKey[minKey];
  if (!evInfo) {
    const lk = liveSchedule[liveKey(m)];
    const d = (lk ? new Date(lk).toLocaleDateString('sv-SE') : m.datum).replace(/-/g, '');
    try {
      const rs = await fetch('https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard?dates=' + d);
      if (rs.ok) { const js = await rs.json(); if (js && js.events) parseESPN(js.events); }
    } catch (e) {}
    evInfo = espnEventByKey[minKey];
  }
  const gl = (r && r.goals) ? r.goals : [];
  const goalRow = g => '<div>⚽ ' +
    (g.min ? '<strong style="color:var(--hkv-blue)">' + g.min + "'</strong> " : '') +
    (g.who || '') + (g.pen ? ' (P)' : '') +
    (g.og ? ' <span style="color:var(--muted)">(ET)</span>' : '') + '</div>';
  const hG = gl.filter(g => g.side === 'h').map(goalRow).join('');
  const aG = gl.filter(g => g.side === 'a').map(goalRow).join('');
  const rest = gl.filter(g => !g.side);
  const goalsHtml = gl.length
    ? '<div class="lineup-cols" style="margin-bottom:12px;font-size:13px;line-height:1.7;">' +
      '<div style="text-align:center;">' + hG + '</div>' +
      '<div style="text-align:center;">' + aG + '</div></div>' +
      (rest.length ? '<div style="text-align:center;font-size:12px;color:var(--muted);margin:-6px 0 10px;">⚽ ' +
        rest.map(g => (g.min ? g.min + "'" : '')).join(' · ') + '</div>' : '')
    : '';
  if (!evInfo) {
    body.innerHTML = goalsHtml + '<div class="modal-hint">Offizielle Aufstellung folgt ~1 h vor Anpfiff. ' +
      'Unten eine <strong>aus dem Kader abgeleitete</strong> mögliche Elf.</div>' +
      '<div id="last-lineups" class="lineup-cols"><div class="modal-loading">Lade Kader…</div></div>' +
      kaderButtons(m);
    const cols = [];
    for (const code of [m.heim, m.gast]) {
      const roster = await fetchRoster(code);
      cols.push(roster
        ? lineupColHtml(code, buildLineupFromRoster(roster), 'mögliche Elf — aus dem Kader abgeleitet')
        : '<div class="lineup-col"><h4>' + TEAMS[code].flag + ' ' + TEAMS[code].name +
          '</h4><div style="font-size:12px;color:var(--muted);">Aufstellung folgt, sobald Daten verfügbar sind.</div></div>');
    }
    const el = document.getElementById('last-lineups');
    if (el) el.innerHTML = cols.join('');
    return;
  }
  const sum = await fetchSummary(evInfo.id);
  const rosters = sum && sum.rosters;
  const hasLineup = rosters && rosters.some(x => x.roster && x.roster.length);
  if (hasLineup) {
    const rosH = rosters.find(x => x.homeAway === 'home') || rosters[0];
    const rosA = rosters.find(x => x.homeAway === 'away') || rosters[1];
    body.innerHTML = goalsHtml +
      '<div class="lineup-cols">' +
      lineupColHtml(m.heim, rosH || {}) + lineupColHtml(m.gast, rosA || {}) +
      '</div>' + kaderButtons(m);
  } else {
    // Aufstellung noch nicht publiziert → letzte Aufstellung, sonst aus Kader ableiten
    body.innerHTML = goalsHtml + '<div class="modal-hint">Offizielle Aufstellung noch nicht publiziert ' +
      '(kommt ~1 h vor Anpfiff). Angezeigt wird die <strong>zuletzt gespielte</strong> oder eine ' +
      '<strong>aus dem Kader abgeleitete</strong> Aufstellung.</div>' +
      '<div id="last-lineups" class="lineup-cols"><div class="modal-loading">Lade Aufstellungen…</div></div>' +
      kaderButtons(m);
    const cols = [];
    for (const code of [m.heim, m.gast]) {
      const last = await findLastLineup(code, evInfo.id);
      if (last) {
        cols.push(lineupColHtml(code, last, 'zuletzt gespielte Aufstellung'));
        continue;
      }
      const roster = await fetchRoster(code);
      if (roster) {
        cols.push(lineupColHtml(code, buildLineupFromRoster(roster),
          'mögliche Elf — aus dem Kader abgeleitet'));
      } else {
        cols.push('<div class="lineup-col"><h4>' + TEAMS[code].flag + ' ' + TEAMS[code].name +
          '</h4><div style="font-size:12px;color:var(--muted);">Aufstellung folgt, sobald Daten verfügbar sind.</div></div>');
      }
    }
    const el = document.getElementById('last-lineups');
    if (el) el.innerHTML = cols.join('');
  }
}

async function findLastLineup(code, excludeEventId) {
  // Jüngstes anderes Event dieses Teams mit publizierter Aufstellung suchen
  const entries = Object.entries(espnEventByKey)
    .filter(([k, v]) => k.includes(code) && v.id !== excludeEventId)
    .sort((a, b) => (b[1].dateIso || '').localeCompare(a[1].dateIso || ''));
  for (const [, v] of entries.slice(0, 3)) {
    const sum = await fetchSummary(v.id);
    const ros = sum && sum.rosters && sum.rosters.find(x => {
      const tc = codeFor(x.team && (x.team.displayName || x.team.name));
      return tc === code && x.roster && x.roster.length;
    });
    if (ros) return ros;
  }
  return null;
}

function kaderButtons(m) {
  return '<div style="margin-top:14px;display:flex;gap:8px;flex-wrap:wrap;">' +
    '<button class="modal-close" style="width:auto;padding:0 14px;height:32px;font-size:12px;" ' +
    'onclick="openTeamRoster(\'' + m.heim + '\')">👥 Kader ' + TEAMS[m.heim].name + '</button>' +
    '<button class="modal-close" style="width:auto;padding:0 14px;height:32px;font-size:12px;" ' +
    'onclick="openTeamRoster(\'' + m.gast + '\')">👥 Kader ' + TEAMS[m.gast].name + '</button></div>';
}

// ═══ SPIELERFOTO BEI HOVER (Wikipedia, wie beim Parlament) ═══
const playerPhotoCache = {};
async function fetchPlayerPhoto(name) {
  if (name in playerPhotoCache) return playerPhotoCache[name];
  let found = null;
  for (const lang of ['de', 'en']) {
    try {
      const r = await fetch('https://' + lang + '.wikipedia.org/api/rest_v1/page/summary/' +
        encodeURIComponent(name.replace(/ /g, '_')));
      if (!r.ok) continue;
      const j = await r.json();
      if (j.type && String(j.type).includes('disambiguation')) continue;
      const txt = ((j.extract || '') + ' ' + (j.description || '')).toLowerCase();
      if (!/fußball|fussball|footballer|football|soccer/.test(txt)) continue;
      if (j.thumbnail && j.thumbnail.source) { found = j.thumbnail.source; break; }
    } catch (e) {}
  }
  playerPhotoCache[name] = found;
  return found;
}

(function () {
  const body = document.getElementById('modal-body');
  const tt = document.getElementById('map-tooltip');
  let hoverName = null;
  body.addEventListener('mouseover', async e => {
    const g = e.target.closest('g.pl');
    if (!g || !g.dataset.pname) return;
    const name = g.dataset.pname;
    hoverName = name;
    tt.innerHTML = '<div style="font-weight:600">' + name + '</div>';
    tt.style.display = 'block';
    const photo = await fetchPlayerPhoto(name);
    if (hoverName !== name || tt.style.display === 'none') return;
    if (photo) tt.innerHTML = '<div style="font-weight:600">' + name + '</div>' +
      '<img src="' + photo + '" alt="" onerror="this.remove()">';
  });
  body.addEventListener('mousemove', e => {
    if (!e.target.closest('g.pl')) return;
    tt.style.left = (e.clientX + 14) + 'px';
    tt.style.top = (e.clientY + 14) + 'px';
  });
  body.addEventListener('mouseout', e => {
    if (e.target.closest('g.pl')) { hoverName = null; tt.style.display = 'none'; }
  });
  body.addEventListener('click', e => {
    const g = e.target.closest('g.pl');
    if (!g || !g.dataset.pname) return;
    window.open('https://de.wikipedia.org/w/index.php?search=' +
      encodeURIComponent(g.dataset.pname + ' Fussball'), '_blank', 'noopener');
  });
})();

// ═══ HELPERS ═══
function formatDate(iso, long) {
  const d = new Date(iso + 'T12:00:00');
  return d.toLocaleDateString('de-CH', long
    ? { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }
    : { weekday: 'short', day: 'numeric', month: 'short' });
}

// Spiel-Klick → Detail-Modal (Inputs & Links bleiben funktional)
document.addEventListener('click', e => {
  const matchEl = e.target.closest('.match');
  if (!matchEl || !matchEl.dataset.mid) return;
  if (e.target.closest('input, a, button')) return;
  openMatchDetail(matchEl.dataset.mid);
});

// ═══ TABS ═══
document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById('tab-' + tab.dataset.tab).classList.add('active');
  });
});

// ═══ INIT — Live läuft IMMER ═══
function renderAll() { renderGroups(); renderBracket(); renderSchedule(); renderScorers(); }
// Follow-Dropdown befüllen (alphabetisch)
(function () {
  const sel = document.getElementById('follow-select');
  Object.entries(TEAMS)
    .sort((a, b) => a[1].name.localeCompare(b[1].name, 'de'))
    .forEach(([code, t]) => {
      const o = document.createElement('option');
      o.value = code;
      o.textContent = t.flag + ' ' + t.name + ' (Gruppe ' + t.gruppe + ')';
      sel.appendChild(o);
    });
  if (followTeam && TEAMS[followTeam]) sel.value = followTeam;
  else followTeam = null;
})();
if (liveInTips) document.getElementById('live-toggle').classList.add('on');
renderAll();
updateMapHighlights();
fetchLive().then(() => renderAll());
setInterval(() => fetchLive().then(() => renderAll()), 60000);
</script>
</body>
</html>
"""

HTML = (HTML
    .replace('__MAP_SVG__', MAP_SVG)
    .replace('__TEAMS__', json.dumps(teams_js, ensure_ascii=False))
    .replace('__MATCHES__', json.dumps(matches_js, ensure_ascii=False))
    .replace('__STADIONS__', json.dumps(stadions_js, ensure_ascii=False))
    .replace('__GROUPS__', json.dumps(GROUPS_ORDER))
    .replace('__R32__', json.dumps(R32_BRACKET))
    .replace('__ALIAS__', json.dumps(OLDB_ALIAS, ensure_ascii=False))
    .replace('__STRENGTH__', json.dumps(STRENGTH))
    .replace('__JERSEY__', json.dumps(JERSEY)))

import os
os.makedirs('/mnt/user-data/outputs', exist_ok=True)
out = '/mnt/user-data/outputs/wm2026_spielplan.html'
with open(out, 'w', encoding='utf-8') as f:
    f.write(HTML)
print(f"Gespeichert: {out}")
print(f"Grösse: {os.path.getsize(out) / 1024:.1f} KB")
for ph in ['__MAP_SVG__', '__TEAMS__', '__MATCHES__', '__STADIONS__', '__GROUPS__', '__R32__', '__ALIAS__', '__STRENGTH__']:
    assert ph not in HTML, f"Platzhalter {ph} nicht ersetzt!"
print("Platzhalter ✓ · Leaflet entfernt:", 'leaflet' not in HTML.lower())
