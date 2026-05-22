import streamlit as st
import requests

st.title("⚽ Football Player Search")

# Το νέο σου API
URL = "https://free-api-live-football-data.p.rapidapi.com/football-players-search"
HEADERS = {
    'x-rapidapi-key': "37046cb451msh72e76cf7c6071cdp1d37a8jsn3abe46eeefe3",
    'x-rapidapi-host': "free-api-live-football-data.p.rapidapi.com"
}

# Είσοδος αναζήτησης
search_query = st.text_input("Ψάξε έναν παίκτη (π.χ. messi):", "messi")

if st.button("Αναζήτηση"):
    params = {"search": search_query}
    try:
        response = requests.get(URL, headers=HEADERS, params=params)
        if response.status_code == 200:
            data = response.json()
            st.success("Βρέθηκαν αποτελέσματα!")
            st.json(data) # Εμφανίζει τα δεδομένα που επιστρέφει το API
        else:
            st.error(f"Σφάλμα {response.status_code}: Κάτι δεν πήγε καλά.")
    except Exception as e:
        st.error(f"Πρόβλημα: {e}")

