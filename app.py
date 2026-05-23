import streamlit as st
import http.client
import json
from datetime import datetime

# ==========================================
# 1. ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ & DESIGN
# ==========================================
st.set_page_config(page_title="Football Live", page_icon="⚽", layout="centered")

# Όμορφο στυλ για τα κουτάκια των αγώνων
st.markdown("""
    <style>
    .match-box {
        padding: 12px;
        border-radius: 8px;
        background-color: #f0f2f6;
        margin-bottom: 10px;
        border-left: 5px solid #0052cc;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ Live Αγώνες & Αποδόσεις (API-Football)")

# Το δικό σου API Key από το API-Football
API_KEY = "6be0e4d0ca519a79fa4da6a9089069bf"
today_str = datetime.now().strftime("%Y-%m-%d")

# Κουμπί για Refresh στην κορυφή
if st.button("🔄 Ανανέωση Δεδομένων"):
    st.rerun()

# ==========================================
# 2. ΛΗΨΗ LIVE ΑΓΩΝΩΝ ΑΠΟ API-FOOTBALL
# ==========================================
try:
    conn = http.client.HTTPSConnection("api-football-v1.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "api-football-v1.p.rapidapi.com"
    }
    
    # Ζητάμε όλους τους σημερινούς αγώνες
    conn.request("GET", f"/v3/fixtures?date={today_str}", headers=headers)
    res = conn.getresponse()
    raw_data = res.read().decode("utf-8")
    data = json.loads(raw_data)
    
    fixtures = data.get("response", [])
    
    if not fixtures:
        st.info("📅 Δεν βρέθηκαν live αγώνες στη βάση για σήμερα.")
    else:
        # Ομαδοποίηση των αγώνων ανά πρωτάθλημα
        leagues_dict = {}
        for item in fixtures:
            league_name = item.get("league", {}).get("name", "Άλλα Πρωταθλήματα")
            if league_name not in leagues_dict:
                leagues_dict[league_name] = []
            leagues_dict[league_name].append(item)
            
        # Εμφάνιση των πρωταθλημάτων (Δείχνουμε τα πρώτα 15 για να μην κολλάει το κινητό)
        for league_name, matches in list(leagues_dict.items())[:15]:
            with st.expander(f"🏆 {league_name} ({len(matches)})", expanded=False):
                for match in matches:
                    match_id = match.get("fixture", {}).get("id")
                    home = match.get("teams", {}).get("home", {}).get("name")
                    away = match.get("teams", {}).get("away", {}).get("name")
                    
                    # Σκορ και Κατάσταση Αγώνα (Live ή Ώρα έναρξης)
                    status_short = match.get("fixture", {}).get("status", {}).get("short", "")
                    home_goals = match.get("goals", {}).get("home")
                    away_goals = match.get("goals", {}).get("away")
                    
                    if home_goals is not None and away_goals is not None:
                        score_str = f"👉 {home_goals} - {away_goals} ({status_short})"
                    else:
                        match_date = match.get("fixture", {}).get("date", "")
                        score_str = f"⏰ {match_date[11:16]}"

                    # Εμφάνιση του αγώνα σε Box
                    st.markdown(f"""
                        <div class="match-box">
                            🏠 <b>{home}</b> vs 🏴 <b>{away}</b><br>
                            <span style="color:#0052cc;">{score_str}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Έξυπνος διακόπτης (Toggle) για τις αποδόσεις
                    show_odds = st.toggle("📊 Εμφάνιση Αποδόσεων", key=f"odds_{match_id}")
                    
                    if show_odds:
                        # Καλούμε τις αποδόσεις από το API-Football για το συγκεκριμένο ματς
                        conn.request("GET", f"/v3/odds?fixture={match_id}", headers=headers)
                        res_odds = conn.getresponse()
                        odds_data = json.loads(res_odds.read().decode("utf-8"))
                        
                        odds_response = odds_data.get("response", [])
                        odds_found = False
                        
                        if odds_response:
                            bookmakers = odds_response[0].get("bookmakers", [])
                            if bookmakers:
                                markets = bookmakers[0].get("bets", [])
                                # Ψάχνουμε το "Match Winner" (Αγορά 1-X-2)
                                for bet in markets:
                                    if bet.get("id") == 1: 
                                        values = bet.get("values", [])
                                        if values:
                                            odds_found = True
                                            st.write("📈 **Αποδόσεις (1-X-2):**")
                                            cols = st.columns(3)
                                            for idx, val in enumerate(values[:3]):
                                                cols[idx].metric(label=f"{val.get('value')}", value=val.get('odd'))
                        
                        if not odds_found:
                            st.warning("⚠️ Δεν έχουν βγει ακόμα αποδόσεις για αυτό το ματς.")
                    st.divider()

except Exception as e:
    st.error(f"❌ Σφάλμα σύνδεσης: {e}")
