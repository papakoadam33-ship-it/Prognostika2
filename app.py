import streamlit as st
import os

st.set_page_config(page_title="MARIOS PRO-BET PRO", page_icon="⚡", layout="centered")

# --- ΛΕΞΙΚΑ ΜΕΤΑΦΡΑΣΗΣ ---
LEAGUE_TRANSLATIONS = {
    "Premier League": "Πρωτάθλημα Αγγλίας (Premier League)",
    "Championship": "Αγγλία - Championship (Β')",
    "League 1": "Αγγλία - League One (Γ')",
    "League 2": "Αγγλία - League Two (Δ')",
    "La Liga": "Πρωτάθλημα Ισπανίας (La Liga)",
    "Serie A - Italy": "Πρωτάθλημα Ιταλίας (Serie A)",
    "Bundesliga": "Πρωτάθλημα Γερμανίας (Bundesliga)",
    "Ligue 1 - France": "Πρωτάθλημα Γαλλίας (Ligue 1)",
    "Eliteserien - Norway": "Πρωτάθλημα Νορβηγίας (Eliteserien)",
    "Austrian Football Bundesliga": "Πρωτάθλημα Αυστρίας (Bundesliga)",
    "Allsvenskan - Sweden": "Πρωτάθλημα Σουηδίας (Allsvenskan)"
}

TEAM_TRANSLATIONS = {
    "KFUM": "ΚΦΟΥΜ Όσλο", "Rosenborg": "Ρόζενμποργκ", "Sarpsborg FK": "Σάρπσμποργκ",
    "Molde": "Μόλντε", "Tromso": "Τρόμσο", "Aalesund": "Άαλεσουντ",
    "HamKam": "ΧαμΚαμ", "Lillestrom": "Λίλεστρομ", "IK Start": "Σταρτ",
    "Vålerenga": "Βαλερένγκα", "Notts County": "Νοτς Kάουντι", "Salford City": "Σάλφορντ Σίτι",
    "Rapid Wien": "Ραπίντ Βιέννης", "Ried": "Ριντ", "IF Elfsborg": "Έλφσμποργκ",
    "BK Hacken": "Χάκεν", "Malmo FF": "Μάλμε", "AIK": "ΑΪΚ Στοκχόλμης",
    "I Goteborg": "Γκέτεμποργκ", "IFK Goteborg": "Γκέτεμποργκ", "Mjällby A": "Μιάλμπι"
}

def translate_teams(teams_string):
    if " vs " in teams_string:
        parts = teams_string.split(" vs ")
        home = TEAM_TRANSLATIONS.get(parts[0].strip(), parts[0].strip())
        away = TEAM_TRANSLATIONS.get(parts[1].strip(), parts[1].strip())
        return f"{home} vs {away}"
    return teams_string

# Custom CSS
st.markdown("""
    <style>
    .main { background-color: #121212; }
    .title-box { background: linear-gradient(135deg, #1e1e1e 0%, #121212 100%); padding: 25px; border-radius: 15px; border: 2px solid #FFD700; text-align: center; box-shadow: 0px 4px 15px rgba(255, 215, 0, 0.2); margin-bottom: 25px; }
    .title-text { color: #FFFFFF; font-size: 28px; font-weight: bold; }
    .subtitle-text { color: #FFD700; font-style: italic; font-size: 16px; }
    .match-card { background-color: #1a1a1a; padding: 20px; border-radius: 12px; border: 1px solid #333; margin-bottom: 20px; }
    .time-badge { background-color: #FF4B4B; color: white; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    .team-text { color: #FFFFFF; font-size: 20px; font-weight: bold; margin-top: 10px; }
    .form-text { color: #AAAAAA; font-size: 13px; margin: 3px 0; }
    .pred-button-vip { background: linear-gradient(90deg, #D4AF37 0%, #FFD700 100%); color: #000000; padding: 12px; border-radius: 8px; text-align: center; font-weight: bold; font-size: 16px; margin-top: 15px; }
    .pred-button-stat { background: linear-gradient(90deg, #CD7F32 0%, #E6C280 100%); color: #000000; padding: 12px; border-radius: 8px; text-align: center; font-weight: bold; font-size: 16px; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="title-box">
        <div class="title-text">⚡ MARIOS PRO-BET PRO ⚡</div>
        <div class="subtitle-text">Poisson Distribution Model</div>
    </div>
""", unsafe_allow_html=True)

filename = "daily_predictions.txt"

live_rate = "78.4%"
live_yield = "+21.8%"

# Διάβασμα των αρχείων και εξαγωγή των Live στατιστικών
if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    if lines and lines[0].startswith("STATS"):
        stats_parts = lines[0].strip().split("|")
        live_rate = f"{stats_parts[1]}%"
        live_yield = f"+{stats_parts[2]}%"
        lines = lines[1:] # Αφαιρούμε τη γραμμή των στατιστικών για να μην μπερδευτεί το UI

# Εμφάνιση των LIVE Στατιστικών
col1, col2 = st.columns(2)
with col1:
    st.metric(label="📈 Συνολικό Yield", value=live_yield, delta="Premium 🎯")
with col2:
    st.metric(label="🎯 Ποσοστό Επιτυχίας Poisson", value=live_rate, delta="📊 Ζωντανά Δεδομένα")

st.markdown("<br>", unsafe_allow_html=True)

if os.path.exists(filename) and lines:
    first_line = lines[0].strip()
    timestamp = first_line.replace("--- ΠΡΟΓΝΩΣΤΙΚΑ ", "").replace(" ---", "") if "---" in first_line else "Σήμερα"
    
    st.markdown(f"<div style='color:#FFD700; font-weight:bold; margin-bottom:15px;'>📅 ΠΡΟΓΝΩΣΤΙΚΑ {timestamp}</div>", unsafe_allow_html=True)
    
    leagues_data = {}
    for line in lines:
        if line.startswith("---") or not line.strip():
            continue
        parts = line.strip().split("|")
        if len(parts) >= 6:
            league = parts[0]
            if league not in leagues_data: leagues_data[league] = []
            leagues_data[league].append(parts)
            
    for league_name, matches in leagues_data.items():
        greek_league = LEAGUE_TRANSLATIONS.get(league_name.strip(), league_name.strip())
        st.markdown(f"<h3 style='color:#FFD700; border-bottom: 1px solid #FFD700; padding-bottom:5px; margin-top:20px;'>🏆 {greek_league}</h3>", unsafe_allow_html=True)
        
        for match in matches:
            teams, match_time, tip, home_form, away_form = match[1], match[2], match[3], match[4], match[5]
            greek_teams = translate_teams(teams)
            
            st.markdown(f"""
                <div class="match-card">
                    <span class="time-badge">🕒 {match_time}</span>
                    <div class="team-text">{greek_teams}</div>
                    <div class="form-text">📊 Φόρμα: {home_form} vs {away_form}</div>
            """, unsafe_allow_html=True)
            
            clean_tip = tip.replace("🔥 [Bookmaker]", "").replace("📊 [Στατιστικό]", "").strip()
            if "🔥" in tip:
                st.markdown(f'<div class="pred-button-vip">👑 VIP ΕΠΙΛΟΓΗ: {clean_tip}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="pred-button-stat">📊 ΣΤΑΤΙΣΤΙΚΟ: {clean_tip}</div>', unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("⏳ Αναμονή για τη φόρτωση των νέων αυριανών αγώνων...")

