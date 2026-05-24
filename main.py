import requests
import json
from datetime import datetime, timedelta
import random

# Αντικατάστησε με το δικό σου πραγματικό API Key
API_KEY = 'YOUR_ODDS_API_KEY' 
SPORT = 'upcoming' 
REGIONS = 'eu' 
MARKETS = 'h2h' 
ODDS_FORMAT = 'decimal'

def generate_random_form():
    """Δημιουργεί μια τυχαία φόρμα 5 αγώνων για τις ομάδες"""
    options = ['🟢', '🟢', '🟡', '🔴', '🟢']
    return "".join(random.choices(options, k=5))

def get_football_predictions():
    url = f'https://api.the-odds-api.com/v4/sports/soccer/odds/'
    params = {
        'apiKey': API_KEY,
        'regions': REGIONS,
        'markets': MARKETS,
        'oddsFormat': ODDS_FORMAT,
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f'Σφάλμα API: {response.status_code}')
            return []
        return response.json()
    except Exception as e:
        print(f"Σφάλμα κατά τη σύνδεση: {e}")
        return []

def analyze_matches():
    matches = get_football_predictions()
    if not matches:
        return
    
    output_lines = []
    now_utc = datetime.utcnow()
    athens_offset = timedelta(hours=3) # Θερινή ώρα Ελλάδος
    now_athens = now_utc + athens_offset
    
    output_lines.append(f"Τελευταία ενημέρωση: {now_athens.strftime('%d/%m/%Y %H:%M')}")
    output_lines.append("---------------------------------------------")
    
    for match in matches:
        home_team = match.get('home_team')
        away_team = match.get('away_team')
        league = match.get('sport_title')
        commence_time_str = match.get('commence_time')
        
        # Μετατροπή ώρας σε Ελλάδος
        match_time_utc = datetime.strptime(commence_time_str, "%Y-%m-%dT%H:%M:%SZ")
        match_time_athens = match_time_utc + athens_offset
        
        # Φιλτράρισμα: Μόνο μελλοντικοί αγώνες για σήμερα
        if match_time_athens.date() != now_athens.date() or match_time_athens < now_athens:
            continue
            
        time_display = match_time_athens.strftime("%H:%M")
        
        # Εύρεση αποδόσεων
        home_odds, away_odds, draw_odds = None, None, None
        bookmakers = match.get('bookmakers', [])
        
        if bookmakers:
            markets = bookmakers[0].get('markets', [])
            if markets:
                outcomes = markets[0].get('outcomes', [])
                for outcome in outcomes:
                    if outcome['name'] == home_team:
                        home_odds = outcome['price']
                    elif outcome['name'] == away_team:
                        away_odds = outcome['price']
                    elif outcome['name'] in ['Draw', 'Διαγραφή', 'Ισοπαλία']:
                        draw_odds = outcome['price']
                        
        if not home_odds or not away_odds:
            continue
            
        # Αλγόριθμος VIP Προγνωστικών
        prediction = ""
        if home_odds < 1.45:
            prediction = f"🔥 [Bookmaker] 1 (Φαβορί ο Άσσος στο {home_odds})"
        elif away_odds < 1.45:
            prediction = f"🔥 [Bookmaker] 2 (Φαβορί το Διπλό στο {away_odds})"
        elif 1.45 <= home_odds <= 1.85:
            prediction = f"🔥 [Bookmaker] 1X (Διπλή Ευκαιρία λόγω Έδρας)"
        elif 1.45 <= away_odds <= 1.85:
            prediction = f"🔥 [Bookmaker] X2 (Διπλή Ευκαιρία για το Διπλό)"
        else:
            prediction = "📊 [Στατιστικό] Goal / Goal (Αμφίρροπο Ντέρμπι)"
            
        # Δημιουργία Φόρμας
        home_form = generate_random_form()
        away_form = generate_random_form()
        
        output_lines.append(f"Πρωτάθλημα: {league}")
        output_lines.append(f"Ώρα: {time_display}")
        output_lines.append(f"Αγώνας: {home_team} vs {away_team}")
        output_lines.append(f"Φόρμα_Home: {home_form}")
        output_lines.append(f"Φόρμα_Away: {away_form}")
        output_lines.append(f"🎯 Πρόβλεψη: {prediction}")
        output_lines.append("---------------------------------------------")
        
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))
    print("Τα προγνωστικά και η φόρμα ενημερώθηκαν επιτυχώς!")

if __name__ == "__main__":
    analyze_matches()

