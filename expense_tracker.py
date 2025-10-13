import csv
import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt

# ---------- CONFIG ----------
FILENAME = "expenses.csv"

# ---------- INITIAL SETUP ----------
if not os.path.exists(FILENAME):
    with open(FILENAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Description", "Amount"])

# ---------- FUNCTIONS ----------
def add_expense():
    date = datetime.now().strftime("%Y-%m-%d")
    category = input("Enter category (Food, Travel, Bills, etc.): ")
    desc = input("Enter description: ")
    amount = float(input("Enter amount: "))

    with open(FILENAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, desc, amount])

    print("Expense added successfully.\n")

def view_expenses():
    df = pd.read_csv(FILENAME)
    if df.empty:
        print("No expenses found.\n")
    else:
        print("\n----- All Expenses -----")
        print(df.to_string(index=False))
        print()
        
def delete_expense():
    df = pd.read_csv(FILENAME)
    print(df)
    idx = int(input("Enter the index (row number) of expense to delete: "))

    if 0 <= idx < len(df):
        df = df.drop(idx)
        df.to_csv(FILENAME, index=False)
        print("Expense deleted successfully.\n")
    else:
        print("Invalid index.\n")

def monthly_summary():
    df = pd.read_csv(FILENAME)
    if df.empty:
        print("No data to summarize.\n")
        return

    df['Date'] = pd.to_datetime(df['Date'])
    df['Month'] = df['Date'].dt.strftime('%Y-%m')

    summary = df.groupby(['Month', 'Category'])['Amount'].sum().unstack(fill_value=0)
    print("\n----- Monthly Summary -----")
    print(summary)

    # Plot pie chart for latest month
    latest_month = df['Month'].iloc[-1]
    latest_data = df[df['Month'] == latest_month]
    cat_sum = latest_data.groupby('Category')['Amount'].sum()

    plt.title(f"Expense Breakdown ({latest_month})")
    cat_sum.plot(kind='pie', autopct='%1.1f%%')
    plt.ylabel('')
    plt.show()

# ---------- MAIN MENU ----------
def main():
    while True:
        print("========== Expense Tracker ==========")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Delete Expense")
        print("4. Monthly Summary & Chart")
        print("5. Exit")
        choice = input("Enter choice (1-5): ")

        if choice == '1':
            add_expense()
        elif choice == '2':
            view_expenses()
        elif choice == '3':
            delete_expense()
        elif choice == '4':
            monthly_summary()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid input, try again.\n")

if __name__ == "__main__":
    main()
