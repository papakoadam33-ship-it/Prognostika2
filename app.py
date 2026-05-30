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
    .info-label {
        font-weight: bold;
        color: #94a3b8;
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
            
            # Καθαρισμός κύριου σημείου και εξαγωγή του Ημιχρόνου (αν υπάρχει)
            prediction_clean = prediction.replace("🔥 VALUE BET", "").strip()
            ht_tip = ""
            if "✨" in prediction_clean:
                pred_parts = prediction_clean.split("✨")
                prediction_main = pred_parts[0].strip()
                ht_tip = pred_parts[1].strip()
            else:
                prediction_main = prediction_clean

            with st.container(border=True):
                st.subheader(teams)
                st.caption(f"🏆 {league}  •  ⏰ Ώρα: {m_time}")
                
                if is_value:
                    st.markdown('<div class="value-box">🔥 VALUE BET IDENTIFIED</div>', unsafe_allow_html=True)
                
                # Κύριο Σημείο (π.χ. Under 2.5 / Over 2.5)
                st.info(f"**Κύριο Σημείο:** {prediction_main}")
                
                # Ειδικό Στόχημα Ημιχρόνου (Αν υπάρχει)
                if ht_tip:
                    st.warning(f"**⚡ Combo Tip:** {ht_tip}")
                
                st.divider()
                
                # Καθαρή εμφάνιση Φόρμας χωρίς παρεμβολές
                col_h, col_a = st.columns(2)
                with col_h:
                    st.markdown(f"<span class='info-label'>🏠 Εντός:</span> {h_form}", unsafe_allow_html=True)
                with col_a:
                    st.markdown(f"<span class='info-label'>🚀 Εκτός:</span> {a_form}", unsafe_allow_html=True)
else:
    st.info("🔄 Πατήστε 'Ανανέωση' για να φορτώσουν οι αγώνες.")
