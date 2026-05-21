import requests
import datetime
from datetime import timedelta
import math
import os

# ==========================================
# 1. ΡΥΘΜΙΣΕΙΣ & ΠΑΡΑΜΕΤΡΟΙ (CONFIGURATION)
# ==========================================
API_KEY = "6be0e4d0ca519a79fa4da6a9089069bf"

LEAGUES_CONFIG = {
    39: "🏴 ΠΡΕΜΙΕΡ ΛΙΓΚ",
    40: "🏴 ΤΣΑΜΠΙΟΝΣΙΠ",
    140: "🇪🇸 ΛΑ ΛΙΓΚΑ",
    135: "🇮🇹 ΣΕΡΙΕ Α",
    78: "🇩🇪 ΜΠΟΥΝΤΕΣΛΙΓΚΑ",
    61: "🇫ΡΑΝΣ ΛΙΓΚ 1",
    88: "🇳🇱 ΟΛΛΑΝΔΙΑ",
    94: "🇵🇹 ΠΟΡΤΟΓΑΛΙΑ",
    71: "🇧🇷 BRAZIL SERIE A",
    13: "🏆 COPA LIBERTADORES",
    2: "🇪🇺 ΤΣΑΜΠΙΟΝΣ ΛΙΓΚ",
    197: "🇬🇷 ΕΛΛΑΔΑ SUPER LEAGUE",
    3: "🇪🇺 EUROPA LEAGUE",
    848: "🇪🇺 CONFERENCE LEAGUE",
    332: "🇨🇾 ΚΥΠΡΟΣ Α ΚΑΤΗΓΟΡΙΑ",
    42: "🏴 LEAGUE TWO (PLAYOFFS)",
    106: "🏴 ΣΚΩΤΙΑ PREMIERSHIP"
}

# ==========================================
# 2. ΜΑΘΗΜΑΤΙΚΟΣ ΥΠΟΛΟΓΙΣΜΟΣ POISSON
# ==========================================
def poisson_probability(lambd, k):
    if lambd <= 0:
        return 0.0
    return (math.exp(-lambd) * (math.exp(k * math.log(lambd)) if k > 0 else 1.0)) / math.factorial(k)

def analyze_match_hybrid(home_stats, away_stats):
    home_attack = home_stats.get('goals', {}).get('for', {}).get('average', {}).get('home', 1.4)
    home_defense = home_stats.get('goals', {}).get('against', {}).get('average', {}).get('home', 1.1)
    away_attack = away_stats.get('goals', {}).get('for', {}).get('average', {}).get('away', 1.1)
    away_defense = away_stats.get('goals', {}).get('against', {}).get('away', 1.4)
    
    try:
        home_attack, home_defense = float(home_attack), float(home_defense)
        away_attack, away_defense = float(away_attack), float(away_defense)
    except:
        home_attack, home_defense, away_attack, away_defense = 1.4, 1.1, 1.1, 1.4

    lambda_home = (home_attack + away_defense) / 2.0
    mu_away = (away_attack + home_defense) / 2.0
    
    home_form_str = home_stats.get('form', '50%').replace('%', '')
    away_form_str = away_stats.get('form', '50%').replace('%', '')
    try:
        home_form = float(home_form_str) / 100.0
        away_form = float(away_form_str) / 100.0
    except:
        home_form, away_form = 0.5, 0.5
        
    lambda_home *= (0.8 + (home_form * 0.4))
    mu_away *= (0.8 + (away_form * 0.4))

    p_1, p_x, p_2, p_under = 0.0, 0.0, 0.0, 0.0
    for h in range(6):
        for a in range(6):
            prob = poisson_probability(lambda_home, h) * poisson_probability(mu_away, a)
            if h > a: p_1 += prob
            elif h == a: p_x += prob
            else: p_2 += prob
            if (h + a) < 2.5: p_under += prob

    p_total = p_1 + p_x + p_2
    if p_total > 0:
        p_1, p_x, p_2, p_under = p_1/p_total, p_x/p_total, p_2/p_total, p_under/p_total
    p_over = 1.0 - p_under

    if p_1 > 0.48:
        main_tip = f"1 & Over 1.5 ({int(p_1*100)}%)" if p_over > 0.55 else f"1 ({int(p_1*100)}%)"
    elif p_2 > 0.48:
        main_tip = f"2 & Over 1.5 ({int(p_2*100)}%)" if p_over > 0.55 else f"2 ({int(p_2*100)}%)"
    elif p_x > 0.35 and p_under > 0.55:
        main_tip = f"X & Under 3.5 ({int(p_x*100)}%)"
    else:
        main_tip = f"Goal/Goal & Over 2.5 ({int(p_over*100)}%)" if p_over > 0.60 else f"Over 1.5 Goals ({int(p_over*100)}%)"

    if "1" in main_tip:
        cover_tip = f"Κάλυψη: 1X Διπλή Ευκαιρία ({int((p_1+p_x)*100)}%)"
    elif "2" in main_tip:
        cover_tip = f"Κάλυψη: X2 Διπλή Ευκαιρία ({int((p_2+p_x)*100)}%)"
    else:
        cover_tip = f"Κάλυψη: Over 1.5 Goals ({int(p_over*100)}%)" if p_over > 0.50 else "Κάλυψη: Under 3.5 Goals"

    return main_tip, cover_tip

# ==========================================
# 3. ΚΥΡΙΑ ΛΕΙΤΟΥΡΓΙΑ (SCANNING 3 DAYS)
# ==========================================
def main():
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
    }
    
    # Εμφανίζει τη σημερινή ημερομηνία στην πορτοκαλί μπάρα
    today_display = datetime.date.today().strftime("%d/%m/%Y")
    now_time = datetime.datetime.now().strftime("%H:%M")
    
    predictions_log = []
    predictions_log.append(f"ΗΜΕΡΟΜΗΝΙΑ|{today_display}|{now_time}")
    
    match_found = False
    
    # Ψάχνει αυτόματα για 3 ημέρες: Σήμερα (0), Αύριο (1), Μεθαύριο (2)
    for day_offset in range(3):
        target_date = datetime.date.today() + timedelta(days=day_offset)
        date_str = target_date.strftime("%Y-%m-%d")
        
        url_fixtures = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?date={date_str}"
        try:
            response = requests.get(url_fixtures, headers=headers)
            if response.status_code != 200: continue
            
            fixtures = response.json().get("response", [])
            for item in fixtures:
                league_id = item.get("league", {}).get("id")
                if league_id in LEAGUES_CONFIG:
                    match_found = True
                    league_name = LEAGUES_CONFIG[league_id]
                    home_team = item.get("teams", {}).get("home", {}).get("name")
                    away_team = item.get("teams", {}).get("away", {}).get("name")
                    
                    raw_date = item.get("fixture", {}).get("date", "")
                    match_time = raw_date[11:16] if len(raw_date) > 16 else "00:00"
                    
                    # Προσθήκη ημέρας στο πλάι του χρόνου (π.χ. "Πέμ" ή "Σάβ")
                    days_map = ["Σήμ", "Αύρ", "Μεθ"]
                    time_label = f"{days_map[day_offset]} {match_time}"
                    
                    home_id = item.get("teams", {}).get("home", {}).get("id")
                    away_id = item.get("teams", {}).get("away", {}).get("id")
                    
                    url_home_stats = f"https://api-football-v1.p.rapidapi.com/v3/teams/statistics?league={league_id}&season=2025&team={home_id}"
                    url_away_stats = f"https://api-football-v1.p.rapidapi.com/v3/teams/statistics?league={league_id}&season=2025&team={away_id}"
                    
                    res_home = requests.get(url_home_stats, headers=headers).json().get("response", {})
                    res_away = requests.get(url_away_stats, headers=headers).json().get("response", {})
                    
                    main_tip, cover_tip = analyze_match_hybrid(res_home, res_away)
                    teams_formatted = f"{home_team} - {away_team}"
                    predictions_log.append(f"{league_name}|{teams_formatted}|{time_label}|{main_tip}|{cover_tip}")
        except Exception as e:
            print(f"Σφάλμα την ημέρα {day_offset}: {e}")

    if not match_found:
        predictions_log.append("INFO|Δεν υπάρχουν προγραμματισμένοι αγώνες.")
        
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        for line in predictions_log:
            f.write(line + "\n")

if __name__ == "__main__":
    main()

