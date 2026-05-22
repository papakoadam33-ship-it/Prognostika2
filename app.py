# Αν χρησιμοποιείς Streamlit για την εφαρμογή σου, αυτός είναι ο κώδικας:
import streamlit as st
import os

st.set_page_config(page_title="Προγνωστικά Στοιχήματος", page_icon="⚽", layout="centered")

st.title("⚽ Live Στατιστικά & Προγνωστικά")
st.write("Καλώς ορίσατε στην εφαρμογή προγνωστικών!")

# Έλεγχος αν υπάρχει το αρχείο με τα δεδομένα
if os.path.exists("daily_predictions.txt"):
    st.subheader("Σημερινά Δεδομένα Αγώνων")
    
    # Ανάγνωση και εμφάνιση του αρχείου
    with open("daily_predictions.txt", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Εμφάνιση του περιεχομένου σε πλαίσιο κώδικα για να φαίνεται καθαρά
    st.text_area(label="Δεδομένα από το API-Football", value=content, height=400)
else:
    st.warning("Τα σημερινά προγνωστικά δεν έχουν δημιουργηθεί ακόμη. Παρακαλώ τρέξτε το main.py ή περιμένετε την αυτόματη ενημέρωση.")
