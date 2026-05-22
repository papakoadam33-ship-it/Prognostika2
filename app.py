import streamlit as st
import requests

st.title("⚽ Live Αγώνες")

HEADERS = {
    "x-rapidapi-key": "37046cb451msh72e76cf7c6071cdp1d37a8jsn3abe46eeefe3", # Βάλε εδώ το κλειδί σου
    "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
}

# Δοκιμάζουμε το path '/football-livescore' που είναι το πιο σύνηθες για αυτό το API
URL = "https://free-api-live-football-data.p.rapidapi.com/football-livescore"

if st.button("Εμφάνιση Live Αγώνων"):
    try:
        response = requests.get(URL, headers=HEADERS)
        
        # Ανάγνωση με κωδικοποίηση utf-8 για να αποφύγουμε το latin-1 σφάλμα
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            data = response.json()
            st.json(data) # Εμφανίζουμε τα δεδομένα για να δούμε τη δομή τους
        else:
            st.error(f"Σφάλμα {response.status_code}: Ελέγξτε το endpoint.")
    except Exception as e:
        st.error(f"Πρόβλημα: {e}")
