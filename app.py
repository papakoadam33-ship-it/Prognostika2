import streamlit as st
import http.client
import json

st.title("⚽ Live Αγώνες")

# Το URL και οι κεφαλίδες από τον κώδικα που βρήκες
conn = http.client.HTTPSConnection("free-api-live-football-data.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "37046cb451msh72e76cf7c6071cdp1d37a8jsn3abe46eeefe3",
    'x-rapidapi-host': "free-api-live-football-data.p.rapidapi.com"
}

if st.button("Εμφάνιση Αγώνων"):
    try:
        # Χρησιμοποιούμε το endpoint που βρήκες
        conn.request("GET", "/football-get-matches-by-date-and-league?date=20241107&league=39", headers=headers)
        
        res = conn.getresponse()
        data = res.read()
        
        if res.status == 200:
            st.success("Τα δεδομένα λήφθηκαν!")
            # Μετατρέπουμε τα δεδομένα σε μορφή που καταλαβαίνει το Streamlit
            st.json(json.loads(data.decode("utf-8")))
        else:
            st.error(f"Σφάλμα {res.status}: Κάτι δεν πήγε καλά.")
            
    except Exception as e:
        st.error(f"Πρόβλημα: {e}")

