import os
import streamlit as st

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
        border-left: 5px solid #06b6d4;
        padding: 15px;
        border-radius: 6px;
        margin-top: 5px;
        margin-bottom: 10px;
        color: #fff;
    }
    </style>
    """, unsafe_allow_html=True)

DATA_FILE = "daily_predictions.txt"

col_title, col_btn = st.columns([3, 1])
with col_title:
    st.title("⚡ MARIOS PRO-BET PRO")
with col_btn:
    st.write("")
    if st.button("🔄 Ανανέωση"):
        st.rerun()

if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    all_matches = []
    past_results = []
    has_any_value = False
    is_results_section = False

    for line in lines:
        if line.startswith("STATS"):
            continue

        elif "--- ΠΡΟΣΦΑΤΑ ΑΠΟΤΕΛΕΣΜΑΤΑ" in line:
            is_results_section = True
            continue

        elif is_results_section:
            past_results.append(line)

        elif line.startswith("🏆"):
            parts = line.split("|")
            if len(parts) < 4: continue
            
            prediction = parts[3]
            if "VALUE BET" in prediction:
                has_any_value = True
                
            all_matches.append(parts)

    only_value = st.toggle("🔥 Προβολή μόνο Value Bets")

    all_matches.sort(key=lambda x: x[0])

    match_count = 0
    displayed_matches = 0

    for parts in all_matches:
        league = parts[0].replace("🏆 ", "")
        teams = parts[1]
        m_time = parts[2]
        prediction = parts[3]
        
        match_count += 1
        is_value = "VALUE BET" in prediction or (not has_any_value and match_count == 1)
        
        if only_value and not is_value:
            continue

        displayed_matches += 1
        prediction_clean = prediction.replace("🔥 VALUE BET IDENTIFIED", "").replace("🔥 VALUE BET", "").strip()
        ht_tip = ""
        
        if "✨" in prediction_clean:
            pred_parts = prediction_clean.split("✨")
            prediction_clean = pred_parts[0].strip()
            ht_tip = pred_parts[1].strip()

        with st.container(border=True):
            st.subheader(teams)
            st.caption(f"🏆 {league}  •  ⏰ Ώρα: {m_time}")
            
            if is_value:
                st.markdown('<div class="value-box">🔥 VALUE BET IDENTIFIED</div>', unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="custom-pred-box">
                    <strong>Κύριο Σημείο:</strong> {prediction_clean}
                </div>
            """, unsafe_allow_html=True)
            
            if ht_tip:
                st.warning(f"**⚡ Combo Tip:** {ht_tip}")

    if displayed_matches == 0:
        st.info("ℹ️ Δεν βρέθηκαν αγώνες με τα επιλεγμένα φίλτρα.")

    if past_results:
        st.write("")
        with st.expander("📜 Πρόσφατα Αποτελέσματα"):
            for res in past_results:
                st.write(res)

else:
    st.info("🔄 Πατήστε 'Ανανέωση' για να φορτώσουν οι αγώνες.")

