import streamlit as st
import requests

st.title("⚽ Live Αγώνες")

HEADERS = {
    'x-rapidapi-key': "ΤΟ_ΝΕΟ_ΣΟΥ_ΚΛΕΙΔΙ", # <--- Βάλε εδώ το νέο σου κλειδί!
    'x-rapidapi-host': "free-api-live-football-data.p.rapidapi.com"
}

# Δοκιμάζουμε το endpoint 'livescores' αντί για 'football-livescore'
# Πολλά API χρησιμοποιούν πληθυντικό
URL = "https://free-api-live-football-data.p.rapidapi.com/livescores"

if st.button("Εμφάνιση Live Αγώνων"):
    try:
        response = requests.get(URL, headers=HEADERS)
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            data = response.json()
            # Ανάλογα με το τι θα επιστρέψει, ίσως χρειαστεί να αλλάξουμε το 'response'
            st.write(data) 
        elif response.status_code == 404:
            st.error("Σφάλμα 404: Το URL δεν βρέθηκε. Το API ίσως έχει άλλο path.")
        else:
            st.error(f"Σφάλμα: {response.status_code}")
    except Exception as e:
        st.error(f"Πρόβλημα: {str(e)}")

