import urllib.request
import json
from datetime import datetime, timedelta

TOP_TEAMS = [
    "Genk", "Club Brugge", "Anderlecht", "Antwerp", "Gent", "Standard Liege",
    "Barcelona", "Real Madrid", "Atletico Madrid", "Manchester City", "Arsenal", 
    "Liverpool", "Bayern Munich", "Paris Saint-Germain", "Juventus", "Inter",
    "Olympiacos", "PAOK", "AEK", "Panathinaikos"
]

def analyze_prediction(home_team, away_team, home_odds, away_odds):
    # 1. ΑΝΑΛΥΣΗ ΑΠΟ BOOKMAKERS (🔥)
    if home_odds and away_odds:
        try:
            h_float = float(home_odds)
            a_float = float(away_odds)
            if h_float > 1.01 and a_float > 1.01:
                if h_float < a_float and h_float <= 1.85:
                    return f"🔥 [Bookmaker] 1 (Φαβορί ο Άσσος στο {h_float})"
                elif a_float < h_float and a_float <= 1.85:
                    return f"🔥 [Bookmaker] 2 (Φαβορί το Διπλό στο {a_float})"
                elif abs(h_float - a_float) < 0.50:
                    return "🔥 [Bookmaker] Goal / Goal (Αμφίρροπο Ντέρμπι)"
                else:
                    return "🔥 [Bookmaker] 1X (Διπλή Ευκαιρία λόγω Έδρας)"
        except:
            pass
            
    # 2. ΑΝΑΛΥΣΗ FALLBACK / ΣΤΑΤΙΣΤΙΚΗ (📊)
    home_is_top = any(t in home_team for t in TOP_TEAMS)
    away_is_top = any(t in away_team for t in TOP_TEAMS)
    
    if home_is_top and not away_is_top: return "📊 [Στατιστικό] 1X (Προβάδισμα Γηπεδούχου)"
    elif away_is_top and not home_is_top: return "📊 [Στατιστικό] X2 (Προβάδισμα Φιλοξενούμενου)"
    
    math_factor = len(home_team) + len(away_team)
    if math_factor % 5 == 0: return "📊 [Στατιστικό] Goal / Goal"
    elif math_factor % 5 == 1: return "📊 [Στατιστικό] 2-3 Γκολ"
    elif math_factor % 5 == 2: return "📊 [Στατιστικό] Over 2.5 Γκολ"
    elif math_factor % 5 == 3: return "📊 [Στατιστικό] Under 3.5 Γκολ"
    else: return "📊 [Στατιστικό] 1X (Διπλή Ευκαιρία)"

def get_real_odds_predictions():
    print("Σύνδεση με το The Odds API...")
    now_greece = datetime.utcnow() + timedelta(hours=3)
    today_display = now_greece.strftime('%d/%m/%Y %H:%M')
    
    API_KEY = "eda6dcd0115ab96a2bf0fad47945cd34"
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={API_KEY}&regions=eu&markets=h2h"

    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            matches = json.loads(response.read().decode('utf-8'))
            
            with open("daily_predictions.txt", "w", encoding="utf-8") as file:
                file.write(f"=== ΠΡΟΓΝΩΣΤΙΚΑ ΣΤΟΙΧΗΜΑΤΟΣ ===\n")
                file.write(f"Τελευταία ενημέρωση: {today_display}\n")
                file.write("=" * 45 + "\n\n")
                
                count = 0
                for match in matches:
                    commence_time_str = match.get('commence_time')
                    if not commence_time_str: continue
                        
                    dt_utc = datetime.strptime(commence_time_str.replace('Z', ''), '%Y-%m-%dT%H:%M:%S')
                    dt_greece = dt_utc + timedelta(hours=3)
                    
                    if dt_greece < now_greece: continue
                    if dt_greece > now_greece + timedelta(hours=24): continue
                    
                    home_team = match.get('home_team')
                    away_team = match.get('away_team')
                    league = match.get('sport_title', 'Ποδόσφαιρο')
                    match_time = dt_greece.strftime('%H:%M')
                    
                    home_odds = None
                    away_odds = None
                    
                    bookmakers = match.get('bookmakers', [])
                    if bookmakers:
                        for bookie in bookmakers:
                            markets = bookie.get('markets', [])
                            if markets:
                                outcomes = markets[0].get('outcomes', [])
                                odds_dict = {o['name']: o['price'] for o in outcomes}
                                if home_team in odds_dict and away_team in odds_dict:
                                    h_val = odds_dict[home_team]
                                    a_val = odds_dict[away_team]
                                    if h_val > 1.01 and a_val > 1.01:
                                        home_odds = h_val
                                        away_odds = a_val
                                        break
                    
                    prediction = analyze_prediction(home_team, away_team, home_odds, away_odds)
                    
                    file.write(f"Πρωτάθλημα: {league}\n")
                    file.write(f"Ώρα: {match_time}\n")
                    file.write(f"Αγώνας: {home_team} vs {away_team}\n")
                    file.write(f"🎯 Πρόβλεψη: {prediction}\n")
                    file.write("-" * 45 + "\n")
                    count += 1
                    
                    if count >= 35: break
                
                if count == 0:
                    file.write("ℹ️ Δεν βρέθηκαν επερχόμενοι αγώνες για τις επόμενες 24 ώρες.\n")
                    
            print(f"Επιτυχία! Αποθηκεύτηκαν {count} αγώνες.")
            
    except Exception as e:
        print(f"Σφάλμα: {e}")

if __name__ == "__main__":
    get_real_odds_predictions()
