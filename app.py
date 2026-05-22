import streamlit as st
import http.client
import json

st.set_page_config(page_title="Football Live", page_icon="⚽")
st.title("⚽ Live Αγώνες Ποδοσφαίρου")

# Σύνδεση με το API
conn = http.client.HTTPSConnection("free-api-live-football-data.p.rapidapi.com")
headers = {
    'x-rapidapi-key': "37046cb451msh72e76cf7c6071cdp1d37a8jsn3abe46eeefe3", # ΒΑΛΕ ΕΔΩ ΤΟ ΚΛΕΙΔΙ ΣΟΥ
    'x-rapidapi-host': "free-api-live-football-data.p.rapidapi.com"
}

if st.button("Ενημέρωση Live Αγώνων"):
    try:
        # Κλήση στο endpoint
        conn.request("GET", "/football-get-matches-by-date-and-league?date=20241107&league=39", headers=headers)
        res = conn.getresponse()
        data = res.read()
        
        if res.status == 200:
            raw_data = json.loads(data.decode("utf-8"))
            leagues = raw_data.get("response", [])
            
            if not leagues:
                st.info("Δεν βρέθηκαν αγώνες για αυτή την ημερομηνία.")
            else:
                for league in leagues:
                    st.subheader(f"🏆 {league.get('name', 'Πρωτάθλημα')}")
                    for match in league.get("matches", []):
                        # Εδώ εμφανίζουμε τα στοιχεία του αγώνα
                        home = match.get('homeTeam', {}).get('name', 'Γηπεδούχος')
                        away = match.get('awayTeam', {}).get('name', 'Φιλοξενούμενος')
                        st.write(f"🏟️ {home} vs {away} | ⏰ {match.get('time')}")
        else:
            st.error(f"Σφάλμα σύνδεσης: {res.status}")
    except Exception as e:
        st.error(f"Πρόβλημα κατά την ανάκτηση: {e}")

