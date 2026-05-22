import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Προγνωστικά Στοιχήματος", page_icon="⚽", layout="centered")

st.title("⚽ Live Αγώνες & Στατιστικά")

today_date = datetime.now().strftime("%Y-%m-%d")
st.write(f"📅 Ημερομηνία: **{today_date}**")

# Το σωστό live endpoint που υπάρχει σίγουρα στο μενού του API σου
url = "https://free-api-live-football-data.p.rapidapi.com/football-get-live-all-matches"

headers = {
    "x-rapidapi-key": "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561",
    "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
}

@st.cache_data(ttl=60)  # Ανανέωση κάθε 1 λεπτό για live σκορ
def load_real_live_data():
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Σφάλμα API (Status Code: {response.status_code})"}
    except Exception as e:
        return {"error": str(e)}

with st.spinner("⏳ Σύνδεση με το Live κουπόνι..."):
    data = load_real_live_data()

if data and "error" not in data:
    leagues = data.get("response", {}).get("leagues", [])
    
    if not leagues:
        st.info("🕒 Αυτή τη στιγμή δεν υπάρχουν αγώνες σε εξέλιξη (Live). Μόλις ξεκινήσουν τα πρώτα παιχνίδια, τα σκορ θα εμφανιστούν εδώ αυτόματα!")
    else:
        st.success(f"🔥 Αυτή τη στιγμή παίζουν {len(leagues)} πρωταθλήματα live!")
        
        for league in leagues:
            league_name = league.get("name", "Πρωτάθλημα")
            country = league.get("ccode", "Διεθνές")
            
            st.markdown(f"### 🏆 {country.upper()} - {league_name}")
            
            for match in league.get("matches", []):
                home_team = match.get("home", {}).get("name", "Home")
                away_team = match.get("away", {}).get("name", "Away")
                
                # Ζωντανά Σκορ
                home_score = match.get("home", {}).get("score", "0")
                away_score = match.get("away", {}).get("score", "0")
                
                # Λεπτό/Κατάσταση (π.χ. 45', Ημίχρονο)
                status_time = match.get("status", {}).get("time", "LIVE")
                
                st.write(f"🔴 **{home_team}** {home_score} - {away_score}  **{away_team}** | 🕒 *Λεπτό: {status_time}*")
else:
    st.error("⚠️ Πρόβλημα κατά την ανάκτηση των δεδομένων.")
    if data and "error" in data:
        st.code(data["error"])
