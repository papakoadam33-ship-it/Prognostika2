import streamlit as st
import requests

st.set_page_config(page_title="Προγνωστικά Στοιχήματος", page_icon="⚽", layout="centered")
st.title("⚽ Έλεγχος Σύνδεσης API")

# Χρησιμοποιούμε το βασικό endpoint για χώρες/πρωταθλήματα που είναι πάντα ενεργό
URL_TEST = "https://apifootball.p.rapidapi.com/api/"
querystring = {"action": "get_countries"}

HEADERS = {
    "x-rapidapi-key": "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561",
    "x-rapidapi-host": "apifootball.p.rapidapi.com"
}

with st.spinner("🔄 Γίνεται δοκιμαστική κλήση στο API..."):
    try:
        response = requests.get(URL_TEST, headers=HEADERS, params=querystring)
        
        if response.status_code == 200:
            st.success("🎉 ΕΠΙΤΥΧΙΑ! Το API συνδέθηκε κανονικά!")
            data = response.json()
            
            # Δείξε μας τι σου απάντησε
            if isinstance(data, list):
                st.write(f"🌍 Βρέθηκαν {len(data)} διαθέσιμες χώρες:")
                for country in data[:10]: # Δείξε μόνο τις πρώτες 10 για οικονομία
                    st.write(f"📍 {country.get('country_name')}")
            else:
                st.json(data)
                
        elif response.status_code == 403:
            st.error("⚠️ Σφάλμα 403: Forbidden")
            st.info("Το κλειδί σου είναι σωστό, αλλά το συγκεκριμένο API χρειάζεται να πατήσεις 'Subscribe to Test' στο RapidAPI (ακόμα και για το Free Plan) για να ενεργοποιηθεί.")
        else:
            st.error(f"⚠️ Το API επέστρεψε Status Code: {response.status_code}")
            
    except Exception as e:
        st.error(f"💥 Προέκυψε σφάλμα στον κώδικα: {str(e)}")

