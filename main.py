import requests
from datetime import datetime

def get_free_predictions():
    print("Έναρξη συλλογής αγώνων από όλα τα πρωταθλήματα...")
    
    # Χρησιμοποιούμε ένα 100% ελεύθερο και ανοιχτό API που επιστρέφει live/σημερινούς αγώνες
    url = "https://api.football-data.org/v4/matches"
    
    # Επειδή το παραπάνω θέλει registration για πλήρη χρήση, πάμε στην απόλυτη no-key λύση:
    # Τραβάμε δεδομένα από το ανοιχτό feed της ScoreBat που έχει όλα τα παιχνίδια live και επερχόμενα
    url_free = "https://www.scorebat.com/video-api/v3/"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        response = requests.get(url_free, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            matches = data.get('response', [])
            
            if not matches:
                print("Δεν βρέθηκαν αυτούσιοι αγώνες αυτή τη στιγμή.")
                return
                
            # Άνοιγμα και εγγραφή στο daily_predictions.txt
            with open("daily_predictions.txt", "w", encoding="utf-8") as file:
                file.write(f"=== ΠΡΟΓΝΩΣΤΙΚΑ ΣΤΟΙΧΗΜΑΤΟΣ - {datetime.now().strftime('%d/%m/%Y')} ===\n")
                file.write("Χωρίς Όρια & Χωρίς API Κλειδιά\n")
                file.write("=" * 40 + "\n\n")
                
                count = 0
                for match in matches[:40]: # Παίρνουμε τους πρώτους 40 αγώνες παγκοσμίως
                    title = match.get('title', '') # Σου δίνει έτοιμο το "Team A - Team B"
                    competition = match.get('competition', '')
                    
                    if " - " in title:
                        home_team, away_team = title.split(" - ", 1)
                    else:
                        continue
                        
                    # Απλός αλγόριθμος πρόβλεψης (Προγνωστικό)
                    # Μπορείς να αλλάξεις τη λογική εδώ. Βάζουμε Goal/Goal ή 1Χ ως default.
                    prediction = "Goal / Goal" if count % 2 == 0 else "1X (Διπλή Ευκαιρία)"
                    
                    # Μορφοποίηση κειμένου
                    output = f"Πρωτάθλημα: {competition}\n"
                    output += f"Αγώνας: {home_team} vs {away_team}\n"
                    output += f"🎯 Πρόβλεψη: {prediction}\n"
                    output += "-" * 40 + "\n"
                    
                    file.write(output)
                    count += 1
                    
            print(f"Επιτυχία! {count} αγώνες αποθηκεύτηκαν στο daily_predictions.txt")
        else:
            print(f"Το feed απέτυχε με status code: {response.status_code}")
            
    except Exception as e:
        print(f"Σφάλμα κατά την εκτέλεση: {e}")
        # Δημιουργία safe αρχείου σε περίπτωση που πέσει το internet ή το API
        with open("daily_predictions.txt", "w", encoding="utf-8") as file:
            file.write("Το σύστημα ανανεώνεται αυτόματα. Παρακαλώ ελέγξτε σε λίγο.")

if __name__ == "__main__":
    get_free_predictions()

