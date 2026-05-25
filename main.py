import requests
import json
import os
from datetime import datetime

# --- ΡΥΘΜΙΣΕΙΣ API ΚΑΙ ΑΡΧΕΙΩΝ ---
ODDS_API_KEY = os.getenv("ODDS_API_KEY", "eda6dcd0115ab96a2bf0fad47945cd34")
FOOTBALL_DATA_KEY = os.getenv("FOOTBALL_DATA_KEY", "ΤΟ_FOOTBALL_DATA_KEY_ΣΟΥ")

DATA_FILE = "daily_predictions.txt"
HISTORY_FILE = "history.json"

# Λίγκες που παρακολουθούμε
LEAGUES = {
    "ENG_PR": {"odds": "soccer_epl", "fd": "PL"},
    "ENG_CH": {"odds": "soccer_england_championship", "fd": "ELC"},
    "ENG_L1": {"odds": "soccer_england_league1", "fd": "EL1"},
    "ENG_L2": {"odds": "soccer_england_league2", "fd": "EL2"},
    "ESP_LA": {"odds": "soccer_spain_la_liga", "fd": "PD"},
    "ITA_SE": {"odds": "soccer_italy_serie_a", "fd": "SA"},
    "GER_BU": {"odds": "soccer_germany_bundesliga", "fd": "BL1"},
    "FRA_L1": {"odds": "soccer_france_ligue1", "fd": "FL1"},
    "NOR_EL": {"odds": "soccer_norway_eliteserien", "fd": "NOR"},
    "AUT_BU": {"odds": "soccer_austria_bundesliga", "fd": "AUT"},
    "SWE_AL": {"odds": "soccer_sweden_allsvenskan", "fd": "ALL"}
}

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"total": 0, "won": 0, "predictions": {}}

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=4)

def check_past_predictions():
    """Μηχανισμός Auto-Settlement: Ελέγχει τα σκορ για τις εκκρεμείς προβλέψεις"""
    history = load_history()
    if not history["predictions"]:
        return history

    headers = {"X-Auth-Token": FOOTBALL_DATA_KEY}
    updated_any = False

    # Παίρνουμε τα πρόσφατα τελειωμένα ματς από το Football-Data API
    for league_id, league_info in LEAGUES.items():
        fd_code = league_info["fd"]
        url = f"https://api.football-data.org/v4/competitions/{fd_code}/matches?status=FINISHED"
        try:
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                matches = res.json().get("matches", [])
                for m in matches:
                    home_team = m["homeTeam"]["name"]
                    away_team = m["awayTeam"]["name"]
                    match_key = f"{home_team} vs {away_team}"

                    # Αν έχουμε εκκρεμή πρόβλεψη για αυτό το ματς
                    if match_key in history["predictions"] and history["predictions"][match_key]["status"] == "PENDING":
                        home_goals = m["score"]["fullTime"]["home"]
                        away_goals = m["score"]["fullTime"]["away"]
                        
                        if home_goals is json or away_goals is json:
                            continue
                            
                        total_goals = home_goals + away_goals
                        tip = history["predictions"][match_key]["tip"]
                        
                        won = False
                        # Έλεγχος αγοράς Over / Under 2.5
                        if "Over 2.5" in tip and total_goals > 2: won = True
                        elif "Under 2.5" in tip and total_goals < 3: won = True
                        # Έλεγχος αγοράς Goal / Goal
                        elif "Goal / Goal" in tip and home_goals > 0 and away_goals > 0: won = True
                        # Έλεγχος αγοράς 1 (Άσσος)
                        elif "1" in tip and home_goals > away_goals: won = True
                        # Έλεγχος αγοράς Χ2
                        elif "X2" in tip and away_goals >= home_goals: won = True

                        # Ενημέρωση ιστορικού
                        history["predictions"][match_key]["status"] = "WON" if won else "LOST"
                        history["predictions"][match_key]["score"] = f"{home_goals}-{away_goals}"
                        history["total"] += 1
                        if won:
                            history["won"] += 1
                        updated_any = True
        except Exception as e:
            print(f"Σφάλμα κατά το settlement της λίγκας {fd_code}: {e}")

    if updated_any:
        save_history(history)
    return history

def get_dummy_form_and_predict(home, away):
    """Εδώ τρέχει το Poisson σου. Επιστρέφει (Πρόβλεψη, Ποσοστό, Φόρμες)"""
    # Για το παράδειγμα επιστρέφουμε σταθερά data, εδώ έχεις ήδη τον δικό σου Poisson αλγόριθμο
    return "🔥 Over 2.5", "82.5%", "🟢🟢🔴🟢🟡", "🟢🟡🟢🟢🟢"

def main():
    # 1. Έλεγχος και κλείσιμο χθεσινών αγώνων
    history = check_past_predictions()
    
    # Υπολογισμός Live Ποσοστού (αν δεν υπάρχουν ματς, βάζουμε το αρχικό σου 78.4)
    live_rate = (history["won"] / history["total"] * 100) if history["total"] > 0 else 78.4
    live_yield = (history["won"] * 0.2) if history["total"] > 0 else 21.8 # Απλοποιημένο yield
    
    # 2. Τράβηγμα νέων αγώνων από το Odds API
    current_time = datetime.now().strftime("%d/%m/%m %H:%M")
    output_lines = [f"STATS|{live_rate:.1f}|{live_yield:.1f}\n", f"--- ΠΡΟΓΝΩΣΤΙΚΑ {current_time} ---\n"]
    
    # Παράδειγμα Loop (Εδώ μπαίνει το κανονικό loop που τραβάει από το Odds API)
    # Για κάθε νέο ματς που βρίσκει, το αποθηκεύουμε στο history ως PENDING
    # Παράδειγμα εγγραφής στο αρχείο:
    # Πρωτάθλημα | Ομάδες | Ώρα | Πρόβλεψη | Φόρμα1 | Φόρμα2
    
    # Αποθήκευση στο daily_predictions.txt
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        f.writelines(output_lines)
        
    print("Η ενημέρωση ολοκληρώθηκε με επιτυχία!")

if __name__ == "__main__":
    main()

