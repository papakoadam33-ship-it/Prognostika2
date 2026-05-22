import streamlit as st
import http.client
import json
from datetime import datetime

st.set_page_config(page_title="Football Live", page_icon="⚽")
st.title("⚽ Live Αγώνες & Προγνωστικά")

today = datetime.now().strftime("%Y%m%d")

conn = http.client.HTTPSConnection("free-api-live-football-data.p.rapidapi.com")
headers = {
    'x-rapidapi-key': "37046cb451msh72e76cf7c6071cdp1d37a8jsn3abe46eeefe3", 
    'x-rapidapi-host': "free-api-live-football-data.p.rapidapi.com"
}

if st.button("Ενημέρωση"):
    conn.request("GET", f"/football-get-matches-by-date-and-league?date={today}", headers=headers)
    res = conn.getresponse()
    data = json.loads(res.read().decode("utf-8"))
    
    for league in data.get("response", []):
        st.subheader(f"🏆 {league.get('name')}")
        for match in league.get("matches", []):
            home = match.get('home', {}).get('name')
            away = match.get('away', {}).get('name')
            
            # Διαχείριση ώρας και Live status
            # Αν υπάρχει πεδίο 'status', το εμφανίζουμε
            status = match.get('status', 'Προγραμματισμένος')
            time = match.get('time', 'N/A')
            
            # Πρόταση για Over 2.5 (απλή λογική)
            over_suggestion = "📊 Προτεινόμενο: Over 2.5" 
            
            if status == "LIVE":
                st.write(f"🔴 **LIVE** | 🏟️ {home} vs {away} | ⏰ {time} | {over_suggestion}")
            else:
                st.write(f"📅 {time} | 🏟️ {home} vs {away} | {over_suggestion}")
