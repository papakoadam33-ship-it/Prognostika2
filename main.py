import random

def calculate_tip(odds_1, odds_x, odds_2):
    try:
        o1, ox, o2 = float(odds_1), float(odds_x), float(odds_2)
        p1, px, p2 = (1/o1)*100, (1/ox)*100, (1/o2)*100
        total = p1 + px + p2
        prob_1 = (p1 / total) * 100
        prob_2 = (p2 / total) * 100
        
        if prob_1 > 55 and o1 < 1.70: return "1 (Άσος) & Over 1.5"
        elif prob_2 > 55 and o2 < 1.70: return "2 (Διπλό) & Over 1.5"
        elif abs(prob_1 - prob_2) < 8: return "Goal/Goal & Over 2.5" if (o1+o2)/2 < 2.60 else "2-3 Γκολ"
        elif ox > 3.60: return "Over 2.5 Γκολ"
        else: return "Under 2.5 Γκολ"
    except:
        return "1X Διπλή Ευκαιρία"

print("⏳ Παραγωγή αυτόματων καθημερινών αγώνων...")

# Λίστα με κορυφαίες ευρωπαϊκές ομάδες για να υπάρχει ποικιλία
teams_pool = [
    "Real Madrid", "Manchester City", "Bayern Munich", "PSG", "Liverpool", 
    "Arsenal", "Inter Milan", "Juventus", "Atletico Madrid", "Dortmund",
    "Leverkusen", "Barcelona", "AC Milan", "Aston Villa", "Sporting Lisbon"
]

# Πιθανά σετ αποδόσεων
odds_pool = [
    ("1.55", "4.20", "5.50"),
    ("2.15", "3.40", "3.10"),
    ("2.50", "3.20", "2.80"),
    ("1.80", "3.60", "4.20"),
    ("3.20", "3.30", "2.20")
]

# Πιθανές ώρες διεξαγωγής
times_pool = ["17:00", "19:30", "21:45", "22:00"]

try:
    # Επιλέγουμε τυχαίους συνδυασμούς ομάδων για να αλλάζουν αυτόματα κάθε μέρα!
    random.seed(None) # Εξασφαλίζει ότι κάθε φορά που τρέχει, οι αγώνες θα είναι διαφορετικοί
    
    selected_matches = []
    used_teams = set()
    
    while len(selected_matches) < 8:
        home = random.choice(teams_pool)
        away = random.choice(teams_pool)
        
        if home != away and home not in used_teams and away not in used_teams:
            selected_matches.append((home, away))
            used_teams.add(home)
            used_teams.add(away)

    with open("daily_predictions.txt", "w", encoding="utf-8") as f:
        for home_team, away_team in selected_matches:
            match_time = random.choice(times_pool)
            m1, mx, m2 = random.choice(odds_pool)
            
            generated_tip = calculate_tip(m1, mx, m2)
            
            # Εγγραφή στο αρχείο κειμένου
            line = f"{match_time} | {home_team} vs {away_team} | {m1} - {mx} - {m2} | {generated_tip}\n"
            f.write(line)
            print(f"✅ Δημιουργήθηκε: {home_team} vs {away_team} ({match_time})")
            
    print("🚀 Το αρχείο daily_predictions.txt ενημερώθηκε με επιτυχία!")
except Exception as e:
    print(f"❌ Σφάλμα: {e}")
