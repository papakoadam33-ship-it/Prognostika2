import streamlit as st
import os

# Ρύθμιση τίτλου της σελίδας
st.set_page_config(page_title="Live Αγώνες & Προγνωστικά", page_icon="⚽", layout="centered")

st.title("⚽ Live Αγώνες & Προγνωστικά")
st.subheader("📊 Οι σημερινές αυτόματες προτάσεις:")

filename = "daily_predictions.txt"

# Έλεγχος αν υπάρχει το αρχείο με τα προγνωστικά
if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as file:
        content = file.read()
    
    # Διαχωρίζουμε το κείμενο ανά αγώνα χρησιμοποιώντας τις παύλες που βάζει το main.py
    blocks = content.split("---------------------------------------------")
    
    # Εμφάνιση των στοιχείων κεφαλίδας (Ημερομηνία κτλ)
    if blocks:
        header = blocks[0].strip().split("\n\n")[0]
        st.info(header)
        
    # Εμφάνιση των αγώνων σε ωραία πλαίσια (cards)
    for block in blocks:
        lines = block.strip().split("\n")
        
        # Ψάχνουμε τις γραμμές για Πρωτάθλημα, Αγώνα και Πρόβλεψη
        league = ""
        match_teams = ""
        prediction = ""
        
        for line in lines:
            if line.startswith("Πρωτάθλημα:"):
                league = line.replace("Πρωτάθλημα:", "").strip()
            elif line.startswith("Αγώνας:"):
                match_teams = line.replace("Αγώνας:", "").strip()
            elif line.startswith("🎯 Πρόβλεψη:"):
                prediction = line.replace("🎯 Πρόβλεψη:", "").strip()
        
        # Αν βρήκαμε έγκυρο αγώνα, τον εμφανίζουμε σε "κουτάκι"
        if match_teams and prediction:
            with st.container():
                st.markdown(f"**🏆 {league}**")
                st.code(match_teams, language="text")
                st.success(f"🔮 Προγνωστικό: {prediction}")
                st.write("---")
else:
    # Μήνυμα σε περίπτωση που το GitHub Actions δεν έχει προλάβει ακόμα να φτιάξει το αρχείο
    st.warning("⏳ Τα προγνωστικά δημιουργούνται αυτή τη στιγμή από το σύστημα. Παρακαλώ ανανεώστε τη σελίδα σε 1 λεπτό!")
    
    # Εμφάνιση dummy δεδομένων για να μην φαίνεται άδεια η σελίδα στην πρώτη φόρτωση
    st.info("💡 Παράδειγμα εμφάνισης μόλις ολοκληρωθεί η ροή:")
    with st.container():
        st.markdown("**🏆 Premier League**")
        st.code("Arsenal vs Chelsea", language="text")
        st.success("🔮 Προγνωστικό: Goal / Goal")
