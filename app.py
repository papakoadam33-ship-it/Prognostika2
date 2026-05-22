import streamlit as st
import requests

st.set_page_config(page_title="Προγνωστικά Στοιχήματος", page_icon="⚽", layout="centered")

st.title("⚽ Live Αγώνες & Έξυπνα Προγνωστικά")
st.write("🤖 *Ο αλγόριθμος αναλύει τα live δεδομένα και παράγει αυτόματα προγνωστικά!*")

URL_LIVE = "https://free-api-live-football-data.p.rapidapi.com/football-current-live"

HEADERS = {
    "x-rapidapi-key": "47d5da2fb8mshde110deccc94426p115d5ajsnd9cc939fa561",
    "x-rapidapi-host": "free-api-live-football-data.p.rapidapi.com"
}

# 🤖 Συναρτήση AI Αλγορίθμου για Προγνωστικά
def generate_live_tip(home_score, away_score, status_text):
    try:
        home_s = int(home_score)
        away_s = int(away_score)
        total_goals = home_s + away_s
    except:
        return "📊 Αναμονή δεδομένων για ασφαλή πρόβλεψη"

    # Καθαρισμός του κειμένου του χρόνου (π.χ. αν λέει "75'" ή "2H 75")
    time_clean = "".join(filter(str.isdigit, status_text))
    minute = int(time_clean) if time_clean else 45
    
    # 1. Σενάριο Late Goal (Πίεση στα τελευταία λεπτά)
    if minute >= 75 and minute <= 88:
        if total_goals == 0:
            return "🎯 **Πρόβλεψη: Late Over 0.5** (Το παιχνίδι είναι στο τέλος και καμία ομάδα δεν θα ρισκάρει την ισοπαλία, αναμένεται πίεση)."
        elif home_s == 1 and away_s == 1:
            return "🔥 **Πρόβλεψη: Over 2.5 (Goal/Goal Live)** (Το 1-1 στο {minute}' δείχνει ανοιχτό ρυθμό, αξίζει το ρίσκο για επόμενο γκολ)."
        elif abs(home_s - away_s) == 1:
            return "⚠️ **Πρόβλεψη: Πίεση για Ισοπαλία** (Η ομάδα που χάνει πιέζει με γεμίσματα, πιθανό Goal στο τέλος)."

    # 2. Σενάριο για το Πρώτο Ημίχρονο
    if minute > 15 and minute < 35 and total_goals == 0:
        return "⏳ **Πρόβλεψη: Over 0.5 Ημίχρονο** (Ο ρυθμός ανεβαίνει μετά το πρώτο τέταρτο, αξίζει το live ποντάρισμα)."

    # 3. Σενάριο Πολλά Γκολ / Ανοιχτό Ματς
    if minute < 60 and total_goals >= 3:
        return "🚀 **Πρόβλεψη: Over {}.5** (Ο ρυθμός είναι καταιγιστικός, οι άμυνες έχουν «μπει» στα αποδυτήρια).".format(total_goals + 1)

    # 4. Σενάριο "Κλειδωμένου" Ματς
    if minute >= 65 and abs(home_s - away_s) >= 3:
        return "🔒 **Πρόβλεψη: Under {}.5 (No More Goals)** (Το σκορ έχει ξεφύγει, οι ομάδες κάνουν συντήρηση δυνάμεων).".format(total_goals + 1.5)

    # Γενική πρόβλεψη αν δεν πιάνει τα κριτήρια
    if total_goals == 0:
        return "📋 **Πρόβλεψη: Ισοπαλία ή Under 2.5** (Κλειστό παιχνίδι τακτικής, λίγες φάσεις)."
    else:
        return "📈 **Πρόβλεψη: Live Στοίχημα στο Over {}.5**".format(total_goals + 0.5)


@st.cache_data(ttl=15)  # Μειώσαμε το χρόνο για πιο γρήγορο live refresh
def get_football_data_now():
    try:
        response = requests.get(URL_LIVE, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error_status": response.status_code}
    except Exception as e:
        return {"error_msg": str(e)}


with st.spinner("⏳ Ανάλυση αγώνων και παραγωγή προγνωστικών..."):
    data = get_football_data_now()

if data and "error_status" not in data and "error_msg" not in data:
    all_matches = data.get("response", {}).get("matches", [])
    
    if not all_matches:
        st.info("🕒 Αυτή τη στιγμή δεν υπάρχουν ζωντανοί αγώνες σε εξέλιξη. Μόλις ξεκινήσουν τα επόμενα ματς, ο αλγόριθμος θα εμφανίσει αυτόματα τις live επιλογές εδώ!")
    else:
        st.success(f"🤖 Ο αλγόριθμος αναλύει επιτυχώς {len(all_matches)} ζωντανά παιχνίδια!")
        
        for match in all_matches:
            home_team = match.get("home", {}).get("name", "Home")
            away_team = match.get("away", {}).get("name", "Away")
            home_score = match.get("home", {}).get("score", "0")
            away_score = match.get("away", {}).get("score", "0")
            status_text = match.get("status", {}).get("type", "LIVE")
            
            # Εμφάνιση του Αγώνα
            st.markdown(f"### ⚽ {home_team} {home_score} - {away_score} {away_team}")
            st.caption(f"🕒 *Κατάσταση/Λεπτό: {status_text}*")
            
            # Παραγωγή και Εμφάνιση Προγνωστικού με όμορφο Box
            tip = generate_live_tip(home_score, away_score, status_text)
            st.info(tip)
            
            st.write("---")
            
elif data and "error_status" in data:
    st.error(f"⚠️ Σφάλμα API: {data['error_status']}")
else:
    st.error("⚠️ Αδυναμία σύνδεσης.")

