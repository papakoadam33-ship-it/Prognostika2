import streamlit as st
import os
import json

st.set_page_config(page_title="Προγνωστικά Στοιχήματος", page_icon="⚽", layout="centered")

st.title("⚽ Στατιστικά & Προγνωστικά")
st.write("Καλώς ορίσατε στην εφαρμογή προγνωστικών!")

if os.path.exists("daily_predictions.txt"):
    st.subheader("📊 Σημερινή Ανάλυση Αγώνα")
    
    # 1. Διαβάζουμε το αρχείο
    with open("daily_predictions.txt", "r", encoding="utf-8") as f:
        content = f.read()
    
    try:
        # 2. Απομονώνουμε το JSON κομμάτι από το αρχείο για να το επεξεργαστούμε
        json_part = content.split("--- Αναλυτικά Στατιστικά Αγώνα (JSON) ---")[-1].strip()
        data = json.loads(json_part)
        
        # 3. Παίρνουμε τα στοιχεία του αγώνα
        match_detail = data.get("response", {}).get("detail", {})
        match_name = match_detail.get("matchName", "Άγνωστος Αγώνας")
        match_round = match_detail.get("matchRound", "-")
        
        # Καθαρίζουμε λίγο το όνομα του αγώνα αν έχει ημερομηνίες μέσα
        clean_name = match_name.split("_")[0].replace("-vs-", " 🆚 ")
        match_date = match_name.split("_")[1].replace("_", " ") if "_" in match_name else ""

        # 4. Εμφανίζουμε τα στοιχεία όμορφα στην οθόνη
        st.info(f"🏆 **Διοργάνωση / Αγωνιστική:** Round {match_round}")
        
        # Μεγάλος τίτλος για το παιχνίδι
        st.markdown(f"### 🔥 {clean_name}")
        if match_date:
            st.write(f"📅 **Ημερομηνία:** {match_date}")
            
        # Εδώ μπορείς μελλοντικά να προσθέσεις αυτόματα προγνωστικά βασισμένα στα στατιστικά
        st.success("💡 **Πρόβλεψη Μοντέλου:** Η ανάλυση των στατιστικών είναι έτοιμη! (Εδώ μπορείς να βάλεις το δικό σου προγνωστικό).")

    except Exception as e:
        # Αν κάτι πάει στραβά με την ανάγνωση, δείχνει το απλό κείμενο όπως πριν
        st.text_area(label="Δεδομένα Αγώνα", value=content, height=400)
else:
    st.warning("Τα σημερινά προγνωστικά δεν έχουν δημιουργηθεί ακόμη.")
