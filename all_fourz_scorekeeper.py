import datetime
import os

# Define point values for keywords
POINT_VALUES = {
    "high": 1,
    "low": 1,
    "jack": 3,
    "hang": 3,
    "hangjack": 3,
    "game": 1,
    "trick": 1
}

# Ask for team names
team1 = input("Enter name for Team 1: ")
team2 = input("Enter name for Team 2: ")

# Ask for score limit
while True:
    try:
        score_limit = int(input("Enter the score limit to win the game (e.g. 14 or 21): "))
        break
    except ValueError:
        print("⚠️ Please enter a valid number.")

score1 = 0
score2 = 0
rounds = []

# Print colorful scoreboard
def print_scoreboard():
    def color_text(text, color_code):
        return f"\033[{color_code}m{text}\033[0m"

    print("\n+----------------+--------+")
    print("|     Team       | Score  |")
    print("+----------------+--------+")

    if score1 > score2:
        t1_color = "32"  # Green
        t2_color = "31"  # Red
    elif score2 > score1:
        t1_color = "31"
        t2_color = "32"
    else:
        t1_color = t2_color = "37"  # Gray

    print(f"| {color_text(team1, t1_color):<16} | {color_text(str(score1), t1_color):^6} |")
    print(f"| {color_text(team2, t2_color):<16} | {color_text(str(score2), t2_color):^6} |")
    print("+----------------+--------+")

# Score input helper
def get_valid_score(team_name):
    while True:
        entry = input(f"Enter points for {team_name} (e.g. 'jack trick' or number): ").strip().lower()

        if entry == "":
            print("⚠️ Please enter something.")
            continue

        if entry.isdigit():
            return int(entry)

        words = entry.split()
        total = 0
        unknown = []

        for word in words:
            if word in POINT_VALUES:
                total += POINT_VALUES[word]
            else:
                unknown.append(word)

        if unknown:
            print(f"⚠️ Unknown words: {', '.join(unknown)}. Try again.")
        else:
            return total

# Menu-based main loop
while True:
    print("\n📋 What would you like to do?")
    print("1. Enter score for both teams")
    print("2. Show scoreboard")
    print("3. Undo last round")
    print("4. Reset game")
    print("5. End game")
    choice = input("Enter option number (1-5): ").strip()

    if choice == "1":
        points1 = get_valid_score(team1)
        points2 = get_valid_score(team2)

        score1 += points1
        score2 += points2
        round_num = len(rounds) + 1
        rounds.append({
            "round": round_num,
            "team1": points1,
            "team2": points2
        })

        print_scoreboard()

        if score1 > score2:
            print(f"{team1} is winning!\n")
        elif score2 > score1:
            print(f"{team2} is winning!\n")
        else:
            print("It's a tie!\n")

        if score1 >= score_limit or score2 >= score_limit:
            print("\n🏁 Score limit reached!")
            break

    elif choice == "2":
        print_scoreboard()

    elif choice == "3":
        if rounds:
            last_round = rounds.pop()
            score1 -= last_round['team1']
            score2 -= last_round['team2']
            print("↩️ Last round undone!")
        else:
            print("⚠️ No rounds to undo.")
        print_scoreboard()

    elif choice == "4":
        confirm = input("Are you sure you want to reset the game? (yes/no): ").strip().lower()
        if confirm == "yes":
            score1 = score2 = 0
            rounds = []
            print("\n✅ Scores reset!")
            print_scoreboard()

    elif choice == "5":
        print("🛑 Ending game...")
        break

    else:
        print("⚠️ Invalid choice. Enter a number between 1 and 5.")

# Game Over
print("\n🎉 Game Over!")
print(f"Final Score - {team1}: {score1}, {team2}: {score2}")

if score1 > score2:
    winner = team1
    print(f"{team1} wins! 🏆")
elif score2 > score1:
    winner = team2
    print(f"{team2} wins! 🏆")
else:
    winner = "Tie"
    print("It's a tie! 🤝")

# Save to scores.txt
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open("scores.txt", "a") as file:
    file.write(f"Date: {timestamp}\n")
    for r in rounds:
        file.write(f"Round {r['round']}: {team1} +{r['team1']}, {team2} +{r['team2']}\n")
    file.write(f"Final Score: {team1}: {score1}, {team2}: {score2}\n")
    file.write(f"Winner: {winner}\n")
    file.write("-" * 30 + "\n")

# Track win totals
def update_win_totals(winning_team):
    filename = "win_totals.txt"
    totals = {}

    if os.path.exists(filename):
        with open(filename, "r") as f:
            for line in f:
                if ":" in line:
                    name, value = line.strip().split(":")
                    totals[name.strip()] = int(value.strip())

    if winning_team != "Tie":
        if winning_team in totals:
            totals[winning_team] += 1
        else:
            totals[winning_team] = 1

    with open(filename, "w") as f:
        for name, count in totals.items():
            f.write(f"{name}: {count}\n")

update_win_totals(winner)

print("✅ Game saved to 'scores.txt'")
print("✅ Win totals updated in 'win_totals.txt'")
