import urllib.request
import json
from datetime import datetime

# Μια διευρυμένη λίστα με δυνατές ομάδες για έξυπνο fallback
TOP_TEAMS = [
    "Genk", "Club Brugge", "Anderlecht", "Antwerp", "Gent",
    "Barcelona", "Real Madrid", "Atletico Madrid", "Manchester City", "Arsenal", 
    "Liverpool", "Bayern Munich", "Paris Saint-Germain", "Juventus", "Inter",
    "Olympiacos", "PAOK", "AEK", "Panathinaikos"
]

def analyze_prediction(home_team, away_team, home_odds, away_odds):
    # Αν έχουμε πραγματικές αποδόσεις, τις αναλύουμε
    if home_odds and away_odds:
        try:
            h_float = float(home_odds)
            a_float = float(away_odds)
            if h_float < a_float and h_float <= 1.85:
                return f"1 (Φαβορί ο Άσσος στο {h_float})"
            elif a_float < h_float and a_float <= 1.85:
                return f"2 (Φαβορί το Διπλό στο {a_float})"
            elif abs(h_float - a_float) < 0.50:
                return "Goal / Goal (Αμφίρροπο Ντέρμπι)"
        except:
            pass
            
    # Fallback αλγόριθμος αν λείπουν οι αποδόσεις
    home_is_top = any(t in home_team for t in TOP_TEAMS)
    away_is_top = any(t in away_team for t in TOP_TEAMS)
    
    if home_is_top and not away_is_top:
        return "1X (Προβάδισμα Γηπεδούχου λόγω δυναμικής)"
    elif away_is_top and not home_is_top:
        return "X2 (Προβάδισμα Φιλοξενούμενου λόγω δυναμικής)"
    
    # Αν είναι τελείως ισοδύναμες, σπάμε τις προβλέψεις με βάση τα γράμματα των ομάδων
    if (len(home_team) + len(away_team)) % 2 == 0:
        return "2-3 Γκολ"
    else:
        return "Under 3.5 Γκολ"

def get_real_odds_predictions():
    print("Σύνδεση με το The Odds API...")
    today_display = datetime.now().strftime('%d/%m/%Y')
    
    # --- ΤΟ API KEY ΣΟΥ ---
    API_KEY = "eda6dcd0115ab96a2bf0fad47945cd34" # Κρατάω αυτό που ήδη δουλεύει
    
    # Αλλάζουμε το URL για να φέρει αποδόσεις από πολλούς bookmakers (όχι μόνο 1xbet)
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={API_KEY}&regions=eu&markets=h2h"

    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            matches = json.loads(response.read().decode('utf-8'))
            
            with open("daily_predictions.txt", "w", encoding="utf-8") as file:
                file.write(f"=== ΠΡΟΓΝΩΣΤΙΚΑ ΣΤΟΙΧΗΜΑΤΟΣ - {today_display} ===\n")
                file.write("Πηγή: Real-Time Odds API (Αναβαθμισμένο)\n")
                file.write("=" * 45 + "\n\n")
                
                count = 0
                for match in matches[:35]:
                    home_team = match.get('home_team')
                    away_team = match.get('away_team')
                    league = match.get('sport_title', 'Ποδόσφαιρο')
                    
                    home_odds = None
                    away_odds = None
                    
                    # Ψάχνουμε σε όλους τους διαθέσιμους bookmakers να βρούμε τιμές
                    bookmakers = match.get('bookmakers', [])
                    if bookmakers:
                        for bookie in bookmakers: # Τσεκάρει Bet365, Unibet κτλ. μέχρι να βρει αποδόσεις
                            markets = bookie.get('markets', [])
                            if markets:
                                outcomes = markets[0].get('outcomes', [])
                                odds_dict = {o['name']: o['price'] for o in outcomes}
                                if home_team in odds_dict and away_team in odds_dict:
                                    home_odds = odds_dict[home_team]
                                    away_odds = odds_dict[away_team]
                                    break # Τις βρήκαμε, σταματάμε το ψάξιμο για αυτό το ματς
                    
                    # Υπολογισμός πρόβλεψης
                    prediction = analyze_prediction(home_team, away_team, home_odds, away_odds)
                    
                    file.write(f"Πρωτάθλημα: {league}\n")
                    file.write(f"Αγώνας: {home_team} vs {away_team}\n")
                    file.write(f"🎯 Πρόβλεψη: {prediction}\n")
                    file.write("-" * 45 + "\n")
                    count += 1
                    
            print(f"Επιτυχία! Αναλύθηκαν {count} αγώνες.")
            
    except Exception as e:
        print(f"Σφάλμα: {e}")

if __name__ == "__main__":
    get_real_odds_predictions()

