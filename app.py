import streamlit as st
import requests

st.title("⚽ Live Αγώνες")

# Βάλε εδώ το ΚΑΙΝΟΥΡΓΙΟ κλειδί από το FootballAppFinal
HEADERS = {
    'x-rapidapi-key': "37046cb451msh72e76cf7c6071cdp1d37a8jsn3abe46eeefe3",
    'x-rapidapi-host': "free-api-live-football-data.p.rapidapi.com"
}

URL = "https://free-api-live-football-data.p.rapidapi.com/football-livescore"

if st.button("Εμφάνιση Live Αγώνων"):
    try:
        response = requests.get(URL, headers=HEADERS)
        response.encoding = 'utf-8' # Αυτό λύνει το πρόβλημα latin-1
        
        if response.status_code == 200:
            data = response.json()
            matches = data.get("response", [])
            
            if matches:
                for match in matches:
                    home = match.get('homeTeam', {}).get('name', 'Home')
                    away = match.get('awayTeam', {}).get('name', 'Away')
                    st.write(f"⚽ {home} vs {away}")
            else:
                st.info("Δεν βρέθηκαν live αγώνες αυτή τη στιγμή.")
        else:
            st.error(f"Σφάλμα: {response.status_code}. Δοκίμασε ξανά σε λίγο.")
    except Exception as e:
        st.error(f"Πρόβλημα: {e}")
