import streamlit as st
import os

# Ρύθμιση σελίδας
st.set_page_config(page_title="Marios Pro-Bet Pro", page_icon="⚡", layout="centered")

# Custom CSS για πανέμορφο design (Σκούρο Θέμα & Χρυσά Blocks)
st.markdown("""
    <style>
    .main { background-color: #121212; }
    .header-box {
        background: linear-gradient(135deg, #1e1e1e 0%, #2a2a2a 100%);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
        border: 1px solid #333;
        margin-bottom: 25px;
    }
    .header-title { color: #ffffff; font-size: 26px; font-weight: bold; margin-bottom: 5px; }
    .header-subtitle { color: #ffb300; font-size: 16px; font-style: italic; }
    .date-bar {
        background-color: #ff9800;
        color: #000000;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 20px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.3);
    }
    .match-card {
        background: linear-gradient(135deg, #1f1f1f 0%, #2d2d2d 100%);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
        border-left: 6px solid #ffb300;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.4);
    }
    .league-title { color: #ff9800; font-size: 14px; font-weight: bold; text-transform: uppercase; }
    .teams-title { color: #ffffff; font-size: 18px; font-weight: bold; margin: 5px 0; }
    .time-text { color: #aaaaaa; font-size: 13px; }
    .tip-box {
        background-color: #2e7d32;
        color: #ffffff;
        padding: 8px 12px;
        border-radius: 8px;
        font-weight: bold;
        display: inline-block;
        margin-top: 10px;
        font-size: 14px;
    }
    .cover-box {
        background-color: #1565c0;
        color: #ffffff;
        padding: 8px 12px;
        border-radius: 8px;
        font-weight: bold;
        display: inline-block;
        margin-top: 10px;
        margin-left: 10px;
        font-size: 14px;
    }
    .no-matches {
        background-color: #1e1e1e;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        border: 1px solid #333;
    }
    </style>
""", unsafe_allow_html=True)

# 1. Τίτλος Εφαρμογής
st.markdown("""
    <div class="header-box">
        <div class="header-title">⚡ MARIOS PRO-BET PRO ⚡</div>
        <div class="header-subtitle">Advanced Poisson & Hybrid Prediction Engine</div>
    </div>
""", unsafe_allow_html=True)

file_path = "daily_predictions.txt"

if os.path.exists(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    if lines:
        # Διάβασμα της πρώτης γραμμής (Ημερομηνία)
        first_line = lines[0].split("|")
        if first_line[0] == "ΗΜΕΡΟΜΗΝΙΑ" and len(first_line) >= 3:
            st.markdown(f'<div class="date-bar">📅 ΠΡΟΓΝΩΣΤΙΚΑ {first_line[1]} | 🕒 Τελευταία Ενημέρωση: {first_line[2]}</div>', unsafe_allow_html=True)
            match_lines = lines[1:]
        else:
            st.markdown('<div class="date-bar">📅 ΠΡΟΓΝΩΣΤΙΚΑ ΣΗΜΕΡΑ</div>', unsafe_allow_html=True)
            match_lines = lines

        # Έλεγχος αν υπάρχουν αγώνες ή αν έχει γραφτεί INFO μήνυμα
        if match_lines and "INFO" in match_lines[0]:
            st.markdown("""
                <div class="no-matches">
                    <img src="https://fonts.gstatic.com/s/e/notoemoji/latest/1f440/512.webp" width="60" style="margin-bottom:15px;">
                    <h3 style="color:white; margin-bottom:10px;">Δεν υπάρχουν προγραμματισμένοι αγώνες.</h3>
                    <p style="color:#888;">Το σύστημα ελέγχει αυτόματα για νέα μεγάλα πρωταθλήματα.</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Εμφάνιση των αγώνων σε κάρτες
            for line in match_lines:
                parts = line.split("|")
                if len(parts) >= 5:
                    league, teams, match_time, main_tip, cover_tip = parts[0], parts[1], parts[2], parts[3], parts[4]
                    
                    st.markdown(f"""
                        <div class="match-card">
                            <div class="league-title">{league}</div>
                            <div class="teams-title">⚽ {teams}</div>
                            <div class="time-text">🕒 Ώρα Έναρξης: {match_time}</div>
                            <div>
                                <div class="tip-box">🎯 {main_tip}</div>
                                <div class="cover-box">🛡️ {cover_tip}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("Το αρχείο προβλέψεων είναι άδειο.")
else:
    # Εμφάνιση κλεψύδρας αν δεν υπάρχει το αρχείο ακόμα
    st.markdown("""
        <div class="no-matches">
            <h1 style="font-size:60px; margin:0;">⏳</h1>
            <h2 style="color: white; margin-top:20px;">Αναμονή για την πρώτη αυτόματη δημιουργία...</h2>
            <p style="color: #888; margin-top:10px;">Το αρχείο προγνωστικών δεν έχει ενημερωθεί ακόμα στο GitHub Actions.</p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<br><hr><center style='color:#666; font-size:12px;'>Powered by Python & API-Football (Marios Pro-Bet Engine)</center>", unsafe_allow_html=True)
