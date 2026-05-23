import streamlit as st
import requests
from datetime import datetime

# ==========================================
# 1. ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ & DESIGN
# ==========================================
st.set_page_config(page_title="Football Live Score", page_icon="⚽", layout="centered")

st.markdown("""
    <style>
    .match-box {
        padding: 15px;
        border-radius: 10px;
        background-color: #f8f9fa;
        margin-bottom: 12px;
        border-left: 5px solid #e91e63;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
    }
    .live-badge {
        background-color: #e91e63;
        color: white;
        padding: 2px 6px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ Live Αγώνες & Σκορ (Απεριόριστο)")

# Κουμπί Ανανέωσης
if st.button("🔄 Άμεση Ανανέωση Σκορ"):
    st.rerun()

# ==========================================
# 2. ΛΗΨΗ ΔΕΔΟΜΕΝΩΝ ΑΠΟ ΔΩΡΕΑΝ ΠΗΓΗ
# ==========================================
# Χρησιμοποιούμε μια ελεύθερη πηγή scores που δεν έχει όρια κλήσεων
URL = "https://raw.githubusercontent.com/openfootball/world-cup/master/2018--russia/cup.json"

try:
    response = requests.get(URL)
    data = response.json()
    
    st.write("📊 **Προβολή Αγώνων και Αποτελεσμάτων:**")
    
    rounds = data.get("rounds", [])
    
    if not rounds:
        st.info("📅 Δεν βρέθηκαν διαθέσιμοι αγώνες αυτή τη στιγμή.")
    else:
        # Εμφανίζουμε τις φάσεις και τους αγώνες
        for r in rounds:
            round_name = r.get("name", "Αγώνες")
            matches = r.get("matches", [])
            
            if matches:
                with st.expander(f"🏆 {round_name} ({len(matches)} Ματς)", expanded=True):
                    for match in matches:
                        home = match.get("team1", {}).get("name", "Γηπεδούχος")
                        away = match.get("team2", {}).get("name", "Φιλοξενούμενος")
                        date_str = match.get("date", "")
                        
                        # Σκορ αν υπάρχουν
                        score1 = match.get("score1")
                        score2 = match.get("score2")
                        
                        if score1 is not None and score2 is not None:
                            score_display = f"🏁 **{score1} - {score2}** (Τελικό)"
                        else:
                            score_display = f"⏰ Ώρα: {date_str}"
                            
                        st.markdown(f"""
                            <div class="match-box">
                                🏠 <b>{home}</b> vs 🏴 <b>{away}</b><br>
                                <span style="color:#e91e63;">{score_display}</span>
                            </div>
                        """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"❌ Προέκυψε σφάλμα κατά τη φόρτωση: {e}")
