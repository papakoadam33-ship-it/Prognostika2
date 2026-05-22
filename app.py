import streamlit as st
import os
import json

st.set_page_config(page_title="Προγνωστικά Στοιχήματος", page_icon="⚽", layout="centered")

st.title("⚽ Στατιστικά & Προγνωστικά")
st.write("Καλώς ορίσατε στην εφαρμογή προγνωστικών!")

if os.path.exists("daily_predictions.txt"):
    st.subheader("📊 Ανάλυση Επιλεγμένου Αγώνα")
    
    with open("daily_predictions.txt", "r", encoding="utf-8") as f:
        content = f.read()
    
    try:
        data = json.loads(content)
        match_detail = data.get("response", {}).get("detail", {})
        match_name = match_detail.get("matchName", "Άγνουστος Αγώνας")
        match_round = match_detail.get("matchRound", "-")
        
        # Καθαρισμός ονόματος
        clean_name = match_name.split("_")[0].replace("-vs-", " 🆚 ")
        match_date = match_name.split("_")[1].replace("_", " ") if "_" in match_name else ""

        st.info(f"🏆 **Διοργάνωση / Αγωνιστική:** Round {match_round}")
        st.markdown(f"### 🔥 {clean_name}")
        if match_date:
            st.write(f"📅 **Ημερομηνία:** {match_date}")
            
        st.success("💡 **Πρόβλεψη Μοντέλου:** Έτοιμη η στατιστική ανάλυση!")

    except Exception as e:
        # Αν το αρχείο δεν είναι σωστό JSON, δείξε απλά το κείμενο
        st.text_area(label="Δεδομένα", value=content, height=300)
else:
    st.warning("Δεν βρέθηκαν αποθηκευμένα δεδομένα αγώνων. Παρακαλώ εκτελέστε το main.py μέσω GitHub Actions.")
