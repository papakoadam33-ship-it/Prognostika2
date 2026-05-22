import json
import requests

def fetch_match_data():
    # Εδώ βάζεις το ID του αγώνα που θέλεις να δείξεις (π.χ. για live ή επερχόμενο ματς)
    match_id = "4621624" 
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-match-detail"
    querystring = {"eventid": match_id}

    headers = {
        "x-rapidapi-key": "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561",
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }

    try:
        print(f"Λήψη δεδομένων για τον αγώνα {match_id}...")
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Σφάλμα κατά τη λήψη δεδομένων: {e}")
        return None

def generate_predictions():
    data = fetch_match_data()
    if not data:
        print("Δεν βρέθηκαν δεδομένα.")
        return

    # Αποθήκευση του καθαρού JSON στο αρχείο daily_predictions.txt
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))
    print("Το αρχείο daily_predictions.txt ενημερώθηκε!")

if __name__ == "__main__":
    generate_predictions()
