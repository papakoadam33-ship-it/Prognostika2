import streamlit as st
import os
import json

st.set_page_config(page_title="Προγνωστικά Στοιχήματος", page_icon="⚽", layout="centered")

st.title("⚽ Live Αγώνες & Στατιστικά")
st.write("Καλώς ορίσατε στην εφαρμογή προγνωστικών!")

if os.path.exists("daily_predictions.txt"):
    with open("daily_predictions.txt", "r", encoding="utf-8") as f:
        content = f.read()
    
    try:
        data = json.loads(content)
        leagues = data.get("response", {}).get("leagues", [])
        
        if not leagues:
            st.info("🕒 Δεν υπάρχουν live αγώνες αυτή τη στιγμή στο API. Δοκιμάστε αργότερα όταν θα έχει σέντρα!")
        
        for league in leagues:
            league_name = league.get("name", "Πρωτάθλημα")
            country = league.get("ccode", "Διεθνές")
            
            st.markdown(f"### 🏆 {country.upper()} - {league_name}")
            
            for match in league.get("matches", []):
                home_team = match.get("home", {}).get("name", "Home")
                away_team = match.get("away", {}).get("name", "Away")
                
                # Live Σκορ
                home_score = match.get("home", {}).get("score", "0")
                away_score = match.get("away", {}).get("score", "0")
                
                # Λεπτό αγώνα ή κατάσταση
                status_time = match.get("status", {}).get("time", "LIVE")
                
                st.write(f"🔴 **{home_team}** {home_score} - {away_score}  **{away_team}** |  *Λεπτό: {status_time}*")
                
    except Exception as e:
        st.error("Σφάλμα κατά την ανάγνωση των δεδομένων.")
        st.text_area("Δεδομένα Αρχείου", value=content, height=200)
else:
    st.warning("Δεν βρέθηκαν αποθηκευμένα δεδομένα αγώνων. Παρακαλώ τρέξτε το GitHub Action.")
