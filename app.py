import streamlit as st
import http.client
import json
from datetime import datetime, timedelta

# ==========================================
# 1. ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ & DESIGN
# ==========================================
st.set_page_config(page_title="Football Live", page_icon="⚽", layout="centered")

st.markdown("""
    <style>
    .match-box {
        padding: 12px;
        border-radius: 8px;
        background-color: #f0f2f6;
        margin-bottom: 10px;
        border-left: 5px solid #2e7d32;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ Live Αγώνες & Αποδόσεις")

# Το API Key σου
API_KEY = "37046cb451msh72e76cf7c6071cdp1d37a8jsn3abe46eeefe3"

# 📅 Επιλογή Ημέρας
option = st.radio(
    "📅 Επιλέξτε ημέρα για εμφάνιση αγώνων:",
    ["Σήμερα", "Εχθές", "Αύριο"],
    horizontal=True
)

if option == "Σήμερα":
    target_date = datetime.now()
elif option == "Εχθές":
    target_date = datetime.now() - timedelta(days=1)
else:
    target_date = datetime.now() + timedelta(days=1)

today_str = target_date.strftime("%Y%m%d")
display_date = target_date.strftime("%d/%m/%Y")

st.write(f"📊 Εμφάνιση αγώνων για τη μέρα: **{display_date}**")

# Λίστα με τα δημοφιλή League IDs που υποστηρίζει σίγουρα το API σου
# 47 = Champions League, 48 = Premier League, 42 = Champions League Qualification, κλπ.
POPULAR_LEAGUES = [47, 48, 42, 53, 54, 55, 57, 34]

# ==========================================
# 2. ΛΗΨΗ ΔΕΔΟΜΕΝΩΝ ΑΠΟ ΤΟ API
# ==========================================
try:
    conn = http.client.HTTPSConnection("free-api-live-football-data.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "free-api-live-football-data.p.rapidapi.com"
    }
    
    matches_found = False
    
    # Ψάχνουμε συστηματικά στα μεγάλα πρωταθλήματα για τη μέρα που διάλεξες
    for league_id in POPULAR_LEAGUES:
        conn.request("GET", f"/football-get-matches-by-date-and-league?date={today_str}&leagueid={league_id}", headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        leagues = data.get("response", [])
        
        for league in leagues:
            league_name = league.get('name', 'Πρωτάθλημα')
            matches = league.get("matches", [])
            
            if matches:
                matches_found = True
                with st.expander(f"🏆 {league_name} ({len(matches)})", expanded=True):
                    for match in matches:
                        match_id = match.get('id')
                        home = match.get('home', {}).get('name', 'Γηπεδούχος')
                        away = match.get('away', {}).get('name', 'Φιλοξενούμενος')
                        match_time = match.get('time', '--:--')
                        
                        st.markdown(f"""
                            <div class="match-box">
                                ⏳ <b>{match_time}</b><br>
                                🏠 {home} vs 🏴 {away}
                            </div>
                        """, unsafe_allow_html=True)
                        
                        show_odds = st.toggle("📊 Εμφάνιση Αποδόσεων", key=f"toggle_{match_id}")
                        
                        if show_odds:
                            try:
                                conn.request("GET", f"/football-event-odds?eventid={match_id}&countrycode=GR", headers=headers)
                                res_odds = conn.getresponse()
                                odds_data = json.loads(res_odds.read().decode("utf-8"))
                                
                                market = odds_data.get("response", {}).get("odds", {}).get("odds", {}).get("resolvedOddsMarket", {})
                                selections = market.get("selections", [])
                                
                                if selections:
                                    st.write("📈 **Αποδόσεις (1-X-2):**")
                                    cols = st.columns(len(selections))
                                    for i, item in enumerate(selections):
                                        cols[i].metric(
                                            label=f"Σημείο {item.get('name')}", 
                                            value=item.get('oddsDecimal')
                                        )
                                else:
                                    st.warning("⚠️ Δεν υπάρχουν διαθέσιμες αποδόσεις.")
                            except Exception as odds_err:
                                st.caption("Αδυναμία φόρτωσης αποδόσεων.")
                        st.divider()

    if not matches_found:
        st.info(f"📅 Δεν βρέθηκαν live αγώνες στα μεγάλα πρωταθλήματα για τις {display_date}. Δοκιμάστε άλλη ημερομηνία!")

except Exception as e:
    st.error(f"❌ Σφάλμα σύνδεσης: {e}")

