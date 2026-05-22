import json
import requests
from datetime import datetime

def fetch_todays_matches():
    # Παίρνουμε τη σημερινή ημερομηνία σε μορφή ΥΥΥΥ-ΜΜ-DD
    today_date = datetime.now().strftime("%Y-%m-%d")
    print(f"Λήψη αγώνων για τη σημερινή ημερομηνία: {today_date}")
    
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-matches-by-date"
    querystring = {"date": today_date}

    headers = {
        "x-rapidapi-key": "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561",
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Σφάλμα κατά τη λήψη δεδομένων: {e}")
        return None

def generate_predictions():
    data = fetch_todays_matches()
    if not data:
        print("Δεν βρέθηκαν δεδομένα αγώνων.")
        return

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))
    print("Το αρχείο daily_predictions.txt ενημερώθηκε με τους αγώνες της ημέρας!")

if __name__ == "__main__":
    generate_predictions()
