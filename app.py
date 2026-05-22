import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Προγνωστικά Στοιχήματος", page_icon="⚽", layout="centered")

st.title("⚽ Αγώνες & Στατιστικά Ημέρας")

# Παίρνουμε τη σημερινή ημερομηνία αυτόματα (2026)
today_date = datetime.now().strftime("%Y-%m-%d")
st.write(f"📅 Πρόγραμμα αγώνων για σήμερα: **{today_date}**")

# Απευθείας κλήση στο API
url = "https://free-api-live-football-data.p.rapidapi.com/football-get-all-matches-by-date"
querystring = {"date": today_date}

headers = {
    "x-rapidapi-key": "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561",
    "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
}

@st.cache_data(ttl=600)  # Κρατάει τα δεδομένα στη μνήμη για 10 λεπτά για οικονομία στα requests
def load_live_data():
    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Σφάλμα API (Status Code: {response.status_code})"}
    except Exception as e:
        return {"error": str(e)}

with st.spinner("⏳ Φόρτωση σημερινών αγώνων live από το API..."):
    data = load_live_data()

if data and "error" not in data:
    # Διάβασμα των πρωταθλημάτων από την πραγματική δομή του API
    leagues = data.get("response", {}).get("leagues", [])
    
    if not leagues:
        st.info("📅 Δεν υπάρχουν διαθέσιμοι αγώνες στο API για σήμερα.")
    else:
        st.success(f"🔄 Βρέθηκαν {len(leagues)} διοργανώσεις live!")
        
        for league in leagues:
            league_name = league.get("name", "Πρωτάθλημα")
            country = league.get("ccode", "Διεθνές")
            
            # Εμφάνιση Τίτλου Πρωταθλήματος
            st.markdown(f"### 🏆 {country.upper()} - {league_name}")
            
            for match in league.get("matches", []):
                home_team = match.get("home", {}).get("name", "Home")
                away_team = match.get("away", {}).get("name", "Away")
                
                # Σκορ (αν υπάρχει)
                home_score = match.get("home", {}).get("score")
                away_score = match.get("away", {}).get("score")
                
                # Κατάσταση ή Ώρα έναρξης
                status_time = match.get("status", {}).get("time", "--:--")
                
                if home_score is not None and away_score is not None:
                    score_text = f"**{home_score} - {away_score}**"
                else:
                    score_text = "🆚"
                
                st.write(f"⚫ **{home_team}** {score_text} **{away_team}** | 🕒 *{status_time}*")
else:
    st.error("⚠️ Αδυναμία σύνδεσης με το API.")
    if data and "error" in data:
        st.code(data["error"])

