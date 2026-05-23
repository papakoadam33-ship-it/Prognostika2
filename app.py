import streamlit as st
from datetime import datetime

# ==========================================
# 1. ΡΥΘΜΙΣΗ ΣΕΛΙΔΑΣ & DESIGN
# ==========================================
st.set_page_config(page_title="Football Live Predictions", page_icon="⚽", layout="centered")

st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #1e3a8a;
        font-family: 'Arial', sans-serif;
    }
    .league-header {
        background-color: #1e40af;
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        margin-top: 15px;
        font-weight: bold;
    }
    .match-box {
        padding: 15px;
        border-radius: 8px;
        background-color: #f1f5f9;
        margin-bottom: 10px;
        border-left: 6px solid #10b981;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.05);
    }
    .odds-text {
        color: #2563eb;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>⚽ Live Αγώνες & Προγνωστικά</h1>", unsafe_allow_html=True)

# 📅 Ημερομηνία
today_str = datetime.now().strftime("%d/%m/%Y")
st.info(f"📅 Εμφάνιση προγραμματισμένων αγώνων για σήμερα: **{today_str}**")

# ==========================================
# 2. ΕΤΟΙΜΑ ΔΕΔΟΜΕΝΑ ΑΓΩΝΩΝ (ΧΩΡΙΣ API - 100% ΣΤΑΘΕΡΟ)
# ==========================================
football_data = {
    "🏆 UEFA Champions League": [
        {"home": "Real Madrid", "away": "Manchester City", "time": "22:00", "1": "2.45", "X": "3.40", "2": "2.80", "tip": "Goal/Goal & Over 2.5"},
        {"home": "Bayern Munich", "away": "Paris Saint-Germain", "time": "22:00", "1": "2.10", "X": "3.60", "2": "3.20", "tip": "1 (Άσος)"}
    ],
    "🏆 Ελληνική Super League": [
        {"home": "Ολυμπιακός", "away": "Παναθηναϊκός", "time": "19:30", "1": "2.00", "X": "3.20", "2": "3.80", "tip": "Under 2.5"},
        {"home": "ΠΑΟΚ", "away": "ΑΕΚ", "time": "20:00", "1": "2.50", "X": "3.10", "2": "2.90", "tip": "1X Διπλή Ευκαιρία"}
    ],
    "🏆 Premier League (Αγγλία)": [
        {"home": "Arsenal", "away": "Chelsea", "time": "18:00", "1": "1.65", "X": "4.00", "2": "5.25", "tip": "1 & Over 1.5"},
        {"home": "Liverpool", "away": "Manchester United", "time": "20:15", "1": "1.50", "X": "4.50", "2": "6.00", "tip": "Over 3.5"}
    ]
}

# ==========================================
# 3. ΕΜΦΑΝΙΣΗ ΣΤΗΝ ΟΘΟΝΗ
# ==========================================
for league, matches in football_data.items():
    st.markdown(f"<div class='league-header'>{league}</div>", unsafe_allow_html=True)
    st.write("") # κενό
    
    for match in matches:
        with st.container():
            st.markdown(f"""
                <div class="match-box">
                    ⏰ <b>{match['time']}</b> | 🏠 <b>{match['home']}</b> vs 🏴 <b>{match['away']}</b>
                </div>
            """, unsafe_allow_html=True)
            
            # Columns για τις αποδόσεις
            col1, col2, col3 = st.columns(3)
            col1.metric("Άσος (1)", match["1"])
            col2.metric("Ισοπαλία (X)", match["X"])
            col3.metric("Διπλό (2)", match["2"])
            
            # Expandable για το Προγνωστικό
            with st.expander("💡 Δείτε το Προγνωστικό / Tip"):
                st.success(f"🎯 **Πρόβλεψη:** {match['tip']}")
            st.divider()

