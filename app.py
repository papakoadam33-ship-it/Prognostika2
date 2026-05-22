import streamlit as st
import requests

st.set_page_config(page_title="Προγνωστικά Στοιχήματος", page_icon="⚽", layout="centered")
st.title("⚽ Live Αγώνες & Στατιστικά")

# Δοκιμάζουμε το βασικό endpoint για live σκορ (χωρίς ημερομηνία στο URL)
URL_LIVE = "https://free-api-live-football-data.p.rapidapi.com/football-current-live"

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
    st.success("✅ Επιτυχής σύνδεση με το API!")
    
    # Εμφάνιση των live δεδομένων
    all_matches = data.get("response", {}).get("matches", [])
    
    if not all_matches:
        st.info("🕒 Αυτή τη στιγμή δεν υπάρχουν ζωντανοί αγώνες σε εξέλιξη.")
    else:
        for match in all_matches:
            home_team = match.get("home", {}).get("name", "Home")
            away_team = match.get("away", {}).get("name", "Away")
            home_score = match.get("home", {}).get("score", "0")
            away_score = match.get("away", {}).get("score", "0")
            status = match.get("status", {}).get("type", "LIVE")
            
            st.write(f"⚽ **{home_team}** {home_score} - {away_score} **{away_team}** | *Κατάσταση: {status}*")
            st.write("---")
            
elif data and "error_status" in data:
    st.error(f"⚠️ Το API επέστρεψε σφάλμα: Status Code {data['error_status']}")
    st.info("💡 Αν επιμένει το σφάλμα, περιμένουμε το ακριβές URL από την Elaine για το Free Plan.")
else:
    st.error("⚠️ Αδυναμία σύνδεσης.")
