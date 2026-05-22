import streamlit as st
import requests

st.title("⚽ Live Scores (ApiFootball)")

# Χρήση του σωστού endpoint που επιτρέπεται στο πλάνο σου
URL = "https://apifootball3.p.rapidapi.com/"
# Η παράμετρος 'get_fixtures' είναι ανοιχτή στο πλάνο σου
params = {"action": "get_fixtures", "match_live": "1"}

HEADERS = {
    "x-rapidapi-key": "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561",
    "x-rapidapi-host": "apifootball3.p.rapidapi.com"
}

def get_data():
    response = requests.get(URL, headers=HEADERS, params=params)
    return response.json()

data = get_data()

if isinstance(data, list):
    for match in data:
        st.write(f"🏆 {match['league_name']}")
        st.write(f"⚽ {match['match_hometeam_name']} {match['match_hometeam_score']} - {match['match_awayteam_score']} {match['match_awayteam_name']}")
        st.write("---")
else:
    st.info("🕒 Δεν υπάρχουν ζωντανοί αγώνες αυτή τη στιγμή.")

