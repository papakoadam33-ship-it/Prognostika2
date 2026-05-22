import streamlit as st
import http.client
import json
from datetime import datetime

st.title("⚽ Debugging Ομάδων")

today = datetime.now().strftime("%Y%m%d")

conn = http.client.HTTPSConnection("free-api-live-football-data.p.rapidapi.com")
headers = {
    'x-rapidapi-key': "37046cb451msh72e76cf7c6071cdp1d37a8jsn3abe46eeefe3", 
    'x-rapidapi-host': "free-api-live-football-data.p.rapidapi.com"
}

if st.button("Εμφάνιση Δομής"):
    conn.request("GET", f"/football-get-matches-by-date-and-league?date={today}&league=39", headers=headers)
    res = conn.getresponse()
    # Μετατρέπουμε το JSON σε λεξικό Python
    data = json.loads(res.read().decode("utf-8"))
    
    leagues = data.get("response", [])
    if leagues:
        # Παίρνουμε τον πρώτο αγώνα από το πρώτο πρωτάθλημα για να δούμε τα κλειδιά του
        first_match = leagues[0].get("matches", [{}])[0]
        st.write("### Δομή του αντικειμένου 'match':")
        st.json(first_match) 
    else:
        st.write("Δεν βρέθηκαν αγώνες.")

