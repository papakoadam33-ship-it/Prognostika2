import streamlit as st
import http.client
import json
from datetime import datetime

st.set_page_config(page_title="Football Live", page_icon="⚽")
st.title("⚽ Live Αγώνες Ποδοσφαίρου")

# Υπολογισμός σημερινής ημερομηνίας
today = datetime.now().strftime("%Y%m%d")

conn = http.client.HTTPSConnection("free-api-live-football-data.p.rapidapi.com")
headers = {
    'x-rapidapi-key': "37046cb451msh72e76cf7c6071cdp1d37a8jsn3abe46eeefe3", # Βεβαιώσου ότι είναι το σωστό
    'x-rapidapi-host': "free-api-live-football-data.p.rapidapi.com"
}

if st.button("Ενημέρωση Αγώνων"):
    try:
        # Χρησιμοποιούμε τη σωστή ημερομηνία
        conn.request("GET", f"/football-get-matches-by-date-and-league?date={today}", headers=headers)
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        
        leagues = data.get("response", [])
        
        if not leagues:
            st.info("Δεν βρέθηκαν αγώνες για σήμερα.")
        else:
            for league in leagues:
                st.subheader(f"🏆 {league.get('name', 'Πρωτάθλημα')}")
                for match in league.get("matches", []):
                    # Εδώ χρησιμοποιούμε τα σωστά κλειδιά που βρήκαμε
                    home_name = match.get('home', {}).get('name', 'Γηπεδούχος')
                    away_name = match.get('away', {}).get('name', 'Φιλοξενούμενος')
                    time = match.get('time', 'N/A')
                    st.write(f"🏟️ **{home_name}** vs **{away_name}** | ⏰ {time}")
    except Exception as e:
        st.error(f"Πρόβλημα: {e}")

