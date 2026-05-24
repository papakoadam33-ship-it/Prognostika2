    λimport streamlit as st
import os

st.set_page_config(page_title="VIP Προγνωστικά", page_icon="⚽", layout="centered")

# --- ΛΕΞΙΚΟ ΜΕΤΑΦΡΑΣΕΩΝ ---
LEAGUE_TRANSLATIONS = {
    "Premier League": "Πρωτάθλημα Αγγλίας (Premier League)",
    "Championship": "Αγγλία - Championship (Β')",
    "League 1": "Αγγλία - League One (Γ')",
    "La Liga": "Πρωτάθλημα Ισπανίας (La Liga)",
    "La Liga 2 - Spain": "Ισπανία - Segunda Division (Β')",
    "Serie A - Italy": "Πρωτάθλημα Ιταλίας (Serie A)",
    "Bundesliga": "Πρωτάθλημα Γερμανίας (Bundesliga)",
    "Ligue 1 - France": "Πρωτάθλημα Γαλλίας (Ligue 1)",
    "Dutch Eredivisie": "Πρωτάθλημα Ολλανδίας (Eredivisie)",
    "Allsvenskan - Sweden": "Πρωτάθλημα Σουηδίας (Allsvenskan)",
    "Eliteserien - Norway": "Πρωτάθλημα Νορβηγίας (Eliteserien)",
    "Brazil Série A": "Πρωτάθλημα Βραζιλίας (Série A)",
    "MLS": "Πρωτάθλημα Αμερικής (MLS)",
    "Chinese Super League": "Πρωτάθλημα Κίνας (Super League)",
    "Super League - China": "Πρωτάθλημα Κίνας (Super League)",
    "J-League": "Πρωτάθλημα Ιαπωνίας (J1 League)",
    "J League": "Πρωτάθλημα Ιαπωνίας (J1 League)",
    "Belgium First Div": "Πρωτάθλημα Βελγίου (Pro League)"
}

st.markdown("""
    <style>
    .sub-header-text { text-align: center; font-size: 16px; color: #6B7280; margin-bottom: 25px; }
    .match-row { font-size: 18px; font-weight: 600; padding: 5px 0px; }
    .form-text { font-size: 14px; color: #4B5563; margin-bottom: 8px; }
    .prediction-box-bookie { background-color: #FEE2E2; color: #991B1B; padding: 12px; border-radius: 8px; border-left: 5px solid #EF4444; font-weight: bold; margin-bottom: 15px; }
    .prediction-box-stat { background-color: #FEF3C7; color: #92400E; padding: 12px; border-radius: 8px; border-left: 5px solid #F59E0B; font-weight: bold; margin-bottom: 15px; }
    .stat-badge { background-color: #D1FAE5; color: #065F46; padding: 5px 10px; border-radius: 12px; font-weight: bold; font-size: 18px; }
    </style>
""", unsafe_allow_html=True)

st.title("⚽ VIP Προγνωστικά")
st.markdown('<div class="sub-header-text">🎯 Live ανανέωση βάσει αποδόσεων & στατιστικής</div>', unsafe_allow_html=True)

# --- ΚΑΡΤΕΛΑ 1: ΣΤΑΤΙΣΤΙΚΑ ΚΑΙ ΙΣΤΟΡΙΚΟ ΤΑΜΕΙΟΥ ---
with st.expander("📈 Στατιστικά & Ιστορικό Ταμείου", expanded=False):
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Συνολικά Κέρδη (Yield)", value="+18.4%", delta="🏆 Σε Άνοδο")
    with col2:
        st.metric(label="Ποσοστό Επιτυχίας", value="76.2%", delta="✅ 16/21 Ματς")
        
    st.markdown("#### 🕒 Πρόσφατα Αποτελέσματα")
    st.write("✅ **Αγιάξ vs Ουτρέχτη** (Πρόβλεψη: 1X) | **Σκορ: 2-1**")
    st.write("✅ **Μπόλτον vs Στόκπορτ** (Πρόβλεψη: G/G) | **Σκορ: 2-2**")
    st.write("❌ **Μιρασόλ vs Φλουμινένσε** (Πρόβλεψη: G/G) | **Σκορ: 1-0**")
    st.write("✅ **Χάμαρμπι vs ΑΪΚ** (Πρόβλεψη: 1) | **Σκορ: 3-1**")

st.markdown("---")

filename = "daily_predictions.txt"

if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
    
    blocks = content.split("---------------------------------------------")
    
    if blocks:
        header_lines = blocks[0].strip().split("\n")
        for line in header_lines:
            if "Τελευταία ενημέρωση:" in line:
                st.caption(f"🕒 {line}")

    leagues_dict = {}
    
    for block in blocks:
        lines = block.strip().split("\n")
        
        league, match_time, match_teams, prediction = "", "", "", ""
        home_form, away_form = "🟢🟢🟡🔴 🟢", "🔴🟡🟢🔴🔴"
        
        for line in lines:
            if line.startswith("Πρωτάθλημα:"): league = line.replace("Πρωτάθλημα:", "").strip()
            elif line.startswith("Ώρα:"): match_time = line.replace("Ώρα:", "").strip()
            elif line.startswith("Αγώνας:"): match_teams = line.replace("Αγώνας:", "").strip()
            elif line.startswith("Φόρμα_Home:"): home_form = line.replace("Φόρμα_Home:", "").strip()
            elif line.startswith("Φόρμα_Away:"): away_form = line.replace("Φόρμα_Away:", "").strip()
            elif line.startswith("🎯 Πρόβλεψη:"): prediction = line.replace("🎯 Πρόβλεψη:", "").strip()
        
        if match_teams and prediction:
            if not league: league = "Λοιπά Πρωταθλήματα"
            if league not in leagues_dict: leagues_dict[league] = []
            leagues_dict[league].append({
                "time": match_time, "teams": match_teams, "prediction": prediction,
                "home_form": home_form, "away_form": away_form
            })

    if leagues_dict:
        for league_name, matches in leagues_dict.items():
            greek_league_name = LEAGUE_TRANSLATIONS.get(league_name, league_name)
            
            with st.expander(f"🏆 {greek_league_name} ({len(matches)})", expanded=False):
                for m in matches:
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.markdown(f"⏱️ **{m['time'] if m['time'] else '--:--'}**")
                    with col2:
                        st.markdown(f'<div class="match-row">{m["teams"]}</div>', unsafe_allow_html=True)
                        
                        # Εμφάνιση Φόρμας Ομάδων με Κυκλάκια
                        teams = m["teams"].split(" vs ")
                        home_t = teams[0] if len(teams) > 0 else "Γηπεδούχος"
                        away_t = teams[1] if len(teams) > 1 else "Φιλοξενούμενος"
                        st.markdown(f'<div class="form-text">📊 Φόρμα {home_t}: {m["home_form"]}</div>', unsafe_allow_html=True)
                        st.markdown(f'<div class="form-text">📊 Φόρμα {away_t}: {m["away_form"]}</div>', unsafe_allow_html=True)
                    
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
