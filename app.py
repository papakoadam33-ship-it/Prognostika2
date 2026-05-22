import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Προγνωστικά Στοιχήματος", page_icon="⚽", layout="centered")

st.title("⚽ Live Αγώνες & Στατιστικά (ApiFootball)")

today_date = datetime.now().strftime("%Y-%m-%d")
st.write(f"📅 Ημερομηνία: **{today_date}**")

# Το ΣΩΣΤΟ URL και Host για το API που δείχνει το screenshot σου
URL_LIVE = "https://apifootball.p.rapidapi.com/api/"

# Εδώ ζητάμε τους live αγώνες της ημέρας (action=get_events)
querystring = {"action": "get_events", "match_live": "1"}

HEADERS = {
    "x-rapidapi-key": "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561",
    "x-rapidapi-host": "apifootball.p.rapidapi.com"
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

# Εμφάνιση των αποτελεσμάτων
if data and "error_status" not in data and "error_msg" not in data:
    if isinstance(data, list):
        st.success(f"🔥 Βρέθηκαν {len(data)} ζωντανοί αγώνες!")
        
        for match in data:
            league_name = match.get("league_name", "Πρωτάθλημα")
            country_name = match.get("country_name", "Χώρα")
            
            home_team = match.get("match_hometeam_name", "Home")
            away_team = match.get("match_awayteam_name", "Away")
            
            home_score = match.get("match_hometeam_score", "0")
            away_score = match.get("match_awayteam_score", "0")
            match_time = match.get("match_time", "LIVE")
            
            st.markdown(f"🏆 **{country_name} - {league_name}**")
            st.write(f"🔴 **{home_team}** {home_score} - {away_score} **{away_team}** | 🕒 Λεπτό: {match_time}")
            st.write("---")
    else:
        # Αν δεν έχει live αγώνες αυτή τη στιγμή, το API συνήθως επιστρέφει ένα μήνυμα λάθους
        if "error" in data:
            st.info("🕒 Αυτή τη στιγμή δεν υπάρχουν live αγώνες σε εξέλιξη. Μόλις ξεκινήσουν τα παιχνίδια, θα εμφανιστούν εδώ!")
        else:
            st.json(data)

elif data and "error_status" in data:
    st.error(f"⚠️ Το API επέστρεψε σφάλμα: Status Code {data['error_status']}")
else:
    st.error("⚠️ Αδυναμία σύνδεσης στο δίκτυο.")

