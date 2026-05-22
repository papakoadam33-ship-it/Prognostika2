import streamlit as st
import http.client
import json
from datetime import datetime

# Ρύθμιση σελίδας
st.set_page_config(page_title="Football Live", page_icon="⚽")
st.title("⚽ Live Αγώνες & Αποδόσεις")

# Ασφάλεια: Χρήση secrets (ρυθμίστε το στο Streamlit Cloud)
API_KEY = st.secrets.get("RAPIDAPI_KEY", "37046cb451msh72e76cf7c6071cdp1d37a8jsn3abe46eeefe3")
today = datetime.now().strftime("%Y%m%d")

if st.button("Ενημέρωση"):
    try:
        conn = http.client.HTTPSConnection("free-api-live-football-data.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': API_KEY,
            'x-rapidapi-host': "free-api-live-football-data.p.rapidapi.com"
        }
        
        # Λήψη αγώνων
        conn.request("GET", f"/football-get-matches-by-date-and-league?date={today}", headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        leagues = data.get("response", [])
        if not leagues:
            st.info("Δεν βρέθηκαν αγώνες για σήμερα.")
            
        for league in leagues:
            with st.expander(f"🏆 {league.get('name', 'Πρωτάθλημα')}"):
                for match in league.get("matches", []):
                    match_id = match.get('id')
                    home = match.get('home', {}).get('name', 'Γηπεδούχος')
                    away = match.get('away', {}).get('name', 'Φιλοξενούμενος')
                    
                    st.write(f"📅 {match.get('time')} | {home} vs {away}")
                    
                    # Κουμπί για Αποδόσεις
                    if st.button(f"📊 Αποδόσεις: {home} vs {away}", key=f"btn_{match_id}"):
                        conn.request("GET", f"/football-event-odds?eventid={match_id}&countrycode=GR", headers=headers)
                        res_odds = conn.getresponse()
                        odds_data = json.loads(res_odds.read().decode("utf-8"))
                        
                        # Ανάκτηση αποδόσεων από τη δομή του JSON
                        market = odds_data.get("response", {}).get("odds", {}).get("odds", {}).get("resolvedOddsMarket", {})
                        selections = market.get("selections", [])
                        
                        if selections:
                            st.write("📈 **Στοιχηματικές Επιλογές:**")
                            cols = st.columns(len(selections))
                            for i, item in enumerate(selections):
                                cols[i].metric(label=f"Σημείο {item.get('name')}", value=item.get('oddsDecimal'))
                        else:
                            st.warning("Δεν βρέθηκαν διαθέσιμες αποδόσεις.")
                            
    except Exception as e:
        st.error(f"Σφάλμα σύνδεσης: {e}")
