import urllib.request
import json
from datetime import datetime, timedelta

# Λίστα με γνωστές/δυνατές ομάδες για έξυπνο fallback
TOP_TEAMS = [
    "Genk", "Club Brugge", "Anderlecht", "Antwerp", "Gent", "Standard Liege",
    "Barcelona", "Real Madrid", "Atletico Madrid", "Manchester City", "Arsenal", 
    "Liverpool", "Bayern Munich", "Paris Saint-Germain", "Juventus", "Inter",
    "Olympiacos", "PAOK", "AEK", "Panathinaikos"
]

def analyze_prediction(home_team, away_team, home_odds, away_odds):
    # 1. Αν υπάρχουν έγκυρες αποδόσεις, βγάζουμε σημείο βάσει των bookmakers
    if home_odds and away_odds:
        try:
            h_float = float(home_odds)
            a_float = float(away_odds)
            if h_float > 1.01 and a_float > 1.01:
                if h_float < a_float and h_float <= 1.85:
                    return f"1 (Φαβορί ο Άσσος στο {h_float})"
                elif a_float < h_float and a_float <= 1.85:
                    return f"2 (Φαβορί το Διπλό στο {a_float})"
                elif abs(h_float - a_float) < 0.50:
                    return "Goal / Goal (Αμφίρροπο Ντέρμπι)"
                else:
                    return "1X (Διπλή Ευκαιρία λόγω Έδρας)"
        except:
            pass
            
    # 2. ΠΟΛΥΠΟΙΚΙΛΟ FALLBACK (Όταν οι αποδόσεις είναι κλειδωμένες ή λείπουν)
    home_is_top = any(t in home_team for t in TOP_TEAMS)
    away_is_top = any(t in away_team for t in TOP_TEAMS)
    
    if home_is_top and not away_is_top: return "1X (Προβάδισμα Γηπεδούχου)"
    elif away_is_top and not home_is_top: return "X2 (Προβάδισμα Φιλοξενούμενου)"
    
    # Χρήση των γραμμάτων των ομάδων για τυχαία αλλά σταθερή κατανομή σημείων
    math_factor = len(home_team) + len(away_team)
    if math_factor % 5 == 0: return "Goal / Goal"
    elif math_factor % 5 == 1: return "2-3 Γκολ"
    elif math_factor % 5 == 2: return "Over 2.5 Γκολ"
    elif math_factor % 5 == 3: return "Under 3.5 Γκολ"
    else: return "1X (Διπλή Ευκαιρία)"

def get_real_odds_predictions():
    print("Σύνδεση με το The Odds API...")
    now_greece = datetime.utcnow() + timedelta(hours=3) # Τρέχουσα ώρα Ελλάδας
    today_display = now_greece.strftime('%d/%m/%Y')
    
    API_KEY = "3a00f2efbe3a10972c84fd43d2c67e81"
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={API_KEY}&regions=eu&markets=h2h"

    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            matches = json.loads(response.read().decode('utf-8'))
            
            with open("daily_predictions.txt", "w", encoding="utf-8") as file:
                file.write(f"=== ΠΡΟΓΝΩΣΤΙΚΑ ΣΤΟΙΧΗΜΑΤΟΣ - {today_display} ===\n")
                file.write("Φίλτρο: Μόνο Σημερινοί Αγώνες (Επερχόμενοι)\n")
                file.write("=" * 45 + "\n\n")
                
                count = 0
                for match in matches:
                    commence_time_str = match.get('commence_time')
                    if not commence_time_str:
                        continue
                        
                    # Μετατροπή ώρας αγώνα σε ώρα Ελλάδας
                    dt_utc = datetime.strptime(commence_time_str.replace('Z', ''), '%Y-%m-%dT%H:%M:%S')
                    dt_greece = dt_utc + timedelta(hours=3)
                    
                    # ΦΙΛΤΡΟ 1: Μόνο σημερινοί αγώνες
                    if dt_greece.date() != now_greece.date():
                        continue
                        
                    # ΦΙΛΤΡΟ 2: Μόνο αγώνες που ΔΕΝ έχουν ξεκινήσει ακόμα
                    if dt_greece < now_greece:
                        continue
                    
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
                    
                    if count >= 35: # Όριο για να μην είναι τεράστια η σελίδα
                        break
                
                if count == 0:
                    file.write("ℹ️ Όλοι οι σημερινοί αγώνες έχουν ολοκληρωθεί ή ξεκινήσει.\n")
                    file.write("Νέα ανανέωση με το αυριανό πρόγραμμα θα γίνει αυτόματα το πρωί.\n")
                    
            print(f"Επιτυχία! Αποθηκεύτηκαν {count} σημερινοί αγώνες.")
            
    except Exception as e:
        print(f"Σφάλμα: {e}")

if __name__ == "__main__":
    get_real_odds_predictions()

