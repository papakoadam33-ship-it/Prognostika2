import streamlit as st
import http.client
import json
from datetime import datetime

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

# Ασφάλεια API Key
API_KEY = st.secrets.get("RAPIDAPI_KEY", "37046cb451msh72e76cf7c6071cdp1d37a8jsn3abe46eeefe3")
today = datetime.now().strftime("%Y%m%d")

# Κουμπί για χειροκίνητο Refresh
if st.button("🔄 Ανανέωση Δεδομένων"):
    st.rerun()

# ==========================================
# 2. ΛΗΨΗ LIVE ΑΓΩΝΩΝ
# ==========================================
try:
    conn = http.client.HTTPSConnection("free-api-live-football-data.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': API_KEY,
        'x-rapidapi-host': "free-api-live-football-data.p.rapidapi.com"
    }
    
    # Καλούμε το API για τους αγώνες
    conn.request("GET", f"/football-get-matches-by-date-and-league?date={today}", headers=headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    
    leagues = data.get("response", [])
    
    if not leagues:
        st.info("📅 Δεν υπάρχουν προγραμματισμένοι αγώνες για σήμερα.")
    
    # Εμφάνιση Πρωταθλημάτων
    for league in leagues:
        league_name = league.get('name', 'Πρωτάθλημα')
        matches = league.get("matches", [])
        
        if matches:
            with st.expander(f"🏆 {league_name} ({len(matches)})", expanded=True):
                for match in matches:
                    match_id = match.get('id')
                    home = match.get('home', {}).get('name', 'Γηπεδούχος')
                    away = match.get('away', {}).get('name', 'Φιλοξενούμενος')
                    match_time = match.get('time', '--:--')
                    status = match.get('status', '') # Π.χ. Live, Finished
                    
                    # Όμορφο box για κάθε ματς
                    st.markdown(f"""
                        <div class="match-box">
                            <b>⏳ {match_time}</b> {f' - <span style="color:red">{status}</span>' if status else ''}<br>
                            🏠 {home} vs 🏴 {away}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Έξυπνος διακόπτης (Toggle) για εμφάνιση αποδόσεων χωρίς κρασάρισμα
                    show_odds = st.toggle("📊 Εμφάνιση Αποδόσεων", key=f"toggle_{match_id}")
                    
                    if show_odds:
                        try:
                            # Καλούμε τις αποδόσεις για το συγκεκριμένο ματς
                            conn.request("GET", f"/football-event-odds?eventid={match_id}&countrycode=GR", headers=headers)
                            res_odds = conn.getresponse()
                            odds_data = json.loads(res_odds.read().decode("utf-8"))
                            
                            # Διάβασμα των αποδόσεων
                            market = odds_data.get("response", {}).get("odds", {}).get("odds", {}).get("resolvedOddsMarket", {})
                            selections = market.get("selections", [])
                            
                            if selections:
                                st.write("📈 **Τρέχουσες Αποδόσεις (1-X-2):**")
                                cols = st.columns(len(selections))
                                for i, item in enumerate(selections):
                                    cols[i].metric(
                                        label=f"Σημείο {item.get('name')}", 
                                        value=item.get('oddsDecimal')
                                    )
                            else:
                                st.warning("⚠️ Δεν βρέθηκαν διαθέσιμες αποδόσεις για αυτό το ματς.")
                        except Exception as odds_error:
                            st.caption(f"Αδυναμία φόρτωσης αποδόσεων: {odds_error}")
                    
                    st.divider() # Διαχωριστική γραμμή ανάμεσα στα ματς

except Exception as e:
    st.error(f"❌ Σφάλμα σύνδεσης με το API: {e}")
