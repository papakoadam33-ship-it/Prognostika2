import streamlit as st
import os

st.set_page_config(page_title="MARIOS PRO-BET PRO", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #020617;
        color: #f8fafc;
    }
    
    .main-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border-radius: 15px;
        border: 1px solid #334155;
        margin-bottom: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    .main-header h1 {
        color: #fff;
        font-family: 'Urbanist', sans-serif;
        font-weight: 700;
        letter-spacing: 2px;
        margin: 0;
    }
    
    .stats-container {
        display: flex;
        justify-content: space-around;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid #10b981;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 25px;
    }
    
    .stat-item { text-align: center; }
    .stat-value { font-size: 24px; font-weight: 700; color: #10b981; }
    .stat-label { font-size: 12px; color: #94a3b8; text-transform: uppercase; }

    .match-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 15px;
    }
    
    .league-tag { color: #f59e0b; font-size: 12px; font-weight: 700; margin-bottom: 5px; }
    .teams { font-size: 18px; font-weight: 700; color: #fff; margin-bottom: 10px; }
    
    .value-bet-alert {
        background: linear-gradient(90deg, rgba(245, 158, 11, 0.2) 0%, rgba(245, 158, 11, 0.05) 100%);
        border-left: 5px solid #f59e0b;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        font-weight: 700;
        color: #fff;
    }

    .pred-box { background: #1e293b; padding: 10px; border-radius: 8px; margin-top: 10px; font-size: 14px; }
    .form-dots { font-size: 16px; margin-top: 5px; }
    </style>
    """, unsafe_allow_html=True)

DATA_FILE = "daily_predictions.txt"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    st.markdown('<div class="main-header"><h1>⚡ MARIOS PRO-BET PRO</h1></div>', unsafe_allow_html=True)
    
    if lines and lines[0].startswith("STATS"):
        _, wr, yld = lines[0].strip().split("|")
        st.markdown(f"""
            <div class="stats-container">
                <div class="stat-item"><div class="stat-value">{wr}%</div><div class="stat-label">Win Rate</div></div>
                <div class="stat-item"><div class="stat-value">+{yld}%</div><div class="stat-label">Total Yield</div></div>
            </div>
        """, unsafe_allow_html=True)

    for line in lines[1:]:
        if line.startswith("🏆"):
            parts = line.strip().split("|")
            league = parts[0].replace("🏆 ", "")
            teams = parts[1]
            m_time = parts[2]
            prediction = parts[3]
            h_form = parts[4]
            a_form = parts[5]
            
            is_value = "VALUE BET" in prediction
            prediction_clean = prediction.replace("🔥 VALUE BET", "").strip()

            with st.container():
                st.markdown(f"""
                    <div class="match-card">
                        <div class="league-tag">{league} • {m_time}</div>
                        <div class="teams">{teams}</div>
                        {"<div class='value-bet-alert'>🔥 VALUE BET IDENTIFIED</div>" if is_value else ""}
                        <div class="pred-box">{prediction_clean}</div>
                        <div class="form-dots">Φόρμα: {h_form} vs {a_form}</div>
                    </div>
                """, unsafe_allow_html=True)
else:
    st.info("🔄 Πατήστε 'Ανανέωση' για να φορτώσουν οι αγώνες.")
