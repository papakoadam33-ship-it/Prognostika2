import streamlit as st
import os

# Ρύθμιση σελίδας για κινητά
st.set_page_config(page_title="Marios Pro-Bet Pro", page_icon="⚡", layout="centered")

# Custom CSS για το Μαύρο-Χρυσό VIP Στυλ
st.markdown("""
    <style>
    body {
        background-color: #111216;
    }
    .main-title {
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        color: #FFFFFF;
        background: #1e1f24;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.5);
        margin-bottom: 20px;
    }
    .title-text {
        font-size: 28px;
        font-weight: 900;
        letter-spacing: 1px;
        margin: 0;
    }
    .subtitle-text {
        color: #f39c12;
        font-style: italic;
        font-size: 16px;
        margin-top: 10px;
    }
    .date-badge {
        text-align: center;
        background: #1e1f24;
        border: 2px solid #f39c12;
        padding: 10px;
        border-radius: 10px;
        color: #f39c12;
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 25px;
    }
    .match-card {
        background: #1a1b20;
        border: 2px solid #f39c12;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0px 4px 15px rgba(243, 156, 18, 0.15);
    }
    .league-header {
        color: #f39c12;
        font-size: 13px;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .teams-title {
        color: #FFFFFF;
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 15px;
    }
    .time-badge {
        background: #c0392b;
        color: white;
        padding: 3px 8px;
        border-radius: 5px;
        font-size: 12px;
        font-weight: bold;
        float: right;
    }
    .tip-box {
        background: #d4ac0d;
        color: #000000;
        font-weight: bold;
        text-align: center;
        padding: 12px;
        border-radius: 8px;
        font-size: 18px;
        margin-bottom: 10px;
    }
    .cover-box {
        background: #e67e22;
        color: #FFFFFF;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        border-radius: 8px;
        font-size: 15px;
    }
    .no-matches {
        background: #1e1f24;
        border-radius: 15px;
        padding: 40px;
        text-align: center;
        color: #FFFFFF;
    }
    .footer {
        text-align: center;
        color: #555555;
        font-size: 12px;
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ΕΦΑΡΜΟΓΗΣ ---
st.markdown("""
    <div class="main-title">
        <p class="title-text">⚡ MARIOS PRO-BET PRO ⚡</p>
        <p class="subtitle-text">Advanced Poisson & Hybrid Prediction Engine</p>
    </div>
""", unsafe_allow_html=True)

# --- ΑΝΑΓΝΩΣΗ ΔΕΔΟΜΕΝΩΝ ---
file_path = "daily_predictions.txt"

if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    if lines:
        header_parts = lines[0].strip().split("|")
        if header_parts[0] == "ΗΜΕΡΟΜΗΝΙΑ" and len(header_parts) >= 3:
            date_str = header_parts[1]
            time_str = header_parts[2]
            st.markdown(f'<div class="date-badge">📅 ΠΡΟΓΝΩΣΤΙΚΑ {date_str} | 🕒 Τελευταία Ενημέρωση: {time_str}</div>', unsafe_allow_html=True)
        
        match_lines = lines[1:]
        
        if len(match_lines) == 1 and "INFO" in match_lines[0]:
            st.markdown("""
                <div class="no-matches">
                    <span style="font-size: 50px;">⏰</span>
                    <h3 style="margin-top:15px; font-weight:bold;">Δεν υπάρχουν προγραμματισμένοι αγώνες για σήμερα.</h3>
                    <p style="color:#888888;">Το σύστημα ανανεώνει τις προβλέψεις αυτόματα.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            for line in match_lines:
                if not line.strip():
                    continue
                parts = line.strip().split("|")
                if len(parts) >= 5:
                    league = parts[0]
                    teams = parts[1]
                    m_time = parts[2]
                    main_tip = parts[3]
                    cover_tip = parts[4]
                    
                    st.markdown(f"""
                        <div class="match-card">
                            <span class="time-badge">🕒 {m_time}</span>
                            <div class="league-header">🏆 {league} [VIP]</div>
                            <div class="teams-title">{teams}</div>
                            <div class="tip-box">👑 {main_tip}</div>
                            <div class="cover-box">🛡️ {cover_tip}</div>
                        </div>
                    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <div class="no-matches">
            <span style="font-size: 50px;">⏳</span>
            <h3 style="margin-top:15px; font-weight:bold;">Αναμονή για την πρώτη αυτόματη δημιουργία...</h3>
            <p style="color:#888888;">Το αρχείο προγνωστικών δεν έχει δημιουργηθεί ακόμα στο GitHub.</p>
        </div>
    """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown('<div class="footer">Powered by Python & API-Football (Marios Pro-Bet Engine)</div>', unsafe_allow_html=True)

