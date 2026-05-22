import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Προγνωστικά Στοιχήματος", page_icon="⚽", layout="centered")

st.title("⚽ Live Αγώνες & Στατιστικά")

today_date = datetime.now().strftime("%Y-%m-%d")
st.write(f"📅 Ημερομηνία: **{today_date}**")

# Η επίσημη διεύθυνση endpoint για το ApiFootball
URL_LIVE = "https://apifootball3.p.rapidapi.com/"
querystring = {"action": "get_livescore"}

HEADERS = {
    "x-rapidapi-key": "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561",
    "x-rapidapi-host": "apifootball3.p.rapidapi.com"
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

with st.spinner("⏳ Φόρτωση ζωντανών αγώνων..."):
    data = get_football_data_now()

if data and "error_status" not in data and "error_msg" not in data:
    if isinstance(data, list):
        st.success(f"🔥 Αυτή τη στιγμή υπάρχουν {len(data)} ζωντανοί αγώνες!")
        for match in data:
            league_name = match.get("league_name", "Πρωτάθλημα")
            country_name = match.get("country_name", "Χώρα")
            home_team = match.get("match_hometeam_name", "Home")
            away_team = match.get("match_awayteam_name", "Away")
            home_score = match.get("match_hometeam_score", "0")
            away_score = match.get("match_awayteam_score", "0")
            match_time = match.get("match_status", "LIVE")
            
            st.markdown(f"### 🏆 {country_name} - {league_name}")
            st.write(f"🔴 **{home_team}** {home_score} - {away_score} **{away_team}** | 🕒 *Λεπτό: {match_time}*")
            st.write("---")
    elif isinstance(data, dict) and "error" in data:
        st.info("🕒 Δεν υπάρχουν live αγώνες αυτή τη στιγμή.")
    else:
        st.json(data)
elif data and "error_status" in data:
    st.error(f"⚠️ Το API επέστρεψε σφάλμα: Status Code {data['error_status']}")
    if data['error_status'] == 401:
        st.info("💡 Το σφάλμα 401 σημαίνει ότι πρέπει να βεβαιωθείς πως έχεις πατήσει το κουμπί Subscribe στο Free Plan του ApiFootball μέσα στο RapidAPI.")
else:
    st.error("⚠️ Αδυναμία σύνδεσης.")
