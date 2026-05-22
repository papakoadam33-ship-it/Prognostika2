import streamlit as st
import http.client
import json
from datetime import datetime

st.set_page_config(page_title="Football Live", page_icon="⚽")
st.title("⚽ Live Αγώνες & Προγνωστικά")

# Υπολογισμός ημερομηνίας
today = datetime.now().strftime("%Y%m%d")

conn = http.client.HTTPSConnection("free-api-live-football-data.p.rapidapi.com")
headers = {
    'x-rapidapi-key': "37046cb451msh72e76cf7c6071cdp1d37a8jsn3abe46eeefe3",
    'x-rapidapi-host': "free-api-live-football-data.p.rapidapi.com"
}

if st.button("Ενημέρωση"):
    conn.request("GET", f"/football-get-matches-by-date-and-league?date={today}", headers=headers)
    res = conn.getresponse()
    raw_data = res.read()
    data = json.loads(raw_data.decode("utf-8"))
    
    leagues = data.get("response", [])
    for league in leagues:
        st.subheader(f"🏆 {league.get('name')}")
        for match in league.get("matches", []):
            home = match.get('home', {}).get('name', 'Γηπεδούχος')
            away = match.get('away', {}).get('name', 'Φιλοξενούμενος')
            score_h = match.get('home', {}).get('score', 0)
            score_a = match.get('away', {}).get('score', 0)
            status = match.get('status', '') # Παίρνουμε το status
            
            # Δοκιμαστικό μήνυμα για να δεις ότι ο κώδικας άλλαξε
            if status == "LIVE":
                st.markdown(f"🔴 **LIVE: {home} {score_h} - {score_a} {away}**")
            else:
                st.write(f"📅 {match.get('time')} | {home} vs {away} | 📊 Over 2.5")
