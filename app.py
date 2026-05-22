import streamlit as st
import requests

st.set_page_config(page_title="Προγνωστικά Στοιχήματος", page_icon="⚽", layout="centered")

st.title("⚽ Live Αγώνες & Έξυπνα Προγνωστικά")
st.write("🤖 *Ο αλγόριθμος αναλύει τα live δεδομένα σε πραγματικό χρόνο!*")

# Επιστροφή στο σωστό και δωρεάν API
URL_LIVE = "https://free-api-live-football-data.p.rapidapi.com/football-current-live"

HEADERS = {
    "x-rapidapi-key": "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561",
    "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
}

def generate_live_tip(home_score, away_score, minute):
    try:
        home_s = int(home_score)
        away_s = int(away_score)
        total_goals = home_s + away_s
    except:
        return "📊 Αναμονή live δεδομένων για ασφαλή πρόβλεψη"

    # 1. Σενάριο Late Goal (75'+)
    if minute >= 75 and minute <= 88:
        if total_goals == 0:
            return "🎯 **Πρόβλεψη: Late Over 0.5** (Οι ομάδες θα ρισκάρουν στα τελευταία λεπτά)."
        elif home_s == 1 and away_s == 1:
            return "🔥 **Πρόβλεψη: Over 2.5 (Goal/Goal Live)** (Ανοιχτό παιχνίδι, αμοιβαία ρίσκα)."
        elif abs(home_s - away_s) == 1:
            return "⚠️ **Πρόβλεψη: Πίεση για Ισοπαλία** (Πιθανό γκολ στις καθυστερήσεις)."

    # 2. Σενάριο Πρώτου Ημιχρόνου (15'-35')
    if minute > 15 and minute < 35 and total_goals == 0:
        return "⏳ **Πρόβλεψη: Over 0.5 Ημίχρονο** (Ανεβαίνει ο ρυθμός, αξίζει στο live)."

    # 3. Σενάριο Πολλά Γκολ
    if minute < 60 and total_goals >= 3:
        return "🚀 **Πρόβλεψη: Over {}.5** (Καταιγιστικός ρυθμός, ευάλωτες άμυνες).".format(total_goals + 1)

    if total_goals == 0:
        return "📋 **Πρόβλεψη: Under 2.5** (Παιχνίδι κλειστής τακτικής, λίγες φάσεις)."
    else:
        return "📈 **Πρόβλεψη: Live Στοίχημα στο Over {}.5**".format(total_goals + 0.5)


@st.cache_data(ttl=15)
def get_football_data_now():
    try:
        response = requests.get(URL_LIVE, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error_status": response.status_code}
    except Exception as e:
        return {"error_msg": str(e)}


with st.spinner("⏳ Ανάλυση live αγώνων..."):
    data = get_football_data_now()

if data and "error_status" not in data and "error_msg" not in data:
    # Καθαρισμός και λήψη των αγώνων από τη σωστή δομή του Free API
    all_matches = data.get("response", {}).get("live", [])
    
    if not all_matches:
        st.info("🕒 Αυτή τη στιγμή δεν υπάρχουν ζωντανοί αγώνες σε εξέλιξη (ή το δωρεάν API δεν καλύπτει τα τρέχοντα πρωταθλήματα).")
    else:
        st.success(f"🤖 Ο αλγόριθμος αναλύει {len(all_matches)} ζωντανά παιχνίδια!")
        
        for match in all_matches:
            # Σωστά κλειδιά για το Free API Live Football Data
            home_team = match.get("homeTeam", {}).get("name", "Home")
            away_team = match.get("awayTeam", {}).get("name", "Away")
            home_score = match.get("homeScore", {}).get("current", 0)
            away_score = match.get("awayScore", {}).get("current", 0)
            
            # Λεπτό αγώνα
            status = match.get("status", {})
            minute = status.get("liveTime", {}).get("minutes", 0)
            
            # Εμφάνιση
            st.markdown(f"#### ⚽ {home_team} {home_score} - {away_score} {away_team}")
            st.caption(f"🕒 *Λεπτό: {minute}'*")
            
            # Παραγωγή προγνωστικού
            tip = generate_live_tip(home_score, away_score, minute)
            st.info(tip)
            st.write("---")
            
elif data and "error_status" in data:
    st.error(f"⚠️ Σφάλμα API: Status Code {data['error_status']}")
else:
    st.error("⚠️ Αδυναμία σύνδεσης.")

