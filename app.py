import streamlit as st
import os
import json
from datetime import datetime

st.set_page_config(page_title="Προγνωστικά Στοιχήματος", page_icon="⚽", layout="centered")

st.title("⚽ Αγώνες & Στατιστικά Ημέρας")

today_date = datetime.now().strftime("%Y-%m-%d")
st.write(f"Καλώς ορίσατε! Πρόγραμμα αγώνων για σήμερα: **{today_date}**")

if os.path.exists("daily_predictions.txt"):
    with open("daily_predictions.txt", "r", encoding="utf-8") as f:
        content = f.read()
    
    try:
        data = json.loads(content)
        leagues = data.get("response", {}).get("leagues", [])
        
        if not leagues:
            st.info("📅 Δεν υπάρχουν προγραμματισμένοι αγώνες στο API για σήμερα.")
        
        for league in leagues:
            league_name = league.get("name", "Πρωτάθλημα")
            country = league.get("ccode", "Διεθνές")
            
            st.markdown(f"### 🏆 {country.upper()} - {league_name}")
            
            for match in league.get("matches", []):
                home_team = match.get("home", {}).get("name", "Home")
                away_team = match.get("away", {}).get("name", "Away")
                
                # Έλεγχος αν υπάρχουν σκορ
                home_score = match.get("home", {}).get("score")
                away_score = match.get("away", {}).get("score")
                
                # Ώρα έναρξης ή κατάσταση αγώνα
                status_time = match.get("status", {}).get("time", "--:--")
                
                if home_score is not None and away_score is not None:
                    score_text = f"**{home_score} - {away_score}**"
                else:
                    score_text = "🆚"
                
                st.write(f"⚫ **{home_team}** {score_text} **{away_team}** | 🕒 *{status_time}*")
                
    except Exception as e:
        st.error("Σφάλμα κατά την ανάγνωση των δεδομένων.")
        st.text_area("Δεδομένα Αρχείου", value=content, height=200)
else:
    st.warning("Δεν βρέθηκαν αποθηκευμένα δεδομένα αγώνων. Παρακαλώ τρέξτε το GitHub Action.")
