import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Προγνωστικά Στοιχήματος", page_icon="⚽", layout="centered")

st.title("⚽ Live Αγώνες & Στατιστικά")

today_date = datetime.now().strftime("%Y-%m-%d")
st.write(f"📅 Ημερομηνία: **{today_date}**")

# Επιστροφή στο σωστό, ενεργοποιημένο API από το γράφημά σου
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

with st.spinner("⏳ Φόρτωση αγώνων της ημέρας..."):
    data = get_football_data_now()

if data and "error_status" not in data and "error_msg" not in data:
    st.success("✅ Επιτυχής σύνδεση με το API!")
    
    # Ανάγνωση των αγώνων από τη σωστή δομή του Free API Live Football Data
    all_matches = data.get("response", {}).get("matches", [])
    
    if not all_matches:
        st.info("🕒 Δεν βρέθηκαν αγώνες προγραμματισμένοι για σήμερα ή το API δεν έχει διαθέσιμα δεδομένα αυτή τη στιγμή.")
    else:
        for match in all_matches:
            home_team = match.get("home", {}).get("name", "Home")
            away_team = match.get("away", {}).get("name", "Away")
            home_score = match.get("home", {}).get("score", "0")
            away_score = match.get("away", {}).get("score", "0")
            status = match.get("status", {}).get("type", "NS")
            
            st.write(f"⚽ **{home_team}** {home_score} - {away_score} **{away_team}** | *Κατάσταση: {status}*")
            st.write("---")
            
elif data and "error_status" in data:
    st.error(f"⚠️ Το API επέστρεψε σφάλμα: Status Code {data['error_status']}")
else:
    st.error("⚠️ Αδυναμία σύνδεσης στο δίκτυο.")
