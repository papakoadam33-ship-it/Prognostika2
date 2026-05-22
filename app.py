import streamlit as st
import http.client
import json
from datetime import datetime

st.set_page_config(page_title="Football Live", page_icon="⚽")
st.title("⚽ Live Αγώνες & Προγνωστικά")

# Υπολογισμός σημερινής ημερομηνίας
today = datetime.now().strftime("%Y%m%d")

conn = http.client.HTTPSConnection("free-api-live-football-data.p.rapidapi.com")
headers = {
    'x-rapidapi-key': "37046cb451msh72e76cf7c6071cdp1d37a8jsn3abe46eeefe3", # ΒΑΛΕ ΕΔΩ ΤΟ ΚΛΕΙΔΙ ΣΟΥ
    'x-rapidapi-host': "free-api-live-football-data.p.rapidapi.com"
}

if st.button("Ενημέρωση"):
    try:
        conn.request("GET", f"/football-get-matches-by-date-and-league?date={today}", headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        for league in data.get("response", []):
            st.subheader(f"🏆 {league.get('name')}")
            for match in league.get("matches", []):
                home = match.get('home', {}).get('name', 'Γηπεδούχος')
                away = match.get('away', {}).get('name', 'Φιλοξενούμενος')
                score_h = match.get('home', {}).get('score', 0)
                score_a = match.get('away', {}).get('score', 0)
                status = match.get('status')
                
                if status == "LIVE":
                    st.write(f"🔴 **LIVE** | 🏟️ {home} {score_h} vs {away} {score_a} | ⏰ {match.get('time')}")
                else:
                    st.write(f"📅 {match.get('time')} | 🏟️ {home} vs {away} | 📊 Προτεινόμενο: Over 2.5")
                    
    except Exception as e:
        st.error(f"Πρόβλημα: {e}")
