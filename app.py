import streamlit as st
import requests

st.title("⚽ Live Αγώνες")

HEADERS = {
    "x-rapidapi-key": "37046cb451msh72e76cf7c6071cdp1d37a8jsn3abe46eeefe3", # Βάλε το κλειδί σου
    "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
}

# Το σωστό URL είναι συχνά με πληθυντικό ή διαφορετικό path
# Δοκιμάζουμε το /livescores
URL = "https://free-api-live-football-data.p.rapidapi.com/livescores"

if st.button("Εμφάνιση Live Αγώνων"):
    try:
        response = requests.get(URL, headers=HEADERS)
        
        if response.status_code == 200:
            st.success("Σύνδεση επιτυχής!")
            data = response.json()
            st.json(data) 
        else:
            st.error(f"Σφάλμα {response.status_code}: Το endpoint δεν βρέθηκε. Δοκίμασε το /football-livescore")
    except Exception as e:
        st.error(f"Πρόβλημα: {e}")

