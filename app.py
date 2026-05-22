import streamlit as st
import requests

st.set_page_config(page_title="Προγνωστικά Στοιχήματος", page_icon="⚽", layout="centered")

st.title("⚽ Live Αγώνες & Έξυπνα Προγνωστικά")
st.write("🤖 *Δημιουργία live προβλέψεων μέσω του ελεύθερου Livescore feed.*")

# Χρήση του βασικού URL και της σωστής παραμέτρου δράσης
URL_API = "https://apifootball3.p.rapidapi.com/"
querystring = {"action": "get_livescore"}

HEADERS = {
    "x-rapidapi-key": "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561",
    "x-rapidapi-host": "apifootball3.p.rapidapi.com"
}

def generate_live_tip(home_score, away_score, status_text):
    try:
        home_s = int(home_score)
        away_s = int(away_score)
        total_goals = home_s + away_s
    except:
        return "📊 Αναμονή live ροής για υπολογισμό προγνωστικού"

    # Προσπάθεια εξαγωγής του λεπτού
    time_clean = "".join(filter(str.isdigit, str(status_text)))
    minute = int(time_clean) if time_clean else 45
    
    if minute >= 75 and minute <= 88:
        if total_goals == 0:
            return "🎯 **Πρόβλεψη: Late Over 0.5** (Αυξημένο ρίσκο στο τέλος του αγώνα)."
        elif home_s == 1 and away_s == 1:
            return "🔥 **Πρόβλεψη: Over 2.5 (Goal/Goal Live)** (Ανοιχτό παιχνίδι με εκατέρωθεν ευκαιρίες)."
        elif abs(home_s - away_s) == 1:
            return "⚠️ **Πρόβλεψη: Πίεση για Ισοπαλία** (Η ομάδα που υπολείπεται ανεβάζει τις γραμμές της)."
    if minute > 15 and minute < 35 and total_goals == 0:
        return "⏳ **Πρόβλεψη: Over 0.5 Ημίχρονο** (Ανεβαίνει η ένταση στο παιχνίδι)."
    if minute < 60 and total_goals >= 3:
        return "🚀 **Πρόβλεψη: Over {}.5** (Πολύ γρήγορος ρυθμός, ευάλωτες άμυνες).".format(total_goals + 1)
    
    if total_goals == 0:
        return "📋 **Πρόβλεψη: Under 2.5** (Παιχνίδι κέντρου και σκοπού σκοπιμότητας)."
    else:
        return "📈 **Πρόβλεψη: Live Ποντάρισμα στο Over {}.5**".format(total_goals + 0.5)

@st.cache_data(ttl=20)
def get_football_data_now():
    try:
        response = requests.get(URL_API, headers=HEADERS, params=querystring)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error_status": response.status_code}
    except Exception as e:
        return {"error_msg": str(e)}

with st.spinner("⏳ Ανάκτηση live σκορ..."):
    data = get_football_data_now()

if data and "error_status" not in data and "error_msg" not in data:
    # Έλεγχος αν η απάντηση έχει σφάλμα από το ίδιο το API
    if isinstance(data, dict) and "error" in data:
        st.info("🕒 Δεν υπάρχουν ζωντανοί αγώνες αυτή τη στιγμή στη ροή δεδομένων.")
    else:
        all_matches = data if isinstance(data, list) else data.get("response", [])
        
        if not all_matches:
            st.info("🕒 Δεν εντοπίστηκαν live αναμετρήσεις σε εξέλιξη.")
        else:
            st.success(f"🤖 Ο αλγόριθμος επεξεργάζεται {len(all_matches)} ζωντανά παιχνίδια!")
            for match in all_matches:
                league_name = match.get("league_name", "Πρωτάθλημα")
                country = match.get("country_name", "")
                home_team = match.get("match_hometeam_name", "Home")
                away_team = match.get("match_awayteam_name", "Away")
                home_score = match.get("match_hometeam_score", "0")
                away_score = match.get("match_awayteam_score", "0")
                match_time = match.get("match_status", "LIVE")
                
                st.markdown(f"#### 🏆 {country} - {league_name}")
                st.write(f"⚽ **{home_team}** {home_score} - {away_score} **{away_team}**")
                st.caption(f"🕒 *Κατάσταση: {match_time}*")
                
                tip = generate_live_tip(home_score, away_score, match_time)
                st.info(tip)
                st.write("---")
elif data and "error_status" in data:
    st.error(f"⚠️ Σφάλμα σύνδεσης: Status Code {data['error_status']}")
else:
    st.error("⚠️ Αδυναμία λήψης δεδομένων.")

