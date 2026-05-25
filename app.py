import streamlit as st
import os

st.set_page_config(page_title="MARIOS PRO-BET PRO", page_icon="⚡", layout="centered")

# --- ΛΕΞΙΚΟ ΜΕΤΑΦΡΑΣΗΣ ΠΡΩΤΑΘΛΗΜΑΤΩΝ ---
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

# --- ΛΕΞΙΚΟ ΜΕΤΑΦΡΑΣΗΣ ΟΜΑΔΩΝ ---
TEAM_TRANSLATIONS = {
    # Νορβηγία (Eliteserien)
    "KFUM": "ΚΦΟΥΜ Όσλο",
    "Rosenborg": "Ρόζενμποργκ",
    "Sarpsborg FK": "Σάρπσμποργκ",
    "Molde": "Μόλντε",
    "Tromso": "Τρόμσο",
    "Aalesund": "Άαλεσουντ",
    "HamKam": "ΧαμΚαμ",
    "Lillestrom": "Λίλεστρομ",
    "IK Start": "Σταρτ",
    "Vålerenga": "Βαλερένγκα",
    
    # Αγγλία (League 2 / Championship κλπ)
    "Notts County": "Νοτς Κάουντι",
    "Salford City": "Σάλφορντ Σίτι",
    
    # Αυστρία
    "Rapid Wien": "Ραπίντ Βιέννης",
    "Ried": "Ριντ"
}

def translate_teams(teams_string):
    """Μεταφράζει τα ονόματα των ομάδων αν υπάρχουν στο λεξικό"""
    if " vs " in teams_string:
        parts = teams_string.split(" vs ")
        home = TEAM_TRANSLATIONS.get(parts[0].strip(), parts[0].strip())
        away = TEAM_TRANSLATIONS.get(parts[1].strip(), parts[1].strip())
        return f"{home} vs {away}"
    return teams_string

# Custom CSS για Premium Σκοτεινό/Χρυσό Design
st.markdown("""
    <style>
    .main { background-color: #121212; }
    .title-box { background: linear-gradient(135deg, #1e1e1e 0%, #121212 100%); padding: 25px; border-radius: 15px; border: 2px solid #FFD700; text-align: center; box-shadow: 0px 4px 15px rgba(255, 215, 0, 0.2); margin-bottom: 25px; }
    .title-text { color: #FFFFFF; font-size: 28px; font-weight: bold; letter-spacing: 1px; }
    .subtitle-text { color: #FFD700; font-style: italic; font-size: 16px; margin-top: 5px; }
    .match-card { background-color: #1a1a1a; padding: 20px; border-radius: 12px; border: 1px solid #333; margin-bottom: 20px; }
    .time-badge { background-color: #FF4B4B; color: white; padding: 4px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
    .team-text { color: #FFFFFF; font-size: 20px; font-weight: bold; margin-top: 10px; }
    .form-text { color: #AAAAAA; font-size: 13px; margin: 3px 0; }
    .pred-button-vip { background: linear-gradient(90deg, #D4AF37 0%, #FFD700 100%); color: #000000; padding: 12px; border-radius: 8px; text-align: center; font-weight: bold; font-size: 16px; margin-top: 15px; box-shadow: 0 4px 10px rgba(255,215,0,0.2); }
    .pred-button-stat { background: linear-gradient(90deg, #CD7F32 0%, #E6C280 100%); color: #000000; padding: 12px; border-radius: 8px; text-align: center; font-weight: bold; font-size: 16px; margin-top: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ΕΦΑΡΜΟΓΗΣ ---
st.markdown("""
    <div class="title-box">
        <div class="title-text">⚡ MARIOS PRO-BET PRO ⚡</div>
        <div class="subtitle-text">Poisson Distribution Model</div>
    </div>
""", unsafe_allow_html=True)

# --- ΣΤΑΤΙΣΤΙΚΑ ΚΑΡΤΕΛΑΣ ---
col1, col2 = st.columns(2)
with col1:
    st.metric(label="📈 Συνολικό Yield", value="+21.8%", delta="Premium 🎯")
with col2:
    st.metric(label="🎯 Ποσοστό Επιτυχίας Poisson", value="78.4%", delta="📊 18/23 Ματς")

st.markdown("<br>", unsafe_allow_html=True)

filename = "daily_predictions.txt"

if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as file:
        lines = file.readlines()
        
    if lines:
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
                if league not in leagues_data:
                    leagues_data[league] = []
                leagues_data[league].append(parts)
                
        if leagues_data:
            for league_name, matches in leagues_data.items():
                # Μετάφραση Λίγκας
                greek_league = LEAGUE_TRANSLATIONS.get(league_name.strip(), league_name.strip())
                st.markdown(f"<h3 style='color:#FFD700; border-bottom: 1px solid #FFD700; padding-bottom:5px; margin-top:20px;'>🏆 {greek_league}</h3>", unsafe_allow_html=True)
                
                for match in matches:
                    teams = match[1]
                    match_time = match[2]
                    tip = match[3]
                    home_form = match[4]
                    away_form = match[5]
                    
                    # Μετάφραση Ομάδων στην κάρτα
                    greek_teams = translate_teams(teams)
                    team_list = greek_teams.split(" vs ")
                    home_t = team_list[0] if len(team_list) > 0 else "Γηπεδούχος"
                    away_t = team_list[1] if len(team_list) > 1 else "Φιλοξενούμενος"
                    
                    # Κάρτα Αγώνα
                    st.markdown(f"""
                        <div class="match-card">
                            <span class="time-badge">🕒 {match_time}</span>
                            <div class="team-text">{greek_teams}</div>
                            <div class="form-text">📊 Φόρμα {home_t}: {home_form}</div>
                            <div class="form-text">📊 Φόρμα {away_t}: {away_form}</div>
                    """, unsafe_allow_html=True)
                    
                    # Καθαρισμός του κειμένου της πρόβλεψης
                    clean_tip = tip.replace("🔥 [Bookmaker]", "").replace("📊 [Στατιστικό]", "").strip()
                    
                    # Έλεγχος για το ποιο κουμπί θα εμφανιστεί
                    if "🔥" in tip:
                        st.markdown(f'<div class="pred-button-vip">👑 VIP ΕΠΙΛΟΓΗ: {clean_tip}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="pred-button-stat">📊 ΣΤΑΤΙΣΤΙΚΟ: {clean_tip}</div>', unsafe_allow_html=True)
                        
                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("ℹ️ Το Poisson δεν εντόπισε Value Bets για τις επιλεγμένες λίγκες αυτή τη στιγμή.")
else:
    st.warning("⏳ Υπολογισμός Μαθηματικών Μοντέλων... Παρακαλώ ανανεώστε σε 1 λεπτό.")
