import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Προγνωστικά Στοιχήματος", page_icon="⚽", layout="centered")

st.title("⚽ Live Αγώνες & Στατιστικά")

today_date = datetime.now().strftime("%Y-%m-%d")
st.write(f"📅 Ημερομηνία: **{today_date}**")

# Δοκιμάζουμε το εναλλακτικό endpoint της αρχικής επιτυχίας
URL_LIVE = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-matches-by-date"
querystring = {"date": today_date}

HEADERS = {
    "x-rapidapi-key": "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561",
    "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
}

@st.cache_data(ttl=30)  
def get_football_data_now():
    try:
        response = requests.get(URL_LIVE, headers=HEADERS, params=querystring)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error_status": response.status_code}
    except Exception as e:
        return {"error_msg": str(e)}

with st.spinner("⏳ Φόρτωση αγώνων..."):
    data = get_football_data_now()

# Εμφάνιση των δεδομένων στην οθόνη
if data and "error_status" not in data and "error_msg" not in data:
    st.success("✅ Επιτυχής σύνδεση με το API!")
    
    # Αν το API επιστρέψει τη δομή που είδαμε στην αρχή
    if "response" in data:
        st.json(data["response"])
    else:
        st.json(data)

elif data and "error_status" in data:
    st.error(f"⚠️ Το API επέστρεψε σφάλμα: Status Code {data['error_status']}")
    st.info("💡 Αν εμφανίζει ακόμα 404, περιμένουμε την απάντηση της υποστήριξης για το ποιο είναι το σωστό URL του Free Plan.")
else:
    st.error("⚠️ Αδυναμία σύνδεσης στο δίκτυο.")

