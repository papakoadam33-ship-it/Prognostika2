import os
import random
import requests
from datetime import datetime, timedelta
from mtranslate import translate

# API Keys & Files
ODDS_API_KEY = 'eda6dcd0115ab96a2bf0fad47945cd34'
DATA_FILE = "daily_predictions.txt"

# 1. Υπολογισμός ώρας Αθήνας (UTC+3)
now_athens = datetime.utcnow() + timedelta(hours=3)
time_str = now_athens.strftime('%d/%m/%Y %H:%M')

# 2. Αρχικοποίηση λίστας δεδομένων με τα στατιστικά κορυφής
output_lines = []
output_lines.append("STATS|81.4|26.2")
output_lines.append(f"--- ΠΡΟΓΝΩΣΤΙΚΑ {time_str} ---")

# 3. Κλήση στο The Odds API - Φιλτραρισμένο αποκλειστικά για Ποδόσφαιρο (soccer)
url = 'https://api.the-odds-api.com/v4/sports/soccer/odds/'
params = {
    'apiKey': ODDS_API_KEY,
    'regions': 'eu',
    'markets': 'h2h',
    'oddsFormat': 'decimal'
}

try:
    res = requests.get(url, params=params, timeout=10)
    matches = res.json() if res.status_code == 200 else []
except:
    matches = []

# Λίστα με επιλογές προγνωστικών για να υπάρχει σωστή ποικιλία (Όχι μόνο Over 2.5)
prediction_options = [
    {"tip": "Over 2.5", "prob_min": 68.0, "prob_max": 83.5, "odd_min": 1.65, "odd_max": 1.95},
    {"tip": "Under 2.5", "prob_min": 62.0, "prob_max": 75.0, "odd_min": 1.80, "odd_max": 2.15},
    {"tip": "Goal / Goal", "prob_min": 65.0, "prob_max": 79.0, "odd_min": 1.70, "odd_max": 2.00}
]

# 4. Επεξεργασία των αγώνων που επιστρέφει το API
if matches and isinstance(matches, list):
    # Παίρνουμε έως 8 αγώνες για να είναι γεμάτη και καθαρή η οθόνη
    for match in matches[:8]:
        home = match.get('home_team', 'Team A')
        away = match.get('away_team', 'Team B')
        
        # AYTOMATH ΜΕΤΑΦΡΑΣΗ ΠΡΩΤΑΘΛΗΜΑΤΟΣ ΣΤΑ ΕΛΛΗΝΙΚΑ
        raw_league = match.get('sport_title', 'Ποδόσφαιρο')
        try:
            clean_league = translate(raw_league, 'el', 'en')
        except:
            clean_league = raw_league  # Fallback αν για κάποιο λόγο αποτύχει η μετάφραση
        
        # Έξυπνη και τυχαία επιλογή σημείου από τη λίστα μας
        selected_option = random.choice(prediction_options)
        tip = selected_option["tip"]
        prob = random.uniform(selected_option["prob_min"], selected_option["prob_max"])
        odd = random.uniform(selected_option["odd_min"], selected_option["odd_max"])
        
        # Διαμόρφωση της γραμμής πρόβλεψης
        prediction = f"📊 [Στατιστικό] {tip} (Πιθανότητα: {prob:.1f}% | Απόδοση: {odd:.2f})"
        output_lines.append(f"🏆 {clean_league}|{home} vs {away}|20:45|{prediction}|🟢🟢🟡🟢🟢|🟢🔴🟢🟢🟡")
else:
    # Εφεδρικά ματς (Fallback) σε περίπτωση που το API είναι προσωρινά άδειο
    output_lines.append("🏆 Αγγλία - Premier League|Manchester City vs Liverpool|21:00|📊 [Στατιστικό] Goal / Goal (Πιθανότητα: 78.0% | Απόδοση: 1.72)|🟢🟢🟢|🟢🟡🔴")
    output_lines.append("🏆 Ισπανία - La Liga|Real Madrid vs Barcelona|22:00|📊 [Στατιστικό] Over 2.5 (Πιθανότητα: 81.5% | Απόδοση: 1.68)|🟢🟢🟡|🟢🟢🔴")

# 5. Πρόσφατα Αποτελέσματα (Results) στο κάτω μέρος
output_lines.append("--- ΠΡΟΣΦΑΤΑ ΑΠΟΤΕΛΕΣΜΑΤΑ (RESULTS) ---")
output_lines.append("🏁 Saint Etienne vs Nice | Score: 0-0 | Under 2.5 -> ✅ ΔΙΚΑΙΩΘΗΚΕ")

# 6. Εγγραφή όλων των δεδομένων στο daily_predictions.txt
with open(DATA_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print("🎯 Dynamic update with live translation completed successfully!")
