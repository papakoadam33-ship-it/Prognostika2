import os
import streamlit as st

st.set_page_config(
    page_title="MARIOS PRO-BET PRO", 
    page_icon="⚡", 
    layout="centered"
)

# Custom CSS για Premium Dark UI & Badges
st.markdown("""
    <style>
    .stApp {
        background-color: #020617;
        color: #f8fafc;
    }
    .value-badge {
        background-color: rgba(245, 158, 11, 0.2);
        border: 1px solid #f59e0b;
        color: #fbbf24;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 10px;
    }
    .pred-card {
        background-color: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 15px;
    }
    .tip-tag {
        background-color: #1e293b;
        color: #38bdf8;
        padding: 4px 10px;
        border-radius: 6px;
        font-weight: bold;
        font-size: 0.95rem;
    }
    .ht-tag {
        color: #f43f5e;
        font-weight: bold;
        font-size: 0.85rem;
    }
    </style>
    """, unsafe_allow_html=True)

DATA_FILE = "daily_predictions.txt"

# ⚡ Caching για ακαριαία ταχύτητα
@st.cache_data(ttl=300)
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return []

# Header με τίτλο και κουμπί Ανανέωσης
col_title, col_btn = st.columns([3, 1])
with col_title:
    st.title("⚡ MARIOS PRO-BET")
with col_btn:
    st.write("")
    if st.button("🔄 Ανανέωση"):
        st.cache_data.clear()
        st.rerun()

lines = load_data()

if lines:
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
            
            if "VALUE BET" in parts[3]:
                has_any_value = True
                
            all_matches.append(parts)

    only_value = st.toggle("🔥 Προβολή μόνο Value Bets")

    # Ταξινόμηση ανά Πρωτάθλημα
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
            # Όνομα Αγώνα & Στοιχεία
            st.subheader(teams)
            st.caption(f"🏆 {league}  •  ⏰ Ώρα: {m_time}")
            
            # Badge αν είναι Value Bet
            if is_value:
                st.markdown('<div class="value-badge">🔥 VALUE BET IDENTIFIED</div>', unsafe_allow_html=True)
            
            # Κύριο Σημείο
            st.markdown(f"**🎯 Κύριο Σημείο:** <span class='tip-tag'>{prediction_clean}</span>", unsafe_allow_html=True)
            
            # Combo / 1o Ημίχρονο Tip
            if ht_tip:
                st.write("")
                st.markdown(f"**⚡ Combo Tip:** <span class='ht-tag'>{ht_tip}</span>", unsafe_allow_html=True)

    if displayed_matches == 0:
        st.info("ℹ️ Δεν βρέθηκαν αγώνες με τα επιλεγμένα φίλτρα.")

    # Πρόσφατα Αποτελέσματα
    if past_results:
        st.write("")
        with st.expander("📜 Πρόσφατα Αποτελέσματα"):
            for res in past_results:
                st.write(res)

else:
    st.info("🔄 Πατήστε 'Ανανέωση' για να φορτώσουν οι αγώνες.")

