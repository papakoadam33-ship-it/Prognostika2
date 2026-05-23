import streamlit as st
import os

st.set_page_config(page_title="Live Αγώνες & Προγνωστικά", page_icon="⚽", layout="centered")

st.title("⚽ Live Αγώνες & Προγνωστικά")
st.subheader("📊 Οι σημερινές αυτόματες προτάσεις:")

filename = "daily_predictions.txt"

if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
    
    blocks = content.split("---------------------------------------------")
    
    if blocks:
        header = blocks[0].strip().split("\n\n")[0]
        st.info(header)
        
    for block in blocks:
        lines = block.strip().split("\n")
        
        league = ""
        match_time = ""
        match_teams = ""
        prediction = ""
        
        for line in lines:
            if line.startswith("Πρωτάθλημα:"):
                league = line.replace("Πρωτάθλημα:", "").strip()
            elif line.startswith("Ώρα:"):
                match_time = line.replace("Ώρα:", "").strip()
            elif line.startswith("Αγώνας:"):
                match_teams = line.replace("Αγώνας:", "").strip()
            elif line.startswith("🎯 Πρόβλεψη:"):
                prediction = line.replace("🎯 Πρόβλεψη:", "").strip()
        
        if match_teams and prediction:
            with st.container():
                time_badge = f" ⏱️ {match_time}" if match_time else ""
                st.markdown(f"**🏆 {league}** {time_badge}")
                st.code(match_teams, language="text")
                st.success(f"🔮 Προγνωστικό: {prediction}")
                st.write("---")
else:
    st.warning("⏳ Τα προγνωστικά δημιουργούνται αυτή τη στιγμή. Παρακαλώ ανανεώστε σε 1 λεπτό!")
