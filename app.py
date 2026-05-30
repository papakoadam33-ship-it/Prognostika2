import streamlit as st
import os

st.set_page_config(page_title="MARIOS PRO-BET PRO", layout="centered")

st.markdown("""
    <style>
    .stApp {
        background-color: #020617;
        color: #f8fafc;
    }
    .value-box {
        background-color: rgba(245, 158, 11, 0.2);
        border-left: 5px solid #f59e0b;
        padding: 10px;
        border-radius: 5px;
        font-weight: bold;
        margin-top: 5px;
        margin-bottom: 5px;
        color: #fff;
    }
    </style>
    """, unsafe_allow_html=True)

DATA_FILE = "daily_predictions.txt"

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    st.title("⚡ MARIOS PRO-BET PRO")
    
    if lines and lines[0].startswith("STATS"):
        _, wr, yld = lines[0].strip().split("|")
        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="📊 WIN RATE", value=f"{wr}%")
        with col2:
            st.metric(label="💰 TOTAL YIELD", value=f"+{yld}%")
    
    st.divider()

    for line in lines[1:]:
        if line.startswith("🏆"):
            parts = line.strip().split("|")
            if len(parts) < 6: continue
            
            league = parts[0].replace("🏆 ", "")
            teams = parts[1]
            m_time = parts[2]
            prediction = parts[3]
            h_form = parts[4]
            a_form = parts[5]
            
            is_value = "VALUE BET" in prediction
            prediction_clean = prediction.replace("🔥 VALUE BET", "").strip()

            with st.container(border=True):
                st.subheader(teams)
                st.caption(f"🏆 {league}  •  ⏰ Ώρα: {m_time}")
                
                if is_value:
                    st.markdown('<div class="value-box">🔥 VALUE BET IDENTIFIED</div>', unsafe_allow_html=True)
                
                st.info(prediction_clean)
                
                # Καθαρός διαχωρισμός φόρμας
                st.markdown(f"**📈 Φόρμα Ομάδων:** {h_form}  vs  {a_form}")
else:
    st.info("🔄 Πατήστε 'Ανανέωση' για να φορτώσουν οι αγώνες.")
