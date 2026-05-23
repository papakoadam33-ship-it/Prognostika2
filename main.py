import urllib.request
import json
from datetime import datetime

def get_real_odds_predictions():
    print("Σύνδεση με το The Odds API για πραγματικούς σημερινούς αγώνες...")
    today_display = datetime.now().strftime('%d/%m/%Y')
    
    # --- ΒΑΛΕ ΤΟ ΔΙΚΟ ΣΟΥ API KEY ΕΔΩ ---
    API_KEY = "ΤΟ_ΚΛΕΙΔΙ_ΠΟΥ_ΣΟΥ_ΕΣΤΕΙΛΑΝ_ΣΤΟ_EMAIL"
    
    # Ζητάμε τους σημερινούς αγώνες ποδοσφαίρου παγκοσμίως (soccer) μαζί με αποδόσεις
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={API_KEY}&regions=eu&markets=h2h&bookmakers=onexbet"

    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read()
            matches = json.loads(html.decode('utf-8'))
            
            with open("daily_predictions.txt", "w", encoding="utf-8") as file:
                file.write(f"=== ΠΡΟΓΝΩΣΤΙΚΑ ΣΤΟΙΧΗΜΑΤΟΣ - {today_display} ===\n")
                file.write("Πηγή: Real-Time Odds API\n")
                file.write("=" * 45 + "\n\n")
                
                if not matches or not isinstance(matches, list):
                    file.write("Δεν βρέθηκαν διαθέσιμοι αγώνες για σήμερα στο API.\n")
                    return
                
                count = 0
                for match in matches[:30]: # Παίρνουμε έως 30 πραγματικούς αγώνες
                    home_team = match.get('home_team')
                    away_team = match.get('away_team')
                    league = match.get('sport_title', 'Ποδόσφαιρο')
                    
                    # Προσπάθεια εύρεσης πραγματικών αποδόσεων για έξυπνο προγνωστικό
                    prediction = "1X (Διπλή Ευκαιρία)" # default
                    try:
                        bookmaker = match.get('bookmakers', [])[0]
                        market = bookmaker.get('markets', [])[0]
                        outcomes = market.get('outcomes', [])
                        
                        # outcomes[0] = home, outcomes[1] = away, outcomes[2] = draw (συνήθως)
                        odds_dict = {o['name']: o['price'] for o in outcomes}
                        home_odds = odds_dict.get(home_team, 2.0)
                        away_odds = odds_dict.get(away_team, 2.0)
                        
                        if home_odds < away_odds and home_odds < 1.80:
                            prediction = f"1 (Άσσος με απόδοση {home_odds})"
                        elif away_odds < home_odds and away_odds < 1.80:
                            prediction = f"2 (Διπλό με απόδοση {away_odds})"
                        else:
                            prediction = "Goal / Goal ή Χ (Ντέρμπι)"
                    except:
                        pass
                    
                    file.write(f"Πρωτάθλημα: {league}\n")
                    file.write(f"Αγώνας: {home_team} vs {away_team}\n")
                    file.write(f"🎯 Πρόβλεψη: {prediction}\n")
                    file.write("-" * 45 + "\n")
                    count += 1
                    
            print(f"Επιτυχία! Γράφτηκαν {count} ΠΡΑΓΜΑΤΙΚΟΙ σημερινοί αγώνες.")
            
    except Exception as e:
        print(f"Σφάλμα κατά την κλήση του API: {e}")
        with open("daily_predictions.txt", "w", encoding="utf-8") as file:
            file.write(f"=== ΠΡΟΓΝΩΣΤΙΚΑ ΣΤΟΙΧΗΜΑΤΟΣ - {today_display} ===\n\n")
            file.write("Σφάλμα σύνδεσης. Παρακαλώ ελέγξτε αν το API Key σας είναι σωστό.\n")

if __name__ == "__main__":
    get_real_odds_predictions()
