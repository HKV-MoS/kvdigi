"""WM 2026 Daten — Stand: 11. Juni 2026 (Turnierstart).

Quellen: FIFA, UEFA, Wikipedia.
"""

# ─── 48 TEAMS ────────────────────────────────────────────────────────────
# Code → (Name DE, Flagge-Emoji, Konföderation, Gruppe)
TEAMS = {
    # Gruppe A
    "MEX": ("Mexiko", "🇲🇽", "CONCACAF", "A"),
    "RSA": ("Südafrika", "🇿🇦", "CAF", "A"),
    "KOR": ("Südkorea", "🇰🇷", "AFC", "A"),
    "CZE": ("Tschechien", "🇨🇿", "UEFA", "A"),
    # Gruppe B
    "CAN": ("Kanada", "🇨🇦", "CONCACAF", "B"),
    "BIH": ("Bosnien-Herz.", "🇧🇦", "UEFA", "B"),
    "QAT": ("Katar", "🇶🇦", "AFC", "B"),
    "SUI": ("Schweiz", "🇨🇭", "UEFA", "B"),
    # Gruppe C
    "BRA": ("Brasilien", "🇧🇷", "CONMEBOL", "C"),
    "MAR": ("Marokko", "🇲🇦", "CAF", "C"),
    "HAI": ("Haiti", "🇭🇹", "CONCACAF", "C"),
    "SCO": ("Schottland", "🏴󠁧󠁢󠁳󠁣󠁴󠁿", "UEFA", "C"),
    # Gruppe D
    "USA": ("USA", "🇺🇸", "CONCACAF", "D"),
    "PAR": ("Paraguay", "🇵🇾", "CONMEBOL", "D"),
    "AUS": ("Australien", "🇦🇺", "AFC", "D"),
    "TUR": ("Türkei", "🇹🇷", "UEFA", "D"),
    # Gruppe E
    "GER": ("Deutschland", "🇩🇪", "UEFA", "E"),
    "CUW": ("Curaçao", "🇨🇼", "CONCACAF", "E"),
    "CIV": ("Elfenbeinküste", "🇨🇮", "CAF", "E"),
    "ECU": ("Ecuador", "🇪🇨", "CONMEBOL", "E"),
    # Gruppe F
    "NED": ("Niederlande", "🇳🇱", "UEFA", "F"),
    "JPN": ("Japan", "🇯🇵", "AFC", "F"),
    "SWE": ("Schweden", "🇸🇪", "UEFA", "F"),
    "TUN": ("Tunesien", "🇹🇳", "CAF", "F"),
    # Gruppe G
    "BEL": ("Belgien", "🇧🇪", "UEFA", "G"),
    "EGY": ("Ägypten", "🇪🇬", "CAF", "G"),
    "IRN": ("Iran", "🇮🇷", "AFC", "G"),
    "NZL": ("Neuseeland", "🇳🇿", "OFC", "G"),
    # Gruppe H
    "ESP": ("Spanien", "🇪🇸", "UEFA", "H"),
    "CPV": ("Kap Verde", "🇨🇻", "CAF", "H"),
    "KSA": ("Saudi-Arabien", "🇸🇦", "AFC", "H"),
    "URU": ("Uruguay", "🇺🇾", "CONMEBOL", "H"),
    # Gruppe I
    "FRA": ("Frankreich", "🇫🇷", "UEFA", "I"),
    "SEN": ("Senegal", "🇸🇳", "CAF", "I"),
    "IRQ": ("Irak", "🇮🇶", "AFC", "I"),
    "NOR": ("Norwegen", "🇳🇴", "UEFA", "I"),
    # Gruppe J
    "ARG": ("Argentinien", "🇦🇷", "CONMEBOL", "J"),
    "ALG": ("Algerien", "🇩🇿", "CAF", "J"),
    "AUT": ("Österreich", "🇦🇹", "UEFA", "J"),
    "JOR": ("Jordanien", "🇯🇴", "AFC", "J"),
    # Gruppe K
    "POR": ("Portugal", "🇵🇹", "UEFA", "K"),
    "COD": ("DR Kongo", "🇨🇩", "CAF", "K"),
    "UZB": ("Usbekistan", "🇺🇿", "AFC", "K"),
    "COL": ("Kolumbien", "🇨🇴", "CONMEBOL", "K"),
    # Gruppe L
    "ENG": ("England", "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "UEFA", "L"),
    "CRO": ("Kroatien", "🇭🇷", "UEFA", "L"),
    "GHA": ("Ghana", "🇬🇭", "CAF", "L"),
    "PAN": ("Panama", "🇵🇦", "CONCACAF", "L"),
}

GROUPS_ORDER = list("ABCDEFGHIJKL")

# Konföderations-Farben
KONF_COLORS = {
    "UEFA":     "#3B82F6",  # blau
    "CONMEBOL": "#F59E0B",  # orange
    "CONCACAF": "#10B981",  # grün
    "CAF":      "#EF4444",  # rot
    "AFC":      "#8B5CF6",  # violett
    "OFC":      "#06B6D4",  # cyan
}

# ─── 16 STADIEN ──────────────────────────────────────────────────────────
STADIONS = {
    "atl": {"name": "Atlanta-Stadion", "stadt": "Atlanta", "land": "USA",
            "kap": 75000, "lat": 33.7553, "lng": -84.4006, "spiele": 8},
    "bos": {"name": "Boston-Stadion", "stadt": "Foxborough", "land": "USA",
            "kap": 65000, "lat": 42.0909, "lng": -71.2643, "spiele": 7},
    "dal": {"name": "Dallas-Stadion", "stadt": "Arlington", "land": "USA",
            "kap": 94000, "lat": 32.7475, "lng": -97.0945, "spiele": 9},
    "hou": {"name": "Houston-Stadion", "stadt": "Houston", "land": "USA",
            "kap": 72000, "lat": 29.6847, "lng": -95.4108, "spiele": 7},
    "kan": {"name": "Kansas City-Stadion", "stadt": "Kansas City", "land": "USA",
            "kap": 76000, "lat": 39.0489, "lng": -94.4839, "spiele": 6},
    "los": {"name": "Los Angeles-Stadion", "stadt": "Inglewood", "land": "USA",
            "kap": 70000, "lat": 33.9535, "lng": -118.3392, "spiele": 8},
    "mia": {"name": "Miami-Stadion", "stadt": "Miami Gardens", "land": "USA",
            "kap": 65000, "lat": 25.9580, "lng": -80.2389, "spiele": 7},
    "nyc": {"name": "New York/New Jersey-Stadion", "stadt": "East Rutherford", "land": "USA",
            "kap": 82500, "lat": 40.8135, "lng": -74.0744, "spiele": 8},
    "phi": {"name": "Philadelphia-Stadion", "stadt": "Philadelphia", "land": "USA",
            "kap": 69000, "lat": 39.9008, "lng": -75.1675, "spiele": 6},
    "sfo": {"name": "San Francisco-Stadion", "stadt": "Santa Clara", "land": "USA",
            "kap": 70000, "lat": 37.4030, "lng": -121.9700, "spiele": 6},
    "sea": {"name": "Seattle-Stadion", "stadt": "Seattle", "land": "USA",
            "kap": 69000, "lat": 47.5952, "lng": -122.3316, "spiele": 6},
    "azt": {"name": "Aztekenstadion", "stadt": "Mexiko-Stadt", "land": "MEX",
            "kap": 87000, "lat": 19.3029, "lng": -99.1505, "spiele": 5},
    "gua": {"name": "Guadalajara-Stadion", "stadt": "Guadalajara", "land": "MEX",
            "kap": 49000, "lat": 20.6818, "lng": -103.4625, "spiele": 4},
    "mty": {"name": "Monterrey-Stadion", "stadt": "Monterrey", "land": "MEX",
            "kap": 53500, "lat": 25.6692, "lng": -100.2444, "spiele": 4},
    "tor": {"name": "Toronto-Stadion", "stadt": "Toronto", "land": "CAN",
            "kap": 45000, "lat": 43.6332, "lng": -79.4185, "spiele": 6},
    "van": {"name": "Vancouver-Stadion", "stadt": "Vancouver", "land": "CAN",
            "kap": 54000, "lat": 49.2767, "lng": -123.1119, "spiele": 7},
}

# ─── 72 GRUPPENSPIELE ────────────────────────────────────────────────────
# Format: (id, datum, uhrzeit_mesz, heim, gast, stadion, spieltag)
# Spieltag-Logik: 1: T1vT2 + T3vT4 | 2: T1vT3 + T4vT2 | 3: T4vT1 + T2vT3
# Konkrete Termine sind aus offiziellen Quellen, wo bekannt.

MATCHES_GROUP = [
    # ─── SPIELTAG 1 (11.-17. Juni) ────────────────────────────────────────
    # 11. Juni — Eröffnung
    ("A1", "2026-06-11", "21:00", "MEX", "RSA", "azt", 1),
    ("A2", "2026-06-12", "04:00", "KOR", "CZE", "gua", 1),
    # 12. Juni
    ("D1", "2026-06-12", "19:00", "USA", "PAR", "los", 1),
    ("B1", "2026-06-12", "22:00", "CAN", "BIH", "tor", 1),
    # 13. Juni
    ("C1", "2026-06-13", "21:00", "BRA", "MAR", "mia", 1),
    ("D2", "2026-06-13", "22:00", "AUS", "TUR", "sea", 1),
    ("B2", "2026-06-13", "01:00", "QAT", "SUI", "van", 1),
    # 14. Juni — Deutschland-Start
    ("C2", "2026-06-14", "19:00", "HAI", "SCO", "kan", 1),
    ("E1", "2026-06-14", "19:00", "GER", "CUW", "hou", 1),
    ("E2", "2026-06-14", "22:00", "CIV", "ECU", "phi", 1),
    ("F1", "2026-06-14", "01:00", "NED", "JPN", "los", 1),
    # 15. Juni
    ("F2", "2026-06-15", "19:00", "SWE", "TUN", "bos", 1),
    ("G1", "2026-06-15", "21:00", "BEL", "EGY", "atl", 1),
    ("G2", "2026-06-15", "22:00", "IRN", "NZL", "nyc", 1),
    # 16. Juni
    ("H1", "2026-06-16", "19:00", "ESP", "CPV", "dal", 1),
    ("H2", "2026-06-16", "22:00", "KSA", "URU", "kan", 1),
    ("I1", "2026-06-16", "01:00", "FRA", "SEN", "atl", 1),
    # 17. Juni
    ("I2", "2026-06-17", "19:00", "IRQ", "NOR", "sfo", 1),
    ("J1", "2026-06-17", "21:00", "ARG", "ALG", "mia", 1),
    ("J2", "2026-06-17", "22:00", "AUT", "JOR", "nyc", 1),
    ("K1", "2026-06-17", "01:00", "POR", "COD", "sea", 1),
    ("K2", "2026-06-17", "04:00", "UZB", "COL", "los", 1),
    ("L1", "2026-06-17", "06:00", "ENG", "CRO", "bos", 1),
    ("L2", "2026-06-17", "06:00", "GHA", "PAN", "phi", 1),
    # ─── SPIELTAG 2 (17.-23. Juni) ────────────────────────────────────────
    ("A3", "2026-06-19", "03:00", "MEX", "KOR", "gua", 2),
    ("A4", "2026-06-18", "18:00", "CZE", "RSA", "atl", 2),
    ("B3", "2026-06-18", "21:00", "CAN", "QAT", "van", 2),
    ("B4", "2026-06-19", "01:00", "BIH", "SUI", "tor", 2),
    ("C3", "2026-06-19", "19:00", "BRA", "HAI", "mia", 2),
    ("C4", "2026-06-19", "22:00", "MAR", "SCO", "bos", 2),
    ("D3", "2026-06-19", "01:00", "USA", "AUS", "sea", 2),
    ("D4", "2026-06-19", "21:00", "PAR", "TUR", "kan", 2),
    ("E3", "2026-06-20", "19:00", "GER", "CIV", "tor", 2),
    ("E4", "2026-06-20", "22:00", "CUW", "ECU", "atl", 2),
    ("F3", "2026-06-20", "01:00", "NED", "SWE", "los", 2),
    ("F4", "2026-06-21", "19:00", "JPN", "TUN", "nyc", 2),
    ("G3", "2026-06-21", "21:00", "BEL", "IRN", "phi", 2),
    ("G4", "2026-06-21", "22:00", "EGY", "NZL", "dal", 2),
    ("H3", "2026-06-22", "19:00", "ESP", "KSA", "atl", 2),
    ("H4", "2026-06-22", "22:00", "CPV", "URU", "mty", 2),
    ("I3", "2026-06-22", "01:00", "FRA", "IRQ", "sfo", 2),
    ("I4", "2026-06-23", "19:00", "SEN", "NOR", "hou", 2),
    ("J3", "2026-06-23", "21:00", "ARG", "AUT", "los", 2),
    ("J4", "2026-06-23", "22:00", "ALG", "JOR", "kan", 2),
    ("K3", "2026-06-23", "01:00", "POR", "UZB", "nyc", 2),
    ("K4", "2026-06-24", "04:00", "COD", "COL", "mia", 2),
    ("L3", "2026-06-24", "21:00", "ENG", "GHA", "tor", 2),
    ("L4", "2026-06-24", "22:00", "CRO", "PAN", "atl", 2),
    # ─── SPIELTAG 3 (24.-27. Juni) — parallel pro Gruppe ──────────────────
    ("A5", "2026-06-24", "03:00", "CZE", "MEX", "azt", 3),
    ("A6", "2026-06-24", "03:00", "RSA", "KOR", "mty", 3),
    ("B5", "2026-06-24", "22:00", "SUI", "CAN", "van", 3),
    ("B6", "2026-06-24", "22:00", "QAT", "BIH", "sea", 3),
    ("C5", "2026-06-25", "19:00", "SCO", "BRA", "kan", 3),
    ("C6", "2026-06-25", "19:00", "HAI", "MAR", "mty", 3),
    ("D5", "2026-06-25", "22:00", "TUR", "USA", "los", 3),
    ("D6", "2026-06-25", "22:00", "PAR", "AUS", "bos", 3),
    ("E5", "2026-06-25", "22:00", "ECU", "GER", "nyc", 3),
    ("E6", "2026-06-25", "22:00", "CUW", "CIV", "phi", 3),
    ("F5", "2026-06-26", "19:00", "TUN", "NED", "atl", 3),
    ("F6", "2026-06-26", "19:00", "JPN", "SWE", "sfo", 3),
    ("G5", "2026-06-26", "22:00", "NZL", "BEL", "tor", 3),
    ("G6", "2026-06-26", "22:00", "EGY", "IRN", "dal", 3),
    ("H5", "2026-06-26", "22:00", "URU", "ESP", "atl", 3),
    ("H6", "2026-06-26", "22:00", "KSA", "CPV", "hou", 3),
    ("I5", "2026-06-27", "19:00", "NOR", "FRA", "kan", 3),
    ("I6", "2026-06-27", "19:00", "SEN", "IRQ", "mia", 3),
    ("J5", "2026-06-27", "22:00", "JOR", "ARG", "los", 3),
    ("J6", "2026-06-27", "22:00", "AUT", "ALG", "phi", 3),
    ("K5", "2026-06-27", "22:00", "COL", "POR", "nyc", 3),
    ("K6", "2026-06-27", "22:00", "COD", "UZB", "sea", 3),
    ("L5", "2026-06-27", "22:00", "PAN", "ENG", "atl", 3),
    ("L6", "2026-06-27", "22:00", "GHA", "CRO", "dal", 3),
]

# ─── KO-TERMINE (Paarungen werden dynamisch berechnet) ───────────────────
KO_DATES = {
    "r32": ("28. Juni – 3. Juli", "Sechzehntelfinale"),    # 16 Spiele
    "r16": ("4. – 7. Juli",       "Achtelfinale"),         # 8 Spiele
    "qf":  ("9. – 11. Juli",      "Viertelfinale"),        # 4 Spiele
    "sf":  ("14. & 15. Juli",     "Halbfinale"),           # 2 Spiele
    "tp":  ("18. Juli",           "Spiel um Platz 3"),     # 1 Spiel
    "fin": ("19. Juli",           "Finale"),               # 1 Spiel — MetLife Stadium
}

if __name__ == "__main__":
    print(f"Teams: {len(TEAMS)}")
    print(f"Gruppen: {len(GROUPS_ORDER)}")
    print(f"Stadien: {len(STADIONS)} ({sum(s['spiele'] for s in STADIONS.values())} Spiele geplant)")
    print(f"Gruppenspiele: {len(MATCHES_GROUP)}")
    # Validierung
    from collections import Counter
    g = Counter(t[3] for t in TEAMS.values())
    print(f"Teams pro Gruppe: {dict(g)}")
    g_matches = Counter(m[3:4][0] if len(m) > 6 else None for m in MATCHES_GROUP)
    print(f"Spielpaarungen pro Gruppe: {dict(Counter(TEAMS[m[3]][3] for m in MATCHES_GROUP))}")
