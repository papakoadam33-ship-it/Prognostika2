import streamlit as st
import requests

st.title("⚽ Live Αγώνες")

# ΠΡΟΣΟΧΗ: Βάλε το κλειδί σου ανάμεσα στα εισαγωγικά
HEADERS = {
    "x-rapidapi-key": "37046cb451msh72e76cf7c6071cdp1d37a8jsn3abe46eeefe3",
    "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
}
URL = "https://free-api-live-football-data.p.rapidapi.com/football-livescore"

if st.button("Εμφάνιση Live Αγώνων"):
    try:
        response = requests.get(URL, headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            st.write(data)
        else:
            st.error(f"Σφάλμα σύνδεσης: {response.status_code}")
    except Exception as e:
        st.error(f"Πρόβλημα: {e}")
