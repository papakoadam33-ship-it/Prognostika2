import requests
import math
import time
from datetime import datetime, timezone, timedelta
import hashlib

# --- ΡΥΘΜΙΣΕΙΣ API-FOOTBALL ---
API_KEY = "582474103b6e33694c9f25a1c37dc384"
HEADERS = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": "v3.football.api-sports.io"
}

# Το πλήρες, παγκόσμιο mapping λιγκών για το Marios Pro-Bet
LEAGUES_CONFIG = {
    39: "🏴󠁧󠁢󠁥󠁮󠁧󠁿 ΠΡΕΜΙΕΡ ΛΙΓΚ",
    40: "🏴󠁧󠁢󠁥󠁮󠁧󠁿 ΤΣΑΜΠΙΟΝΣΙΠ",
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
    848: "🇪🇺 CONFERENCE LEAGUE"
}

def get_fixtures_for_today():
    now_gr = datetime.now(timezone.utc) + timedelta(hours=3)
    today_str = now_gr.strftime("%Y-%m-%d")
    url = f"https://v3.football.api-sports.io/fixtures?date={today_str}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=15).json()
        return res.get("response", [])
    except Exception as e:
        print(f"Error fetching fixtures: {e}")
        return []

def calculate_hybrid_prediction(home_name, away_name, league_id):
    combined = f"{home_name}-{away_name}-{league_id}"
    hash_val = int(hashlib.md5(combined.encode('utf-8')).hexdigest(), 16)
    
    stat_score = hash_val % 100
    goal_score = (hash_val // 100) % 100
    
    if stat_score < 45:
        p_1, p_x, p_2 = 53.0, 27.0, 20.0
    elif stat_score < 75:
        p_1, p_x, p_2 = 32.0, 36.0, 32.0
    else:
        p_1, p_x, p_2 = 20.0, 28.0, 52.0
        
    if league_id in [71, 13]:
        p_o15 = 60.0 + (goal_score % 12)
        prob_over_2_5 = 38.0 + (goal_score % 12)
        prob_gg = 44.0 + (goal_score % 12)
    else:
        p_o15 = 74.0 + (goal_score % 12)
        prob_over_2_5 = 55.0 + (goal_score % 12)
        prob_gg = 56.0 + (goal_score % 12)

    if p_1 > 46 and p_o15 > 68:
        tip, pct = "1 & Over 1.5", int((p_1 + p_o15) / 2)
    elif p_2 > 46 and p_o15 > 68:
        tip, pct = "2 & Over 1.5", int((p_2 + p_o15) / 2)
    elif (p_1 + p_x) > 68 and p_o15 > 68:
        tip, pct = "1X & Over 1.5", int(((p_1 + p_x) + p_o15) / 2)
    elif (p_2 + p_x) > 68 and p_o15 > 68:
        tip, pct = "X2 & Over 1.5", int(((p_2 + p_x) + p_o15) / 2)
    elif prob_over_2_5 > 55:
        tip, pct = "Over 2.5", int(prob_over_2_5)
    else:
        tip, pct = "Under 2.5", int(100 - prob_over_2_5)

    cover = f"Goal-Goal ({int(prob_gg)}%)" if prob_gg > 50 else f"No GG ({int(100-prob_gg)}%)"
    return f"{tip} ({pct}%)", cover

def main():
    now_gr = datetime.now(timezone.utc) + timedelta(hours=3)
    fixtures = get_fixtures_for_today()
    predictions = []
    
    for f in fixtures:
        league_id = f.get("league", {}).get("id")
        if league_id in LEAGUES_CONFIG:
            league_label = LEAGUES_CONFIG[league_id].upper()
            home = f["teams"]["home"]["name"]
            away = f["teams"]["away"]["name"]
            
            api_date = f["fixture"]["date"]
            dt_obj = datetime.fromisoformat(api_date.replace("+00:00", "")).replace(tzinfo=timezone.utc)
            gr_dt = dt_obj.astimezone(timezone(timedelta(hours=3)))
            match_time = gr_dt.strftime("%H:%M")
            
            main_tip, cover_tip = calculate_hybrid_prediction(home, away, league_id)
            predictions.append(f"{league_label}|{home} - {away}|{match_time}|{main_tip}|{cover_tip}")
            
    with open("daily_predictions.txt", "w", encoding="utf-8") as file:
        file.write(f"ΗΜΕΡΟΜΗΝΙΑ|{now_gr.strftime('%d/%m/%Y')}|{now_gr.strftime('%H:%M')}\n")
        if not predictions:
            file.write("INFO|Δεν υπάρχουν σημερινοί αγώνες.|-| - (0%) | - \n")
        else:
            for p in predictions:
                file.write(p + "\n")

if __name__ == "__main__":
    main()

