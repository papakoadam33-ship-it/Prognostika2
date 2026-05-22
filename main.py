import json
import requests

def fetch_match_data():
    # Το ID του αγώνα που θέλεις να αναλύσεις
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
        response.raise_for_status() # Έλεγχος αν το αίτημα ήταν επιτυχές
        return response.json()
    except Exception as e:
        print(f"Σφάλμα κατά τη λήψη δεδομένων: {e}")
        return None

def generate_predictions():
    data = fetch_match_data()
    if not data:
        print("Δεν βρέθηκαν δεδομένα αγώνα.")
        return

    # Αποθήκευση των δομημένων δεδομένων σε κείμενο για την εφαρμογή σου
    # Μπορείς να προσαρμόσεις τι θέλεις να γράφει το αρχείο
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write("=== ΚΑΘΗΜΕΡΙΝΑ ΠΡΟΓΝΩΣΤΙΚΑ ===\n")
        # Παράδειγμα ανάγνωσης βασικών στοιχείων (ανάλογα με τη δομή του συγκεκριμένου API)
        if "status" in data:
            f.write(f"Αποτέλεσμα API: Επιτυχής σύνδεση\n")
        
        # Αποθηκεύουμε όλο το JSON όμορφα μορφοποιημένο μέσα στο txt αρχείο
        f.write("\n--- Αναλυτικά Στατιστικά Αγώνα (JSON) ---\n")
        f.write(json.dumps(data, indent=4, ensure_ascii=False))
    
    print("Το αρχείο daily_predictions.txt ενημερώθηκε επιτυχώς!")

if __name__ == "__main__":
    generate_predictions()

