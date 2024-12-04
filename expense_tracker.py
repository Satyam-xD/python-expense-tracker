import csv
import datetime
import matplotlib.pyplot as plt

# File name for storing expenses
FILENAME = "expenses.csv"

# Function to add a new expense
def add_expense(expenses_list):
    try:
        amount = float(input("Enter the amount (₹): "))
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")
    except ValueError as e:
        print(f"Invalid input for amount: {e}")
        return
    
    category = input("Enter the category (e.g., Food, Transport): ").strip()
    date_input = input("Enter the date (YYYY-MM-DD) or leave blank for today: ").strip()
    
    try:
        if date_input:
            date = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()
        else:
            date = datetime.date.today()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    expense = {"amount": amount, "category": category, "date": date}
    expenses_list.append(expense)
    print("Expense added successfully!")

# Function to save expenses to a CSV file
def save_expenses(expenses_list, filename=FILENAME):
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["amount", "category", "date"])
        writer.writeheader()
        writer.writerows(expenses_list)

# Function to load expenses from a CSV file
def load_expenses(filename=FILENAME):
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            return [dict(row) for row in reader]
    except FileNotFoundError:
        return []

# Function to view summary of expenses by category and overall
def view_summary(expenses_list):
    total = sum(float(expense["amount"]) for expense in expenses_list)
    print(f"\nTotal spent: ₹{total:.2f}")

    category_totals = {}
    for expense in expenses_list:
        category = expense["category"]
        amount = float(expense["amount"])
        category_totals[category] = category_totals.get(category, 0) + amount

    print("\nSpending by category:")
    for category, amount in category_totals.items():
        print(f"{category}: ₹{amount:.2f}")

    view_graph(expenses_list)

# Function to generate spending graph
def view_graph(expenses_list):
    categories = [expense['category'] for expense in expenses_list]
    amounts = [float(expense['amount']) for expense in expenses_list]

    plt.figure(figsize=(8, 6))
    plt.bar(categories, amounts, color='lightblue')
    plt.title('Expenses by Category')
    plt.xlabel('Category')
    plt.ylabel('Amount (₹)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Function to delete an expense
def delete_expense(expenses_list):
    if not expenses_list:
        print("No expenses to delete.")
        return

    view_expenses(expenses_list)
    try:
        idx = int(input("Enter the expense number to delete (or 0 to cancel): "))
        if idx == 0:
            return
        if 1 <= idx <= len(expenses_list):
            del expenses_list[idx - 1]
            print("Expense deleted successfully!")
        else:
            print("Invalid number. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Function to edit an expense
def edit_expense(expenses_list):
    if not expenses_list:
        print("No expenses to edit.")
        return

    view_expenses(expenses_list)
    try:
        idx = int(input("Enter the expense number to edit (or 0 to cancel): "))
        if idx == 0:
            return
        if 1 <= idx <= len(expenses_list):
            expense = expenses_list[idx - 1]
            print(f"Editing expense {idx}: {expense}")

            amount = input(f"New amount (current: ₹{expense['amount']}): ").strip()
            category = input(f"New category (current: {expense['category']}): ").strip()
            date_input = input(f"New date (YYYY-MM-DD, current: {expense['date']}): ").strip()

            if amount:
                expense["amount"] = float(amount)
            if category:
                expense["category"] = category
            if date_input:
                expense["date"] = datetime.datetime.strptime(date_input, "%Y-%m-%d").date()

            print("Expense updated successfully!")
        else:
            print("Invalid number. Please try again.")
    except ValueError as e:
        print(f"Error: {e}")

# Function to display all expenses
def view_expenses(expenses_list):
    if not expenses_list:
        print("No expenses to display.")
        return

    for idx, expense in enumerate(expenses_list, start=1):
        print(f"{idx}. {expense['category']} - ₹{expense['amount']} on {expense['date']}")

# Main menu for user interaction
def menu():
    expenses_list = load_expenses()
    
    while True:
        print("\nMenu:")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Edit an Expense")
        print("4. Delete an Expense")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            add_expense(expenses_list)
            save_expenses(expenses_list)
        elif choice == '2':
            view_summary(expenses_list)
        elif choice == '3':
            edit_expense(expenses_list)
            save_expenses(expenses_list)
        elif choice == '4':
            delete_expense(expenses_list)
            save_expenses(expenses_list)
        elif choice == '5':
            save_expenses(expenses_list)
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")

# Run the expense tracker
if __name__ == "__main__":
    menu()
