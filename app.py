import streamlit as st
import requests

st.title("⚽ Live Αγώνες")

HEADERS = {
    'x-rapidapi-key': "ΤΟ_ΚΛΕΙΔΙ_ΣΟΥ", # Βάλε εδώ το κλειδί σου
    'x-rapidapi-host': "free-api-live-football-data.p.rapidapi.com"
}
URL = "https://free-api-live-football-data.p.rapidapi.com/football-livescore"

if st.button("Εμφάνιση Live Αγώνων"):
    try:
        response = requests.get(URL, headers=HEADERS)
        response.encoding = 'utf-8' # Λύνει το πρόβλημα με τα ελληνικά
        
        if response.status_code == 200:
            data = response.json()
            # Εδώ παίρνουμε τα δεδομένα και τα εμφανίζουμε όμορφα
            matches = data.get("response", [])
            
            if matches:
                st.success(f"Βρέθηκαν {len(matches)} αγώνες:")
                for match in matches:
                    # Εμφανίζουμε τις ομάδες και το σκορ
                    st.write(f"🏟️ {match.get('homeTeam', {}).get('name')} vs {match.get('awayTeam', {}).get('name')} | Σκορ: {match.get('score', {}).get('fulltime')}")
            else:
                st.info("Δεν υπάρχουν live αγώνες αυτή τη στιγμή.")
        else:
            st.error(f"Σφάλμα σύνδεσης: {response.status_code}")
    except Exception as e:
        st.error(f"Πρόβλημα: {str(e)}")

