import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Προγνωστικά Στοιχήματος", page_icon="⚽", layout="centered")

st.title("⚽ Live Αγώνες & Στατιστικά")

today_date = datetime.now().strftime("%Y-%m-%d")
st.write(f"📅 Ημερομηνία: **{today_date}**")

# Το σωστό live endpoint που υποστηρίζει το API σου
URL_LIVE = "https://free-api-live-football-data.p.rapidapi.com/football-get-live-all-matches"

HEADERS = {
    "x-rapidapi-key": "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561",
    "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
}

@st.cache_data(ttl=30)  
def get_football_data_now():
    try:
        response = requests.get(URL_LIVE, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error_status": response.status_code}
    except Exception as e:
        return {"error_msg": str(e)}

with st.spinner("⏳ Φόρτωση ζωντανών αγώνων..."):
    data = get_football_data_now()

if data and "error_status" not in data and "error_msg" not in data:
    leagues = data.get("response", {}).get("leagues", [])
    
    if not leagues:
        st.info("🕒 Αυτή τη στιγμή δεν υπάρχουν αγώνες σε εξέλιξη (Live). Μόλις ξεκινήσουν τα πρώτα παιχνίδια της ημέρας, τα σκορ θα εμφανιστούν εδώ αυτόματα!")
    else:
        st.success(f"🔥 Αυτή τη στιγμή παίζουν {len(leagues)} διοργανώσεις live!")
        
        for league in leagues:
            league_name = league.get("name", "Πρωτάθλημα")
            country = league.get("ccode", "Διεθνές")
            
            st.markdown(f"### 🏆 {country.upper()} - {league_name}")
            
            for match in league.get("matches", []):
                home_team = match.get("home", {}).get("name", "Home")
                away_team = match.get("away", {}).get("name", "Away")
                
                home_score = match.get("home", {}).get("score", "0")
                away_score = match.get("away", {}).get("score", "0")
                status_time = match.get("status", {}).get("time", "LIVE")
                
                st.write(f"🔴 **{home_team}** {home_score} - {away_score}  **{away_team}** | 🕒 *Λεπτό: {status_time}*")

elif data and "error_status" in data:
    st.error(f"⚠️ Το API επέστρεψε σφάλμα: Status Code {data['error_status']}")
else:
    st.error("⚠️ Αδυναμία σύνδεσης στο δίκτυο.")

