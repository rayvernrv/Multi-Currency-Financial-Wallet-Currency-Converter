import sys
import csv
import os.path


from datetime import date

# from my own project
from converter import convert  # to convert currency
from summary import view_summary  # to view transaction summary



def main():
    print("\nWelcome to your personalized wallet!\n")
    while True:
        opt = input('Enter your action:\n'
                    '1. Press "W" for Wallet to record your transaction.\n'
                    '2. Press "C" for Currency Converter.\n'
                    '3. Press "V" to View Transaction Summary within date range.\n'
                    '4. Press any other key to Exit.\n\n'
                    'Choice: ').strip().upper()

        if opt == "W" or opt == "WALLET":
            wallet()
        elif opt == "C" or opt == "CONVERT":
            convert()
        elif opt == "V" or opt == "VIEW":
            view_summary()
        else:
            sys.exit("\nYou have exited the program.\n")  # SystemExit is caught when running in Interactive Window


def wallet():
    d = date_format()
    c = currency()
    a = amount()
    t = type_()
    category = input("Category of Transaction (optional): ").strip().title()
    store_csv(d, c, a, t, category)
    print("\n--------------------------------------------------------")
    print("Your transaction has been recorded successfully !")
    print("--------------------------------------------------------\n")


def store_csv(d, c, a, t, category):
    file_exist = os.path.isfile("wallet.csv")
    with open("wallet.csv", "a") as file:
        writer = csv.DictWriter(file, fieldnames=["date", "currency", "amount", "type", "category"])
        if not file_exist:  # if file existed, do not write header anymore
            writer.writeheader()
        writer.writerow({"date": d, "currency": c, "amount": a, "type": t, "category": category})


def date_format():
    while True:
        try:
            d = input('\nDate of Transaction (yyyy-mm-dd) or Leave blank for today\'s date: ').strip()
            if d:
                year, month, day = d.split("-")
                return date(int(year), int(month), int(day))
            else:
                return date.today()
        except ValueError:
            print("\nInvalid date.")


def currency():
    currencies = ["SGD", "USD", "EUR"]
    while True:
        currency = input("Currency (SGD | USD | EUR): ").strip().upper()
        if currency in currencies:
            return currency
        else:
            print("\nInvalid currency.\n")


def amount():
    while True:
        try:
            amount = float(input("Amount: "))
            if amount > 0:
                return f"{amount:.2f}"
            else:
                print("\nAmount cannot be negative. ", end="")
                opt = input("Press R to retry OR any other keys to Exit Program: ").strip().upper()
                print()
                if opt == "R":
                    pass
                else:
                    sys.exit("You have exited the program.")
        except ValueError:
            print("\nInvalid input. Please input the amount in numeric format.\n")


def type_():
    types = {"I": "Income", "E": "Expense"}
    while True:
        t = input("Type of Transaction (I for Income, E for Expense): ").strip().title()
        if t in types:
            return types[t]  # to get the values of types dict
        elif t == "Income" or t == "Expense":
            return t
        else:
            print('\nInvalid input. Press "I" for Income or "E" for Expense.\n')


if __name__ == "__main__":
    main()
