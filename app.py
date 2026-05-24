import streamlit as st
import os

# Αρχική ρύθμιση σελίδας
st.set_page_config(page_title="VIP Προγνωστικά", page_icon="⚽", layout="centered")

# --- ΤΟ ΠΛΗΡΕΣ ΛΕΞΙΚΟ ΜΕΤΑΦΡΑΣΕΩΝ ---
LEAGUE_TRANSLATIONS = {
    # Αγγλία
    "Premier League": "Πρωτάθλημα Αγγλίας (Premier League)",
    "Championship": "Αγγλία - Championship (Β')",
    "League 1": "Αγγλία - League One (Γ')",
    "League 2": "Αγγλία - League Two (Δ')",
    
    # Ισπανία
    "La Liga": "Πρωτάθλημα Ισπανίας (La Liga)",
    "La Liga 2": "Ισπανία - Segunda Division (Β')",
    
    # Ιταλία
    "Serie A": "Πρωτάθλημα Ιταλίας (Serie A)",
    "Serie B": "Ιταλία - Serie B (Β')",
    
    # Γερμανία
    "Bundesliga": "Πρωτάθλημα Γερμανίας (Bundesliga)",
    "2. Bundesliga": "Γερμανία - 2. Bundesliga (Β')",
    
    # Γαλλία
    "Ligue 1": "Πρωτάθλημα Γαλλίας (Ligue 1)",
    "Ligue 2": "Γαλλία - Ligue 2 (Β')",
    
    # Άλλα Ευρωπαϊκά
    "Dutch Eredivisie": "Πρωτάθλημα Ολλανδίας (Eredivisie)",
    "Eredivisie": "Πρωτάθλημα Ολλανδίας (Eredivisie)",
    "Allsvenskan - Sweden": "Πρωτάθλημα Σουηδίας (Allsvenskan)",
    "Allsvenskan": "Πρωτάθλημα Σουηδίας (Allsvenskan)",
    "Super League - Greece": "Ελληνικό Πρωτάθλημα (Super League)",
    "Super League": "Ελληνικό Πρωτάθλημα (Super League)",
    "Belgium First Div": "Πρωτάθλημα Βελγίου (Pro League)",
    "Primeira Liga": "Πρωτάθλημα Πορτογαλίας",
    "Super Lig - Turkey": "Πρωτάθλημα Τουρκίας (Super Lig)",
    "Scottish Premiership": "Πρωτάθλημα Σκωτίας",
    
    # Αμερική & Ασία
    "Brazil Série A": "Πρωτάθλημα Βραζιλίας (Série A)",
    "Brazil Série B": "Πρωτάθλημα Βραζιλίας (Série B)",
    "MLS": "Πρωτάθλημα Αμερικής (MLS)",
    "Chinese Super League": "Πρωτάθλημα Κίνας (Super League)",
    "Super League - China": "Πρωτάθλημα Κίνας (Super League)",
    "Liga MX": "Πρωτάθλημα Μεξικού",
    "J-League": "Πρωτάθλημα Ιαπωνίας (J1 League)",
    "J League": "Πρωτάθλημα Ιαπωνίας (J1 League)",
    
    # Ευρωπαϊκές Διοργανώσεις
    "UEFA Champions League": "🏆 Τσάμπιονς Λιγκ",
    "UEFA Europa League": "🏆 Γιουρόπα Λιγκ",
    "UEFA Conference League": "🏆 Κόνφερενς Λιγκ"
}

# Custom CSS για τέλεια εμφάνιση
st.markdown("""
    <style>
    .sub-header-text {
        text-align: center;
        font-size: 16px;
        color: #6B7280;
        margin-bottom: 25px;
    }
    .match-row {
        font-size: 18px;
        font-weight: 600;
        padding: 5px 0px;
    }
    .prediction-box-bookie {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 12px;
        border-radius: 8px;
        border-left: 5px solid #EF4444;
        font-weight: bold;
        margin-top: 5px;
        margin-bottom: 15px;
    }
    .prediction-box-stat {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 12px;
        border-radius: 8px;
        border-left: 5px solid #F59E0B;
        font-weight: bold;
        margin-top: 5px;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Τίτλοι
st.title("⚽ VIP Προγνωστικά")
st.markdown('<div class="sub-header-text">🎯 Live ανανέωση βάσει αποδόσεων & στατιστικής</div>', unsafe_allow_html=True)

filename = "daily_predictions.txt"

if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
    
    blocks = content.split("---------------------------------------------")
    
    # Εμφάνιση ώρας τελευταίας ενημέρωσης
    if blocks:
        header_lines = blocks[0].strip().split("\n")
        for line in header_lines:
            if "Τελευταία ενημέρωση:" in line:
                st.caption(f"🕒 {line}")

    # Ομαδοποίηση ανά πρωτάθλημα
    leagues_dict = {}
    
    for block in blocks:
        lines = block.strip().split("\n")
        
        league = ""
        match_time = ""
        match_teams = ""
        prediction = ""
        
        for line in lines:
            if line.startswith("Πρωτάθλημα:"):
                league = line.replace("Πρωτάθλημα:", "").strip()
            elif line.startswith("Ώρα:"):
                match_time = line.replace("Ώρα:", "").strip()
            elif line.startswith("Αγώνας:"):
                match_teams = line.replace("Αγώνας:", "").strip()
            elif line.startswith("🎯 Πρόβλεψη:"):
                prediction = line.replace("🎯 Πρόβλεψη:", "").strip()
        
        if match_teams and prediction:
            if not league:
                league = "Λοιπά Πρωταθλήματα"
                
            if league not in leagues_dict:
                leagues_dict[league] = []
            leagues_dict[league].append({
                "time": match_time,
                "teams": match_teams,
                "prediction": prediction
            })

    # Σχεδίαση των αγώνων στην οθόνη
    if leagues_dict:
        for league_name, matches in leagues_dict.items():
            # Έλεγχος μετάφρασης από το λεξικό
            greek_league_name = LEAGUE_TRANSLATIONS.get(league_name, league_name)
            
            # Εδώ το "expanded=False" κρατάει τα μενού κλειστά αρχικά για να είναι καθαρή η οθόνη
            with st.expander(f"🏆 {greek_league_name} ({len(matches)})", expanded=False):
                for m in matches:
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if m['time']:
                            st.markdown(f"⏱️ **{m['time']}**")
                        else:
                            st.markdown("⏱️ --:--")
                    with col2:
                        st.markdown(f'<div class="match-row">{m["teams"]}</div>', unsafe_allow_html=True)
                    
                    if "🔥 [Bookmaker]" in m['prediction']:
                        clean_pred = m['prediction'].replace("🔥 [Bookmaker]", "").strip()
                        st.markdown(f'<div class="prediction-box-bookie">🔥 VIP Επιλογή: {clean_pred}</div>', unsafe_allow_html=True)
                    else:
                        clean_pred = m['prediction'].replace("📊 [Στατιστικό]", "").strip()
                        st.markdown(f'<div class="prediction-box-stat">📊 Στατιστικό: {clean_pred}</div>', unsafe_allow_html=True)
                    
                    st.markdown('<hr style="margin:10px 0px; border-top: 1px navajowhite;" />', unsafe_allow_html=True)
    else:
        st.info("ℹ️ Δεν υπάρχουν διαθέσιμοι αγώνες αυτή τη στιγμή.")
else:
    st.warning("⏳ Τα προγνωστικά δημιουργούνται αυτή τη στιγμή. Παρακαλώ ανανεώστε σε 1 λεπτό!")
