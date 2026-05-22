import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Προγνωστικά Στοιχήματος", page_icon="⚽", layout="centered")

st.title("⚽ Στατιστικά & Προγνωστικά")
st.write("Καλώς ορίσατε στην εφαρμογή προγνωστικών!")

# 1. Παίρνουμε τη σημερινή ημερομηνία live
today_date = datetime.now().strftime("%Y-%m-%d")
st.subheader(f"📅 Αγώνες για σήμερα: {today_date}")

# 2. Καλούμε το API απευθείας από την εφαρμογή
url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-matches-by-date"
querystring = {"date": today_date}
headers = {
    "x-rapidapi-key": "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561",
    "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
}

@st.cache_data(ttl=3600) # Κρατάει τα δεδομένα στη μνήμη για 1 ώρα για να μην χαλάει requests
def get_live_data():
    try:
        response = requests.get(url, headers=headers, params=querystring)
        return response.json()
    except:
        return None

data = get_live_data()

# 3. Εμφάνιση των σημερινών αγώνων
if data and "response" in data and "leagues" in data["response"]:
    leagues = data["response"]["leagues"]
    
    if not leagues:
        st.write("Δεν υπάρχουν προγραμματισμένοι αγώνες για σήμερα στο API.")
    
    for league in leagues:
        league_name = league.get("ccode", "") + " - " + league.get("name", "")
        st.markdown(f"### 🏆 {league_name}")
        
        for match in league.get("matches", []):
            home_team = match.get("home", {}).get("name", "Home")
            away_team = match.get("away", {}).get("name", "Away")
            status = match.get("status", {}).get("time", "")
            
            # Εμφάνιση κάθε αγώνα όμορφα
            st.write(f"⚫ {home_team} 🆚 {away_team}  |  *Ώρα/Κατάσταση: {status}*")
else:
    st.error("Αδυναμία σύνδεσης με το API ή εξαντλήθηκαν τα δωρεάν requests για σήμερα.")

