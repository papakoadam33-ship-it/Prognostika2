import streamlit as st
import os

# ==========================================
# 1. ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ & DESIGN
# ==========================================
st.set_page_config(page_title="Football Predictions", page_icon="⚽", layout="centered")

st.markdown("""
    <style>
    .match-box {
        padding: 15px;
        border-radius: 8px;
        background-color: #f1f5f9;
        margin-bottom: 12px;
        border-left: 6px solid #2563eb;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
    }
    .odds-container {
        display: flex;
        justify-content: space-between;
        background: #ffffff;
        padding: 8px;
        border-radius: 5px;
        margin-top: 5px;
        border: 1px solid #e2e8f0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ Live Αγώνες & Προγνωστικά")

# ==========================================
# 2. ΑΜΕΣΟ ΔΙΑΒΑΣΜΑ ΑΡΧΕΙΟΥ (ΧΩΡΙΣ ΚΑΘΥΣΤΕΡΗΣΗ)
# ==========================================
FILE_NAME = "daily_predictions.txt"

if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    st.write("📊 **Οι σημερινές αυτόματες προτάσεις:**")
    
    for line in lines:
        if line.strip() and "|" in line:
            parts = line.split("|")
            match_time = parts[0].strip()
            match_teams = parts[1].strip()
            match_odds = parts[2].strip()
            match_tip = parts[3].strip()
            
            st.markdown(f"""
                <div class="match-box">
                    ⏰ <b>{match_time}</b> | 🏆 <b>{match_teams}</b>
                    <div class="odds-container">
                        <span>📈 Σετ: {match_odds}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            with st.expander("💡 Δείτε το Προγνωστικό / Tip"):
                st.success(f"🎯 {match_tip}")
else:
    st.info("🔄 Οι αγώνες προετοιμάζονται αυτόματα, δοκιμάστε μια ανανέωση σε ένα λεπτό!")

