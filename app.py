import streamlit as st
import os
import json
from datetime import datetime

st.set_page_config(page_title="Προγνωστικά Στοιχήματος", page_icon="⚽", layout="centered")

st.title("⚽ Αγώνες & Στατιστικά Ημέρας")

today_date = datetime.now().strftime("%Y-%m-%d")
st.write(f"Πρόγραμμα αγώνων για σήμερα: **{today_date}**")

if os.path.exists("daily_predictions.txt"):
    with open("daily_predictions.txt", "r", encoding="utf-8") as f:
        content = f.read()
    
    try:
        data = json.loads(content)
        
        # Προσπάθεια λήψης των αγώνων με διάφορους εναλλακτικούς τρόπους δομής JSON
        leagues = None
        if isinstance(data, dict):
            leagues = data.get("response", {}).get("leagues") or data.get("leagues") or data.get("data")
        
        if leagues and isinstance(leagues, list):
            st.success("🔄 Τα δεδομένα ανακτήθηκαν επιτυχώς!")
            for league in leagues:
                if isinstance(league, dict):
                    league_name = league.get("name", "Πρωτάθλημα")
                    country = league.get("ccode", "Διεθνές")
                    
                    st.markdown(f"### 🏆 {country.upper()} - {league_name}")
                    
                    for match in league.get("matches", []):
                        home_team = match.get("home", {}).get("name", "Home")
                        away_team = match.get("away", {}).get("name", "Away")
                        
                        home_score = match.get("home", {}).get("score")
                        away_score = match.get("away", {}).get("score")
                        status_time = match.get("status", {}).get("time", "--:--")
                        
                        score_text = f"**{home_score} - {away_score}**" if home_score is not None else "🆚"
                        st.write(f"⚫ **{home_team}** {score_text} **{away_team}** | 🕒 *{status_time}*")
        else:
            # Αν η δομή είναι διαφορετική, δείχνουμε τα δεδομένα απευθείας για έλεγχο
            st.info("📊 Εμφάνιση διαθέσιμων δεδομένων από το API:")
            st.json(data)
            
    except Exception as e:
        st.error(f"Σφάλμα κατά την ανάγνωση: {e}")
        st.text_area("Αρχείο Κειμένου", value=content, height=200)
else:
    st.warning("Δεν βρέθηκαν αποθηκευμένα δεδομένα. Παρακαλώ τρέξτε το GitHub Action.")

