import streamlit as st
import os

# Αρχική ρύθμιση σελίδας
st.set_page_config(page_title="VIP Προγνωστικά", page_icon="⚽", layout="centered")

# Custom CSS για τέλεια εμφάνιση που προσαρμόζεται στο Light/Dark Mode
st.markdown("""
    <style>
    .sub-header-text {
        text-align: center;
        font-size: 16px;
        color: #6B7280;
        margin-bottom: 25px;
    }
    .match-row {
        font-size: 18px;
        font-weight: 600;
        padding: 5px 0px;
    }
    .prediction-box-bookie {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 12px;
        border-radius: 8px;
        border-left: 5px solid #EF4444;
        font-weight: bold;
        margin-top: 5px;
        margin-bottom: 15px;
    }
    .prediction-box-stat {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 12px;
        border-radius: 8px;
        border-left: 5px solid #F59E0B;
        font-weight: bold;
        margin-top: 5px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Τίτλοι με τη σωστή μέθοδο του Streamlit για να μην κρύβονται
st.title("⚽ VIP Προγνωστικά")
st.markdown('<div class="sub-header-text">🎯 Live ανανέωση βάσει αποδόσεων & στατιστικής</div>', unsafe_allow_html=True)

filename = "daily_predictions.txt"

if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
    
    blocks = content.split("---------------------------------------------")
    
    # Εμφάνιση ώρας τελευταίας ενημέρωσης
    if blocks:
        header_lines = blocks[0].strip().split("\n")
        for line in header_lines:
            if "Τελευταία ενημέρωση:" in line:
                st.caption(f"🕒 {line}")

    # Ομαδοποίηση ανά πρωτάθλημα
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

    # Σχεδίαση των αγώνων στην οθόνη
    if leagues_dict:
        for league_name, matches in leagues_dict.items():
            with st.expander(f"🏆 {league_name} ({len(matches)})", expanded=True):
                for m in matches:
                    # Δημιουργούμε 2 στήλες: Μία μικρή για την ώρα, μία μεγάλη για τις ομάδες
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.markdown(f"⏱️ **{m['time']}**")
                    with col2:
                        st.markdown(f'<div class="match-row">{m["teams"]}</div>', unsafe_allow_html=True)
                    
                    # Έξυπνα custom πλαίσια ανάλογα με τον τύπο της πρόβλεψης
                    if "🔥 [Bookmaker]" in m['prediction']:
                        clean_pred = m['prediction'].replace("🔥 [Bookmaker]", "").strip()
                        st.markdown(f'<div class="prediction-box-bookie">🔥 VIP Επιλογή: {clean_pred}</div>', unsafe_allow_html=True)
                    else:
                        clean_pred = m['prediction'].replace("📊 [Στατιστικό]", "").strip()
                        st.markdown(f'<div class="prediction-box-stat">📊 Στατιστικό: {clean_pred}</div>', unsafe_allow_html=True)
                    
                    st.markdown('<hr style="margin:10px 0px; border-top: 1px navajowhite;" />', unsafe_allow_html=True)
    else:
        st.info("ℹ️ Δεν υπάρχουν διαθέσιμοι αγώνες αυτή τη στιγμή.")
else:
    st.warning("⏳ Τα προγνωστικά δημιουργούνται αυτή τη στιγμή. Παρακαλώ ανανεώστε σε 1 λεπτό!")

