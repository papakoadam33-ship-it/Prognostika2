import json
import requests
from datetime import datetime

def fetch_todays_matches():
    # 1. Παίρνει αυτόματα τη σημερινή ημερομηνία σε μορφή ΥΥΥΥ-ΜΜ-DD (π.χ. 2026-05-22)
    today_date = datetime.now().strftime("%Y-%m-%d")
    
    # Αλλάζουμε το endpoint για να πάρουμε τη λίστα των αγώνων της ημέρας
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-matches-by-date"
    querystring = {"date": today_date}

    headers = {
        "x-rapidapi-key": "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561",
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }

    try:
        print(f"Λήψη αγώνων για τη σημερινή ημερομηνία: {today_date}...")
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        return response.json(), today_date
    except Exception as e:
        print(f"Σφάλμα κατά τη λήψη δεδομένων: {e}")
        return None, today_date

def generate_predictions():
    data, today_date = fetch_todays_matches()
    if not data:
        print("Δεν βρέθηκαν δεδομένα για σήμερα.")
        return

    # Αποθήκευση των νέων δεδομένων στο αρχείο
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(f"=== ΚΑΘΗΜΕΡΙΝΑ ΠΡΟΓΝΩΣΤΙΚΑ ({today_date}) ===\n")
        f.write("--- Αναλυτικά Στατιστικά Αγώνα (JSON) ---\n")
        f.write(json.dumps(data, indent=4, ensure_ascii=False))
    
    print("Το αρχείο daily_predictions.txt ενημερώθηκε με τα σημερινά ματς!")

if __name__ == "__main__":
    generate_predictions()

