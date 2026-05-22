import streamlit as st
import http.client
import json
from datetime import datetime

# 1. Ρύθμιση σελίδας
st.set_page_config(page_title="Football Live", page_icon="⚽")
st.title("⚽ Live Αγώνες & Προγνωστικά")

# 2. Ασφάλεια: Χρήση secrets του Streamlit αντί για hardcoded key
# Στο τοπικό σου περιβάλλον φτιάξε έναν φάκελο .streamlit/secrets.toml
# και πρόσθεσε: RAPIDAPI_KEY = "το-κλειδί-σου"
API_KEY = st.secrets.get("RAPIDAPI_KEY", "37046cb451msh72e76cf7c6071cdp1d37a8jsn3abe46eeefe3")

today = datetime.now().strftime("%Y%m%d")

if st.button("Ενημέρωση"):
    try:
        conn = http.client.HTTPSConnection("free-api-live-football-data.p.rapidapi.com")
        headers = {
            'x-rapidapi-key': API_KEY,
            'x-rapidapi-host': "free-api-live-football-data.p.rapidapi.com"
        }
        
        conn.request("GET", f"/football-get-matches-by-date-and-league?date={today}", headers=headers)
        res = conn.getresponse()
        
        if res.status == 200:
            data = json.loads(res.read().decode("utf-8"))
            leagues = data.get("response", [])
            
            if not leagues:
                st.info("Δεν βρέθηκαν αγώνες για σήμερα.")
            
            for league in leagues:
                with st.expander(f"🏆 {league.get('name', 'Άγνωστο Πρωτάθλημα')}"):
                    for match in league.get("matches", []):
                        home = match.get('home', {}).get('name', 'Γηπεδούχος')
                        away = match.get('away', {}).get('name', 'Φιλοξενούμενος')
                        score_h = match.get('home', {}).get('score', 0)
                        score_a = match.get('away', {}).get('score', 0)
                        status = match.get('status', '')
                        time = match.get('time', 'N/A')
                        
                        if status == "LIVE":
                            st.markdown(f"🔴 **{home} {score_h} - {score_a} {away}**")
                        else:
                            st.write(f"📅 {time} | {home} vs {away} | 📊 Over 2.5")
        else:
            st.error(f"Σφάλμα σύνδεσης με τον διακομιστή: {res.status}")
            
    except Exception as e:
        st.error(f"Προέκυψε σφάλμα: {e}")

