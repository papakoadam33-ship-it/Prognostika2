import streamlit as st
import requests

st.title("⚽ Live Αγώνες")

HEADERS = {
    'x-rapidapi-key': "ΤΟ_ΝΕΟ_ΣΟΥ_ΚΛΕΙΔΙ", #37046cb451msh72e76cf7c6071cdp1d37a8jsn3abe46eeefe3
    'x-rapidapi-host': "free-api-live-football-data.p.rapidapi.com"
}
# Το σωστό endpoint για live αγώνες
URL = "https://free-api-live-football-data.p.rapidapi.com/football-livescore"

if st.button("Εμφάνιση Live Αγώνων"):
    try:
        response = requests.get(URL, headers=HEADERS)
        
        if response.status_code == 200:
            data = response.json()
            # Προσαρμόζουμε το path ανάλογα με τη δομή του JSON του API
            matches = data.get("response", [])
            
            if matches:
                for match in matches:
                    home = match.get('homeTeam', {}).get('name', 'Home')
                    away = match.get('awayTeam', {}).get('name', 'Away')
                    score = match.get('score', {}).get('fulltime', '0-0')
                    st.write(f"⚽ {home} {score} {away}")
            else:
                st.info("Δεν υπάρχουν ζωντανοί αγώνες αυτή τη στιγμή.")
        else:
            st.error(f"Σφάλμα σύνδεσης: {response.status_code}")
    except Exception as e:
        st.error(f"Πρόβλημα: {e}")

