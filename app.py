import streamlit as st
import os

# Ρύθμιση σελίδας
st.set_page_config(page_title="VIP Προγνωστικά", page_icon="⚽", layout="centered")

# Custom CSS για να κάνουμε την εμφάνιση ακόμα πιο μοντέρνα
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #FFFFFF;
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .subtitle {
        text-align: center;
        color: #A0AEC0;
        font-size: 18px;
        margin-bottom: 30px;
    }
    .match-box {
        background-color: #1E293B;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 5px solid #3B82F6;
    }
    .time-text {
        color: #F59E0B;
        font-weight: bold;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚽ VIP Προγνωστικά Ποδοσφαίρου</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">🎯 Live ανανέωση βάσει αποδόσεων & στατιστικής</div>', unsafe_allow_html=True)

filename = "daily_predictions.txt"

if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
    
    blocks = content.split("---------------------------------------------")
    
    # Διαβάζουμε την κεφαλίδα (ώρα τελευταίας ενημέρωσης)
    if blocks:
        header_lines = blocks[0].strip().split("\n")
        for line in header_lines:
            if "Δεν βρέθηκαν" in line:
                st.warning(line)
            elif "Τελευταία ενημέρωση:" in line:
                st.caption(f"🕒 {line}")

    # Ομαδοποίηση αγώνων ανά πρωτάθλημα για να μην είναι χαοτικό
    leagues_dict = {}
    
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
        
        if league and match_teams and prediction:
            if league not in leagues_dict:
                leagues_dict[league] = []
            leagues_dict[league].append({
                "time": match_time,
                "teams": match_teams,
                "prediction": prediction
            })

    # Εμφάνιση των αγώνων οργανωμένα
    if leagues_dict:
        for league_name, matches in leagues_dict.items():
            # Δημιουργία πτυσσόμενου μενού (Expander) για κάθε πρωτάθλημα
            with st.expander(f"🏆 {league_name} ({len(matches)} αγώνες)", expanded=True):
                for m in matches:
                    # Εμφάνιση ομάδων και ώρας
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.markdown(f"⏱️ **{m['time']}**")
                    with col2:
                        st.markdown(f"**{m['teams']}**")
                    
                    # Εμφάνιση πρόβλεψης με βάση την κατηγορία (Bookie ή Στατιστικό)
                    if "🔥 [Bookmaker]" in m['prediction']:
                        clean_pred = m['prediction'].replace("🔥 [Bookmaker]", "").strip()
                        st.error(f"🔥 **VIP Επιλογή (Bookie):** {clean_pred}")
                    else:
                        clean_pred = m['prediction'].replace("📊 [Στατιστικό]", "").strip()
                        st.warning(f"📊 **Στατιστικό Σημείο:** {clean_pred}")
                    
                    st.write("") # Μικρό κενό ανάμεσα στα ματς
    else:
        st.info("ℹ️ Δεν υπάρχουν διαθέσιμοι αγώνες αυτή τη στιγμή.")
else:
    st.warning("⏳ Τα προγνωστικά δημιουργούνται αυτή τη στιγμή. Παρακαλώ ανανεώστε σε 1 λεπτό!")

