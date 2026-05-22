import streamlit as st
import http.client
import json
from datetime import datetime

st.set_page_config(page_title="Football Live", page_icon="⚽")
st.title("⚽ Live Αγώνες")

today = datetime.now().strftime("%Y%m%d")

conn = http.client.HTTPSConnection("free-api-live-football-data.p.rapidapi.com")
headers = {
    'x-rapidapi-key': "37046cb451msh72e76cf7c6071cdp1d37a8jsn3abe46eeefe3", 
    'x-rapidapi-host': "free-api-live-football-data.p.rapidapi.com"
}

if st.button("Ενημέρωση Αγώνων"):
    try:
        conn.request("GET", f"/football-get-matches-by-date-and-league?date={today}&league=39", headers=headers)
        res = conn.getresponse()
        data = res.read()
        
        if res.status == 200:
            raw_data = json.loads(data.decode("utf-8"))
            leagues = raw_data.get("response", [])
            
            for league in leagues:
                st.subheader(f"🏆 {league.get('name')}")
                for match in league.get("matches", []):
                    # Εδώ προσπαθούμε να πάρουμε τα ονόματα των ομάδων
                    # Συνήθως βρίσκονται στο homeTeam και awayTeam
                    home = match.get('homeTeam', {}).get('name', 'Άγνωστη Ομάδα')
                    away = match.get('awayTeam', {}).get('name', 'Άγνωστη Ομάδα')
                    time = match.get('time', 'N/A')
                    st.write(f"🏟️ **{home}** vs **{away}** | ⏰ {time}")
        else:
            st.error(f"Σφάλμα: {res.status}")
    except Exception as e:
        st.error(f"Πρόβλημα: {e}")
