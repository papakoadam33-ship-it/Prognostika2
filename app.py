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
        background-color: rgba(245, 158, 11, 0.15);
        border-left: 5px solid #f59e0b;
        padding: 12px;
        border-radius: 6px;
        font-weight: bold;
        margin-top: 5px;
        margin-bottom: 10px;
        color: #fff;
    }
    .custom-pred-box {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-left: 5px solid #06b6d4; /* Premium Γαλάζιο/Cyan Περίγραμμα */
        padding: 15px;
        border-radius: 6px;
        margin-top: 5px;
        margin-bottom: 10px;
        color: #fff;
    }
    .info-label {
        font-weight: bold;
        color: #94a3b8;
    }
    </style>
    """, unsafe_allow_html=True)

DATA_FILE = "daily_predictions.txt"

# Κουμπί Ανανέωσης στην κορυφή όπως παλιά
if st.button("🔄 Ανανέωση"):
    st.rerun()

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

    has_any_value = any("VALUE BET" in line for line in lines[1:])
    match_count = 0

    for line in lines[1:]:
        if line.startswith("🏆"):
            parts = line.strip().split("|")
            if len(parts) < 6: continue
            
            league = parts[0].replace("🏆 ", "")
            teams = parts[1]
            m_time = parts[2]
            prediction = parts[3]
            raw_home_form = parts[4].strip()
            raw_away_form = parts[5].strip()
            
            match_count += 1
            is_value = "VALUE BET" in prediction or (not has_any_value and match_count == 1)
            
            prediction_clean = prediction.replace("🔥 VALUE BET", "").strip()
            ht_tip = ""
            
            if "✨" in raw_home_form:
                form_parts = raw_home_form.split("✨")
                extra_odd = form_parts[0].strip()
                if extra_odd and not any(c in extra_odd for c in ["🟢", "🔴", "🟡"]):
                    prediction_clean += " " + extra_odd
                ht_tip = form_parts[1].strip()
                combined_forms = raw_away_form
            elif "✨" in prediction_clean:
                pred_parts = prediction_clean.split("✨")
                prediction_clean = pred_parts[0].strip()
                ht_tip = pred_parts[1].strip()
                combined_forms = raw_home_form
            else:
                combined_forms = raw_home_form

            combined_forms = combined_forms.replace("vs", "").replace(" ", "")
            all_emojis = [char for char in combined_forms if char in ["🟢", "🔴", "🟡"]]
            
            if len(all_emojis) >= 10:
                home_form = "".join(all_emojis[:5])
                away_form = "".join(all_emojis[5:10])
            elif len(all_emojis) == 5:
                home_form = "".join(all_emojis)
                away_form = "🟡🟡🟡🟡🟡"
            else:
                home_form = "🟡🟡🟡🟡🟡"
                away_form = "🟡🟡🟡🟡🟡"

            with st.container(border=True):
                st.subheader(teams)
                st.caption(f"🏆 {league}  •  ⏰ Ώρα: {m_time}")
                
                if is_value:
                    st.markdown('<div class="value-box">🔥 VALUE BET IDENTIFIED</div>', unsafe_allow_html=True)
                
                # Νέο custom πλαίσιο αντί για το κλασικό μπλε st.info
                st.markdown(f"""
                    <div class="custom-pred-box">
                        <strong>Κύριο Σημείο:</strong> {prediction_clean}
                    </div>
                """, unsafe_allow_html=True)
                
                if ht_tip:
                    st.warning(f"**⚡ Combo Tip:** {ht_tip}")
                
                st.divider()
                
                col_h, col_a = st.columns(2)
                with col_h:
                    st.markdown(f"<span class='info-label'>🏠 Εντός:</span> {home_form}", unsafe_allow_html=True)
                with col_a:
                    st.markdown(f"<span class='info-label'>🚀 Εκτός:</span> {away_form}", unsafe_allow_html=True)
else:
    st.info("🔄 Πατήστε 'Ανανέωση' για να φορτώσουν οι αγώνες.")
