import json
import requests

def fetch_live_matches():
    # Αυτό το endpoint φέρνει ΟΛΟΥΣ τους ζωντανούς αγώνες χωρίς να χρειάζεται ID!
    url = "https://free-api-live-football-data.p.rapidapi.com/football-get-live-all-matches"

    headers = {
        "x-rapidapi-key": "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561",
        "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
    }

    try:
        print("Λήψη όλων των live αγώνων...")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Σφάλμα κατά τη λήψη δεδομένων: {e}")
        return None

def generate_predictions():
    data = fetch_live_matches()
    if not data:
        print("Δεν βρέθηκαν δεδομένα live αγώνων.")
        return

    # Αποθήκευση όλων των live αγώνων στο αρχείο
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write(json.dumps(data, indent=4, ensure_ascii=False))
    print("Το αρχείο daily_predictions.txt ενημερώθηκε με τα live παιχνίδια!")

if __name__ == "__main__":
    generate_predictions()
