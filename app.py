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
            raw_home_form = parts[4]
            raw_away_form = parts[5]
            
            is_value = "VALUE BET" in prediction
            
            # --- ΕΞΥΠΝΟΣ ΔΙΑΧΩΡΙΣΜΟΣ ΗΜΙΧΡΟΝΟΥ & ΑΠΟΔΟΣΗΣ ---
            prediction_clean = prediction.replace("🔥 VALUE BET", "").strip()
            
            # Αν το ημίχρονο ξέμεινε κατά λάθος στη στήλη της φόρμας
            ht_tip = ""
            if "✨" in raw_home_form:
                form_parts = raw_home_form.split("✨")
                # Κρατάμε ό,τι περίσσεψε από την απόδοση
                extra_odd = form_parts[0].strip()
                if extra_odd and not extra_odd.startswith("🟢") and not extra_odd.startswith("🔴") and not extra_odd.startswith("🟡"):
                    prediction_clean += " " + extra_odd
                ht_tip = form_parts[1].strip()
                # Η πραγματική φόρμα είναι στην επόμενη στήλη
                home_form = raw_away_form
                away_form = "Δεν είναι διαθέσιμη" # Safe fallback
            elif "✨" in prediction_clean:
                pred_parts = prediction_clean.split("✨")
                prediction_clean = pred_parts[0].strip()
                ht_tip = pred_parts[1].strip()
                home_form = raw_home_form
                away_form = raw_away_form
            else:
                home_form = raw_home_form
                away_form = raw_away_form

            # Αν η φόρμα της μίας ομάδας περιέχει και τις δύο (παλιό string format)
            if "🟢" in home_form and "vs" in home_form:
                vs_parts = home_form.split("vs")
                home_form = vs_parts[0].strip()
                away_form = vs_parts[1].strip()

            with st.container(border=True):
                st.subheader(teams)
                st.caption(f"🏆 {league}  •  ⏰ Ώρα: {m_time}")
                
                if is_value:
                    st.markdown('<div class="value-box">🔥 VALUE BET IDENTIFIED</div>', unsafe_allow_html=True)
                
                # Κύριο Σημείο
                st.info(f"**Κύριο Σημείο:** {prediction_clean}")
                
                # Combo Ημίχρονο
                if ht_tip:
                    st.warning(f"**⚡ Combo Tip:** {ht_tip}")
                
                st.divider()
                
                # Εμφάνιση Φόρμας
                if "🟢" in home_form or "🔴" in home_form:
                    col_h, col_a = st.columns(2)
                    with col_h:
                        st.markdown(f"<span class='info-label'>🏠 Εντός:</span> {home_form}", unsafe_allow_html=True)
                    with col_a:
                        st.markdown(f"<span class='info-label'>🚀 Εκτός:</span> {away_form}", unsafe_allow_html=True)
else:
    st.info("🔄 Πατήστε 'Ανανέωση' για να φορτώσουν οι αγώνες.")
