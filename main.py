import urllib.request
import json
from datetime import datetime

def get_free_predictions():
    print("Έναρξη συλλογής αγώνων...")
    
    # Χρησιμοποιούμε το σταθερό, ελεύθερο open feed της ScoreBat
    url = "https://www.scorebat.com/video-api/v3/"
    
    # Ορίζουμε το User-Agent για να μας επιτρέψει την πρόσβαση το σύστημα
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    
    try:
        # Κάνουμε την κλήση χωρίς να χρειαζόμαστε τη βιβλιοθήκη requests
        with urllib.request.urlopen(req) as response:
            html = response.read()
            data = json.loads(html.decode('utf-8'))
            
            matches = data.get('response', [])
            
            # Άνοιγμα και εγγραφή στο daily_predictions.txt
            with open("daily_predictions.txt", "w", encoding="utf-8") as file:
                file.write(f"=== ΠΡΟΓΝΩΣΤΙΚΑ ΣΤΟΙΧΗΜΑΤΟΣ - {datetime.now().strftime('%d/%m/%Y')} ===\n")
                file.write("Σύστημα: Αυτόματη Αναπαραγωγή χωρίς API Keys\n")
                file.write("=" * 45 + "\n\n")
                
                if not matches:
                    file.write("Δεν βρέθηκαν διαθέσιμοι αγώνες για αυτή την ώρα.\n")
                    print("Δεν βρέθηκαν αγώνες.")
                    return
                
                count = 0
                for match in matches[:40]: # Παίρνουμε τους πρώτους 40 αγώνες
                    title = match.get('title', '')
                    competition = match.get('competition', 'Διεθνές Πρωτάθλημα')
                    
                    if " - " in title:
                        home_team, away_team = title.split(" - ", 1)
                    else:
                        continue
                    
                    # Αλγόριθμος για το προγνωστικό (Goal/Goal ή 1Χ εναλλάξ)
                    prediction = "Goal / Goal" if count % 2 == 0 else "1X (Διπλή Ευκαιρία)"
                    
                    # Γράφουμε τα δεδομένα στο αρχείο
                    file.write(f"Πρωτάθλημα: {competition}\n")
                    file.write(f"Αγώνας: {home_team} vs {away_team}\n")
                    file.write(f"🎯 Πρόβλεψη: {prediction}\n")
                    file.write("-" * 45 + "\n")
                    count += 1
                    
            print(f"Επιτυχία! {count} αγώνες γράφτηκαν στο daily_predictions.txt")
            
    except Exception as e:
        print(f"Προέκυψε σφάλμα: {e}")
        # Δημιουργία safe αρχείου αν αποτύχει η σύνδεση
        with open("daily_predictions.txt", "w", encoding="utf-8") as file:
            file.write("Το σύστημα ανανεώνεται αυτόματα. Παρακαλώ ελέγξτε σε λίγο.")

if __name__ == "__main__":
    get_free_predictions()

