       
import json 
from datetime import datetime, timedelta
import os

class WomensHealthTracker:
    DATA_FILE = "user_data.json"

    def __init__(self):
        self.data = self.load_data()

    def load_data(self):
        """Load user data from a file, or initialize an empty data dictionary."""
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                print("Error: Data file is corrupted. Reinitializing data.")
                return {}
        return {}

    def save_data(self):
        """Save user data to a file."""
        with open(self.DATA_FILE, "w") as file:
            json.dump(self.data, file, indent=4)

    def register_user(self, username):
        """Register a new user."""
        if username in self.data:
            return f"Error: User '{username}' already exists."
        self.data[username] = {
            "last_cycle_date": None,
            "cycle_length": 28,
            "symptoms": [],
            "reminders": [],
        }
        self.save_data()
        return f"User '{username}' registered successfully!"

    def set_cycle_details(self, username, last_cycle_date, cycle_length):
        """Set or update menstrual cycle details for a user."""
        if username not in self.data:
            return "Error: User not found."
        try:
            datetime.strptime(last_cycle_date, "%Y-%m-%d")
        except ValueError:
            return "Error: Invalid date format. Use YYYY-MM-DD."
        self.data[username]["last_cycle_date"] = last_cycle_date
        self.data[username]["cycle_length"] = cycle_length
        self.save_data()
        return f"Cycle details updated for '{username}'."

    def add_symptom(self, username, symptom):
        """Log a symptom for the user."""
        if username not in self.data:
            return "Error: User not found."
        self.data[username]["symptoms"].append(
            {"symptom": symptom, "date": str(datetime.now().date())}
        )
        self.save_data()
        return f"Symptom '{symptom}' logged for '{username}'."

    def add_reminder(self, username, reminder, days_before):
        """Add a reminder for the user based on the next cycle date."""
        if username not in self.data:
            return "Error: User not found."
        last_cycle_date = self.data[username]["last_cycle_date"]
        cycle_length = self.data[username]["cycle_length"]

        if not last_cycle_date:
            return "Error: No cycle details found. Please set your cycle details first."

        next_cycle_date = datetime.strptime(
            last_cycle_date, "%Y-%m-%d"
        ) + timedelta(days=cycle_length)
        reminder_date = next_cycle_date - timedelta(days=days_before)

        self.data[username]["reminders"].append(
            {"reminder": reminder, "date": str(reminder_date.date())}
        )
        self.save_data()
        return f"Reminder '{reminder}' added for {username} on {reminder_date.date()}."

    def view_reminders(self, username):
        """View all reminders for a user."""
        if username not in self.data:
            return "Error: User not found."
        reminders = self.data[username]["reminders"]
        if not reminders:
            return "No reminders set."
        return "\n".join(
            [f"- {r['reminder']} on {r['date']}" for r in sorted(reminders, key=lambda x: x["date"])]
        )

    def predict_next_cycle(self, username):
        """Predict the next cycle date for the user."""
        if username not in self.data:
            return "Error: User not found."
        last_cycle_date = self.data[username]["last_cycle_date"]
        cycle_length = self.data[username]["cycle_length"]

        if not last_cycle_date:
            return "Error: No cycle details found. Please set your cycle details first."

        next_cycle_date = datetime.strptime(
            last_cycle_date, "%Y-%m-%d"
        ) + timedelta(days=cycle_length)
        return f"Next cycle for {username} is predicted on {next_cycle_date.date()}."

    def view_symptoms(self, username):
        """View all logged symptoms for a user."""
        if username not in self.data:
            return "Error: User not found."
        symptoms = self.data[username]["symptoms"]
        if not symptoms:
            return "No symptoms logged."
        return "\n".join(
            [f"- {s['symptom']} (logged on {s['date']})" for s in symptoms]
        )


def main():
    tracker = WomensHealthTracker()

    print("=== Welcome to Women's Health Tracker ===")

    while True:
        print("\nMenu:")
        print("1. Register User")
        print("2. Set Cycle Details")
        print("3. Add Symptom")
        print("4. Add Reminder")
        print("5. View Reminders")
        print("6. Predict Next Cycle")
        print("7. View Symptoms")
        print("8. Exit")

        choice = input("Choose an option (1-8): ").strip()

        if choice == "1":
            username = input("Enter your username: ").strip()
            print(tracker.register_user(username))

        elif choice == "2":
            username = input("Enter your username: ").strip()
            last_cycle_date = input("Enter last cycle date (YYYY-MM-DD): ").strip()
            try:
                cycle_length = int(input("Enter cycle length in days: ").strip())
            except ValueError:
                print("Error: Cycle length must be an integer.")
                continue
            print(tracker.set_cycle_details(username, last_cycle_date, cycle_length))

        elif choice == "3":
            username = input("Enter your username: ").strip()
            symptom = input("Enter the symptom: ").strip()
            print(tracker.add_symptom(username, symptom))

        elif choice == "4":
            username = input("Enter your username: ").strip()
            reminder = input("Enter the reminder: ").strip()
            try:
                days_before = int(input("Set the number of days before next cycle: ").strip())
            except ValueError:
                print("Error: Number of days must be an integer.")
                continue
            print(tracker.add_reminder(username, reminder, days_before))

        elif choice == "5":
            username = input("Enter your username: ").strip()
            print("Reminders:\n" + tracker.view_reminders(username))

        elif choice == "6":
            username = input("Enter your username: ").strip()
            print(tracker.predict_next_cycle(username))

        elif choice == "7":
            username = input("Enter your username: ").strip()
            print("Symptoms:\n" + tracker.view_symptoms(username))

        elif choice == "8":
            print("Thank you for using Women's Health Tracker!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
