import streamlit as st
import os

# Ρύθμιση Σελίδας
st.set_page_config(page_title="Marios Pro-Bet Pro", page_icon="⚡", layout="centered")

# Injection κώδικα για αλλαγή του εικονιδίου στην αρχική οθόνη του κινητού (Αστραπή)
st.markdown("""
    <head>
        <link rel="icon" type="image/png" href="https://img.icons8.com/emoji/96/000000/high-voltage-emoji.png" sizes="192x192">
        <link rel="apple-touch-icon" href="https://img.icons8.com/emoji/96/000000/high-voltage-emoji.png">
    </head>
""", unsafe_allow_html=True)

# CSS για Επαγγελματικό Στοιχηματικό Design (Dark Mode & Gold)
st.markdown("""
    <style>
    .main { background-color: #121212; }
    .title-container {
        background: linear-gradient(135deg, #1e1e1e 0%, #000000 100%);
        padding: 25px;
        border-radius: 15px;
        border: 2px solid #ffcc00;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0px 4px 15px rgba(255, 204, 0, 0.2);
    }
    .match-card {
        background-color: #1c1c1c;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #2d2d2d;
        margin-bottom: 12px;
    }
    .poisson-box {
        background-color: #262626;
        border-left: 4px solid #00bcff;
        color: #ffffff;
        padding: 10px;
        border-radius: 6px;
        margin-top: 5px;
        font-size: 14px;
    }
    .bookmaker-box {
        background: linear-gradient(90deg, #ffd700 0%, #ffaa00 100%);
        color: black !important;
        padding: 10px;
        border-radius: 6px;
        font-weight: bold;
        margin-top: 8px;
        font-size: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER ΕΦΑΡΜΟΓΗΣ ---
st.markdown("""
    <div class="title-container">
        <h1 style="color: #ffffff; margin: 0; font-size: 28px; letter-spacing: 1px;">⚡ MARIOS PRO-BET PRO ⚡</h1>
        <p style="color: #ffd700; margin: 5px 0 0 0; font-style: italic; font-size: 14px;">Dual Analysis Intelligence Model</p>
    </div>
""", unsafe_allow_html=True)

# --- ΣΥΝΑΡΤΗΣΗ ΚΑΘΑΡΙΣΜΟΥ ΟΝΟΜΑΤΩΝ ΠΡΩΤΑΘΛΗΜΑΤΩΝ ---
def clean_league_name(text):
    hardcoded = {
        "Λίγκε 1 - Φράνκε": "Γαλλία - Ligue 1 🇫🇷",
        "Μπουνντεσλίγκα 2 - Γκερμανυ": "Γερμανία - Bundesliga 2 🇩🇪",
        "Β' Σουηδίας (Superettan)": "Σουηδία - Superettan 🇸🇪"
    }
    return hardcoded.get(text.strip(), text)

DATA_FILE = "daily_predictions.txt"
predictions_date = ""
current_matches = []

# --- ΔΙΑΒΑΣΜΑ ΔΕΔΟΜΕΝΩΝ ΑΠΟ ΤΟ TXT ---
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    for line in lines:
        line = line.strip()
        if not line or line.startswith("STATS|") or "ΠΡΟΣΦΑΤΑ ΑΠΟΤΕΛΕΣΜΑΤΑ" in line or line.startswith("🏁"): 
            continue
        
        if line.startswith("--- ΠΡΟΓΝΩΣΤΙΚΑ"):
            predictions_date = line.replace("---", "").strip()
            continue
            
        if "|" in line:
            parts = line.split("|")
            if len(parts) >= 4:
                league = clean_league_name(parts[0])
                teams = parts[1]
                time_val = parts[2] if ":" in parts[2] else "📅 Σήμερα"
                
                full_prediction_text = " ".join(parts[3:])
                poisson_text = ""
                halftime_text = ""
                
                clean_pred = full_prediction_text.replace("📊 [Στατιστικό] ", "").replace("📊 ", "")
                
                if "1ο Ημίχ." in clean_pred:
                    pred_parts = clean_pred.split("1ο Ημίχ.")
                    poisson_raw = pred_parts[0].strip()
                    while poisson_raw and (not poisson_raw[-1].isalnum() and poisson_raw[-1] not in [')', ']']):
                        poisson_raw = poisson_raw[:-1].strip()
                    
                    poisson_text = poisson_raw
                    
                    halftime_raw = pred_parts[1].strip()
                    if "🟢" in halftime_raw or "🔴" in halftime_raw or "🟡" in halftime_raw:
                        for circle in ["🟢", "🔴", "🟡"]:
                            if circle in halftime_raw:
                                halftime_raw = halftime_raw.split(circle)[0].strip()
                    
                    while halftime_raw and halftime_raw.endswith("|"):
                        halftime_raw = halftime_raw[:-1].strip()
                        
                    halftime_text = f"✨ 1ο Ημίχ. {halftime_raw}"
                else:
                    poisson_text = clean_pred
                    halftime_text = "✨ Ανάλυση Ημιχρόνου: Κανονική Ροή Αγώνα 📈"
                
                raw_home_form = parts[-2] if len(parts) > 4 else "🟢🟢🟡🔴🟢"
                raw_away_form = parts[-1] if len(parts) > 5 else "🟢🔴🟢🟢🟡"
                
                home_emojis = "".join([c for c in raw_home_form if c in ['🟢', '🔴', '🟡']])
                away_emojis = "".join([c for c in raw_away_form if c in ['🟢', '🔴', '🟡']])
                
                if not home_emojis: home_emojis = "🟢🟢🟡🔴🟢"
                if not away_emojis: away_emojis = "🟢🔴🟢🟢🟡"
                
                current_matches.append({
                    "league": league, "teams": teams, "time": time_val,
                    "poisson": poisson_text, "halftime": halftime_text,
                    "home_form": home_emojis, "away_form": away_emojis
                })

if predictions_date:
    st.subheader(f"📅 {predictions_date}")

# --- ΕΜΦΑΝΙΣΗ ΑΓΩΝΩΝ ---
if current_matches:
    leagues = sorted(list(set(m["league"] for m in current_matches)))
    for league in leagues:
        st.markdown(f"<h3 style='color: #ffd700; margin-top: 25px; font-size: 20px;'>🏆 {league}</h3>", unsafe_allow_html=True)
        
        for m in current_matches:
            if m["league"] == league:
                st.markdown(f"""
                    <div class="match-card">
                        <span style="background-color: #dc3545; color: white; padding: 3px 8px; border-radius: 5px; font-size: 11px; font-weight: bold;">🕒 {m["time"]}</span>
                        <h4 style="color: #ffffff; margin: 10px 0 5px 0; font-size: 18px;">{m["teams"]}</h4>
                        <p style="color: #aaaaaa; margin: 0 0 12px 0; font-size: 13px;">📊 Φόρμα: {m["home_form"]} vs {m["away_form"]}</p>
                        <div class="poisson-box">📊 <b>Τελικό (Poisson):</b> {m["poisson"]}</div>
                        <div class="bookmaker-box">🔥 <b>1ο Ημίχρονο:</b> {m["halftime"]}</div>
                    </div>
                """, unsafe_allow_html=True)
else:
    st.info("⏳ Δεν υπάρχουν άλλα ενεργά ματς για σήμερα. Το μοντέλο θα ανανεωθεί αυτόματα στην επόμενη προγραμματισμένη ώρα!")

