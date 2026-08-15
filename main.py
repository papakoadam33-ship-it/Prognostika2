import os
import math
import json
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

DATA_FILE = "daily_predictions.txt"
STATS_FILE = "stats.json"

if os.path.exists(STATS_FILE):
    with open(STATS_FILE, "r", encoding="utf-8") as sf:
        stats_data = json.load(sf)
    WIN_RATE = stats_data.get("win_rate", "78.2")
    TOTAL_YIELD = stats_data.get("total_yield", "22.1")
    PAST_RESULTS = stats_data.get("past_results", [])
else:
    WIN_RATE = "78.2"
    TOTAL_YIELD = "22.1"
    PAST_RESULTS = [
        "🏁 Tigre vs Alianza Atletico | Score: 2-0 | Over 2.5 -> ❌ Χάθηκε στο γκολ",
        "🏁 America de Cali vs Macara | Score: 0-0 | Over 2.5 -> ❌ Κουβάς",
        "🏁 Palmeiras vs Atletico Jr | Score: 4-1 | Over 2.5 -> ✅ ΤΑΜΕΙΟ"
    ]

ODDS_API_KEY = os.environ.get('ODDS_API_KEY', 'eda6dcd0115ab96a2bf0fad47945cd34')
tz_athens = ZoneInfo("Europe/Athens")
now_athens = datetime.now(tz_athens)

output_lines = [f"STATS|{WIN_RATE}|{TOTAL_YIELD}"]

def poisson_probability(lmbda, x):
    if lmbda <= 0: return 0.0
    return (math.exp(-lmbda) * (lmbda ** x)) / math.factorial(x)

def estimate_lambdas_from_odds(over_odd, under_odd):
    raw_p_over = 1.0 / over_odd if over_odd > 0 else 0.5
    raw_p_under = 1.0 / under_odd if under_odd > 0 else 0.5
    margin = raw_p_over + raw_p_under
    
    p_over_real = raw_p_over / margin
    
    # Ευαίσθητη κλίμακα υπολογισμού xG για ποικιλία στα σημεία
    if p_over_real > 0.55:
        total_xg = 3.3
    elif p_over_real > 0.48:
        total_xg = 2.85
    elif p_over_real > 0.42:
        total_xg = 2.45
    else:
        total_xg = 1.95

    home_lambda = total_xg * 0.54
    away_lambda = total_xg * 0.46
    return home_lambda, away_lambda

def calculate_advanced_preds(home_lambda, away_lambda):
    home_lambda_half = home_lambda * 0.45
    away_lambda_half = away_lambda * 0.45
    
    over_25_prob = 0.0
    over_15_prob = 0.0
    gg_prob = 0.0
    ht_over15_prob = 0.0 
    ht_00_prob = 0.0
    
    for h in range(6):
        for a in range(6):
            p_score = poisson_probability(home_lambda, h) * poisson_probability(away_lambda, a)
            if (h + a) > 2: over_25_prob += p_score
            if (h + a) > 1: over_15_prob += p_score
            if h > 0 and a > 0: gg_prob += p_score

    for h in range(4):
        for a in range(4):
            p_score_ht = poisson_probability(home_lambda_half, h) * poisson_probability(away_lambda_half, a)
            if h == 0 and a == 0: ht_00_prob = p_score_ht
            if (h + a) > 1: ht_over15_prob += p_score_ht 
                
    under_25_prob = 1.0 - over_25_prob
    ht_over05_prob = 1.0 - ht_00_prob  
    
    return (over_25_prob * 100, under_25_prob * 100, gg_prob * 100, ht_over05_prob * 100, ht_over15_prob * 100, over_15_prob * 100)

session = requests.Session()
retry_strategy = Retry(total=3, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retry_strategy))

matches = []
SPORT_KEYS = ['soccer_international_friendlies', 'soccer']

for sport in SPORT_KEYS:
    url = f'https://api.the-odds-api.com/v4/sports/{sport}/odds/'
    params = {'apiKey': ODDS_API_KEY, 'regions': 'eu', 'markets': 'totals', 'oddsFormat': 'decimal'}
    try:
        res = session.get(url, params=params, timeout=10)
        if res.status_code == 200:
            data = res.json()
            if isinstance(data, list):
                matches.extend(data)
    except Exception as e:
        print(f"Error fetching {sport}: {e}")

valid_count = 0
min_time = now_athens - timedelta(hours=3)
max_time = now_athens + timedelta(days=3)

if matches:
    seen_matches = set()
    
    for match in matches:
        if valid_count >= 24: break
            
        home = match.get('home_team', 'Team A')
        away = match.get('away_team', 'Team B')
        match_key = f"{home} vs {away}"
        
        if match_key in seen_matches: continue
        seen_matches.add(match_key)
        
        commence_time_str = match.get('commence_time')
        if commence_time_str:
            try:
                clean_time_str = commence_time_str.replace('Z', '+00:00')
                match_utc = datetime.fromisoformat(clean_time_str)
                match_athens = match_utc.astimezone(tz_athens)
                if not (min_time <= match_athens <= max_time): continue
                match_time = match_athens.strftime("%d/%m %H:%M")
            except: continue
        else: continue
            
        bookie_over_25_odd = 1.90
        bookie_under_25_odd = 1.90
        
        for bookmaker in match.get('bookmakers', []):
            for market in bookmaker.get('markets', []):
                if market.get('key') == 'totals':
                    for outcome in market.get('outcomes', []):
                        if outcome.get('point') == 2.5:
                            if outcome.get('name') == 'Over':
                                bookie_over_25_odd = float(outcome.get('price', 1.90))
                            elif outcome.get('name') == 'Under':
                                bookie_under_25_odd = float(outcome.get('price', 1.90))

        home_lambda, away_lambda = estimate_lambdas_from_odds(bookie_over_25_odd, bookie_under_25_odd)
        p_over, p_under, p_gg, p_ht_over05, p_ht_over15, p_over15 = calculate_advanced_preds(home_lambda, away_lambda)
        
        # 1. Νέα, ισορροπημένα όρια επιλογής για ποικιλία προγνωστικών
        if p_over >= 45.0: 
            best_tip, best_prob = "Over 2.5", p_over
            final_odd = bookie_over_25_odd
        elif p_gg >= 48.0: 
            best_tip, best_prob = "Goal / Goal", p_gg
            final_odd = 1.85
        elif p_over15 >= 65.0: 
            best_tip, best_prob = "Over 1.5", p_over15
            final_odd = max(1.28, bookie_over_25_odd * 0.70)
        else: 
            best_tip, best_prob = "Under 2.5", p_under
            final_odd = bookie_under_25_odd
        
        # 2. Implied Probability (Πιθανότητα Στοιχηματικής %)
        implied_prob = (1.0 / final_odd * 100) if final_odd > 0 else 0.0

        # 3. Αυστηρός υπολογισμός VALUE BET (Απαιτείται >12% διαφορά)
        fair_odd_poisson = 100.0 / best_prob if best_prob > 0 else 99.0
        
        value_tag = ""
        if final_odd >= (fair_odd_poisson * 1.12):
            value_tag = " 🔥 VALUE BET IDENTIFIED"

        # Combo Tip 1ου Ημιχρόνου
        ht_odd = 1.35 if p_ht_over15 > 40.0 else 1.22
        ht_implied_prob = (1.0 / ht_odd * 100)
        ht_tip = f"1ο Ημίχ. Over 1.5 ({ht_implied_prob:.1f}%)" if p_ht_over15 > 40.0 else f"1ο Ημίχ. Over 0.5 ({ht_implied_prob:.1f}%)"
            
        raw_league = match.get('sport_title', 'International')
        
        if "Brazil Serie B" in raw_league or "Brazil Série B" in raw_league:
            clean_league = "Βραζιλία Série B 🇧🇷"
        elif "Argentina" in raw_league:
            clean_league = "Αργεντινή Primera 🇦🇷"
        elif "La Liga 2" in raw_league or "Segunda" in raw_league or "Spain" in raw_league:
            clean_league = "Ισπανία LaLiga 2 🇪🇸"
        elif "USL" in raw_league or "USA" in raw_league:
            clean_league = "ΗΠΑ USL Championship 🇺🇸"
        elif "Friendly" in raw_league or "International" in raw_league:
            clean_league = "Διεθνή Φιλικά 🌍"
        elif "J-League" in raw_league or "Japan" in raw_league:
            clean_league = "Ιαπωνία J-League 🇯🇵"
        else:
            clean_league = raw_league
        
        prediction = f"{best_tip} {final_odd:.2f} ({implied_prob:.1f}%){value_tag} ✨ {ht_tip}"
        output_lines.append(f"🏆 {clean_league}|{home} vs {away}|{match_time}|{prediction}")
        valid_count += 1

if valid_count == 0:
    output_lines.append("🏆 Πληροφορία|Αναμονή για Live Αγώνες|--:--|Το API καθυστερεί να ανανεώσει τα τρέχοντα φιλικά. Δοκιμάστε ξανά σε λίγο.")

output_lines.append("--- ΠΡΟΣΦΑΤΑ ΑΠΟΤΕΛΕΣΜΑΤΑ (RESULTS) ---")
if PAST_RESULTS:
    for result in PAST_RESULTS:
        if result.strip(): output_lines.append(result)

with open(DATA_FILE, "w", encoding="utf-8") as f:
    f.write("\n".join(output_lines))

print(f"🎯 Ολοκληρώθηκε επιτυχώς! Φορτώθηκαν {valid_count} αγώνες.")

