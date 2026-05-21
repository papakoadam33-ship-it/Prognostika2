import requests
import datetime
import math
import os

# ==========================================
# 1. ΡΥΘΜΙΣΕΙΣ & ΠΑΡΑΜΕΤΡΟΙ (CONFIGURATION)
# ==========================================
API_KEY = "6be0e4d0ca519a79fa4da6a9089069bf"  # Το δικό σου API Key στο API-Football

# Λίστα με όλα τα υποστηριζόμενα πρωταθλήματα και τα ID τους
LEAGUES_CONFIG = {
    39: "🏴" + "         ΠΡΕΜΙΕΡ ΛΙΓΚ",
    40: "🏴" + "         ΤΣΑΜΠΙΟΝΣΙΠ",
    140: "🇪🇸 ΛΑ ΛΙΓΚΑ",
    135: "🇮🇹 ΣΕΡΙΕ Α",
    78: "🇩🇪 ΜΠΟΥΝΤΕΣΛΙΓΚΑ",
    61: "🇫🇷 ΛΙΓΚ 1",
    88: "🇳🇱 ΟΛΛΑΝΔΙΑ",
    94: "🇵🇹 ΠΟΡΤΟΓΑΛΙΑ",
    71: "🇧🇷 BRAZIL SERIE A",
    13: "🏆 COPA LIBERTADORES",
    2: "🇪🇺 ΤΣΑΜΠΙΟΝΣ ΛΙΓΚ",
    197: "🇬🇷 ΕΛΛΑΔΑ SUPER LEAGUE",
    3: "🇪🇺 EUROPA LEAGUE",
    848: "🇪🇺 CONFERENCE LEAGUE",
    332: "🇨🇾 ΚΥΠΡΟΣ Α ΚΑΤΗΓΟΡΙΑ",
    42: "🏴" + "         LEAGUE TWO (PLAYOFFS)",
    106: "🏴" + "         ΣΚΩΤΙΑ PREMIERSHIP"
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
        home_attack = float(home_attack)
        home_defense = float(home_defense)
        away_attack = float(away_attack)
        away_defense = float(away_defense)
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

    p_1, p_x, p_2 = 0.0, 0.0, 0.0
    p_under = 0.0
    
    for h in range(6):
        for a in range(6):
            prob = poisson_probability(lambda_home, h) * poisson_probability(mu_away, a)
            if h > a:
                p_1 += prob
            elif h == a:
                p_x += prob
            else:
                p_2 += prob
                
            if (h + a) < 2.5:
                p_under += prob

    p_total = p_1 + p_x + p_2
    if p_total > 0:
        p_1 /= p_total
        p_x /= p_total
        p_2 /= p_total
        p_under /= p_total
        
    p_over = 1.0 - p_under

    if p_1 > 0.48:
        main_tip = f"1 & Over 1.5 ({int(p_1*100)}%)" if p_over > 0.55 else f"1 ({int(p_1*100)}%)"
    elif p_2 > 0.48:
        main_tip = f"2 & Over 1.5 ({int(p_2*100)}%)" if p_over > 0.55 else f"2 ({int(p_2*100)}%)"
    elif p_x > 0.35 and p_under > 0.55:
        main_tip = f"X & Under 3.5 ({int(p_x*100)}%)"
    else:
        if p_over > 0.60:
            main_tip = f"Goal/Goal & Over 2.5 ({int(p_over*100)}%)"
        else:
            main_tip = f"Over 1.5 Goals ({int(p_over*100)}%)"

    if "1" in main_tip:
        cover_tip = f"Κάλυψη: 1X Διπλή Ευκαιρία ({int((p_1+p_x)*100)}%)"
    elif "2" in main_tip:
        cover_tip = f"Κάλυψη: X2 Διπλή Ευκαιρία ({int((p_2+p_x)*100)}%)"
    else:
        cover_tip = f"Κάλυψη: Over 1.5 Goals ({int(p_over*100)}%)" if p_over > 0.50 else "Κάλυψη: Under 3.5 Goals"

    return main_tip, cover_tip

# ==========================================
# 3. ΚΥΡΙΑ ΛΕΙΤΟΥΡΓΙΑ ΑΝΤΛΗΣΗΣ & ΑΝΑΛΥΣΗΣ
# ==========================================
def main():
    headers = {
        "x-rapidapi-key": API_KEY,
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
    }
    
    # ΤΕΣΤ: Κοιτάμε 2 μέρες μπροστά για να βρούμε σίγουρα αγώνες Σαββατοκύριακου
    today_date = datetime.date.today() + datetime.timedelta(days=2)
    date_str = today_date.strftime("%Y-%m-%d")
    display_date = today_date.strftime("%d/%m/%Y")
    now_time = datetime.datetime.now().strftime("%H:%M")
    
    print(f"Έναρξη ανάλυσης για την ημερομηνία: {display_date} στις {now_time}")
    
    predictions_log = []
    predictions_log.append(f"ΗΜΕΡΟΜΗΝΙΑ|{display_date}|{now_time}")
    
    url_fixtures = f"https://api-football-v1.p.rapidapi.com/v3/fixtures?date={date_str}"
    
    try:
        response = requests.get(url_fixtures, headers=headers)
        if response.status_code != 200:
            print("Σφάλμα κατά την επικοινωνία με το API.")
            return
            
        data = response.json()
        fixtures = data.get("response", [])
        
        match_found = False
        
        for item in fixtures:
            league_id = item.get("league", {}).get("id")
            
            if league_id in LEAGUES_CONFIG:
                match_found = True
                league_name = LEAGUES_CONFIG[league_id]
                
                home_team = item.get("teams", {}).get("home", {}).get("name")
                away_team = item.get("teams", {}).get("away", {}).get("name")
                
                raw_date = item.get("fixture", {}).get("date", "")
                match_time = raw_date[11:16] if len(raw_date) > 16 else "00:00"
                
                home_id = item.get("teams", {}).get("home", {}).get("id")
                away_id = item.get("teams", {}).get("away", {}).get("id")
                
                # ΕΞΥΠΝΟΣ ΥΠΟΛΟΓΙΣΜΟΣ ΣΕΖΟΝ
                raw_season = item.get("league", {}).get("season")
                if league_id in [2, 3, 848, 39, 40, 140, 135, 78, 61, 88, 94, 197, 332, 42, 106]:
                    season = 2025
                else:
                    season = raw_season if raw_season else today_date.year
                
                print(f"Ανάλυση: {league_name} (Σεζόν: {season}) -> {home_team} vs {away_team}")
                
                url_home_stats = f"https://api-football-v1.p.rapidapi.com/v3/teams/statistics?league={league_id}&season={season}&team={home_id}"
                url_away_stats = f"https://api-football-v1.p.rapidapi.com/v3/teams/statistics?league={league_id}&season={season}&team={away_id}"
                
                res_home = requests.get(url_home_stats, headers=headers).json()
                res_away = requests.get(url_away_stats, headers=headers).json()
                
                home_stats = res_home.get("response", {})
                away_stats = res_away.get("response", {})
                
                main_tip, cover_tip = analyze_match_hybrid(home_stats, away_stats)
                
                teams_formatted = f"{home_team} - {away_team}"
                predictions_log.append(f"{league_name}|{teams_formatted}|{match_time}|{main_tip}|{cover_tip}")
        
        if not match_found:
            predictions_log.append("INFO|Δεν υπάρχουν προγραμματισμένοι αγώνες.")
            print("Δεν βρέθηκαν προγραμματισμένοι αγώνες για σήμερα.")
            
    except Exception as e:
        print(f"Προέκυψε σφάλμα: {e}")
        predictions_log.append("INFO|Σφάλμα κατά την εκτέλεση της ανάλυσης.")
        
    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        for line in predictions_log:
            f.write(line + "\n")
            
    print("Το αρχείο daily_predictions.txt ενημερώθηκε επιτυχώς!")

if __name__ == "__main__":
    main()

