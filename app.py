import streamlit as st
import requests

st.title("⚽ Live Αγώνες")

HEADERS = {
    'x-rapidapi-key': "ΤΟ_ΚΛΕΙΔΙ_ΣΟΥ", # 37046cb451msh72e76cf7c6071cdp1d37a8jsn3abe46eeefe3
    'x-rapidapi-host': "free-api-live-football-data.p.rapidapi.com"
}
URL = "https://free-api-live-football-data.p.rapidapi.com/football-livescore"

if st.button("Εμφάνιση Live Αγώνων"):
    try:
        response = requests.get(URL, headers=HEADERS)
        
        # Ρύθμιση της κωδικοποίησης σε utf-8
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            data = response.json()
            # Εμφάνιση των δεδομένων με ασφαλή τρόπο
            st.json(data) 
        else:
            st.error(f"Σφάλμα σύνδεσης: {response.status_code}")
    except Exception as e:
        st.error(f"Πρόβλημα: {str(e)}")
