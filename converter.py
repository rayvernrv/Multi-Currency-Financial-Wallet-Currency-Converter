import requests
import csv


from tabulate import tabulate
from datetime import date

# from my own project
from summary import summary

base_url = "https://free.currconv.com/"
api_key = "0b4c97edeb6c5fe0a394"


def get_currencies():
    endpoint = f"api/v7/currencies?apiKey={api_key}"
    response = requests.get(base_url + endpoint)
    currencySymbol = []
    for currency in ["SGD", "USD", "EUR"]:
        object = response.json()["results"][currency]
        currencySymbol.append(object["currencySymbol"])

    return currencySymbol


def convert_intro():
    currency_group = summary()[0]  # index[0] to get 1st return of summary()
    total_amount = {}  # dict to get currency: net_spend pairs
    for currency, row in currency_group:
        total_income = row[row["type"] == "Income"]["amount"].sum()
        total_expense = row[row["type"] == "Expense"]["amount"].sum()
        net_spend = total_income - total_expense
        total_amount.update({currency: net_spend})

    print("\nWelcome to currency converter!")
    print("Recorded balance in your wallet for each currency is as follows:")

    # tuple (currency, amount) in a dict, sorted on 2nd elemet index[1] in descending order
    currency_table = sorted({(currency, f"{total_amount.get(currency, 0.00):.2f}") for currency in ["SGD", "USD", "EUR"]}, key=lambda x:x[1], reverse=True)
    print(tabulate(currency_table, headers=["Currency", "Amount Balance"], tablefmt="pretty", stralign="center"))

    return total_amount


def convert():
    total_amount = convert_intro()
    currencySymbol = get_currencies()
    currencies = ["SGD", "USD", "EUR"]
    pair_dict = dict(zip(currencies, currencySymbol))  # zip 2 lists into 1 dictionary

    while True:
        from_currency = input("Currency to convert from (SGD | USD | EUR): ").strip().upper()
        if from_currency in currencies:
            while True:
                try:
                    from_amount = float(input("Amount to convert from: "))
                    if from_amount < total_amount[from_currency]:
                        while True:
                            to_currency = input("Currency to convert to (SGD | USD | EUR): ").strip().upper()
                            if to_currency in currencies:

                                endpoint = f"api/v7/convert?q={from_currency}_{to_currency}&compact=ultra&apiKey={api_key}"
                                response = requests.get(base_url + endpoint)
                                exchange_rate = response.json()[f"{from_currency}_{to_currency}"]
                                to_final_amount = float(f"{(from_amount * exchange_rate):.2f}")

                                with open("wallet.csv", "a") as file:
                                    writer = csv.DictWriter(file, fieldnames=["date", "currency", "amount", "type", "category"])
                                    writer.writerow({"date": date.today(), "currency": from_currency, "amount": f"{from_amount:.2f}", "type": "Expense", "category": "Currency Exchange"})
                                    writer.writerow({"date": date.today(), "currency": to_currency, "amount": f"{to_final_amount:.2f}", "type": "Income", "category": "Currency Exchange"})

                                print("------------------------------------------------------------------------------------------")
                                print(f"Base Exchange Rate: {from_currency} {pair_dict[from_currency]}1.00 = {to_currency} {pair_dict[to_currency]}{1*exchange_rate}")
                                print(f"You've successfully converted: {from_currency} {pair_dict[from_currency]}{from_amount:.2f} to {to_currency} {pair_dict[to_currency]}{to_final_amount:.2f} !\n")
                                print("The currency exchange transaction has been recorded in your wallet.")
                                print("------------------------------------------------------------------------------------------\n")

                                return to_final_amount

                            else:
                                print(f"\nThis program does not support {to_currency} at the moment.")
                                print("Please try again with (SGD | USD | EUR) only.\n")

                    else:
                        print(f"\nYou do not have enough balance for {from_currency}.")
                        opt1 = input('Press "B" to go back to currency selection OR any other keys to input amount again: ').strip().upper()
                        print()
                        if opt1 == "B":
                            break

                except ValueError:
                    print("\nInvalid input. Please input the amount in numeric format\n")

        else:
            print(f"\nThis program does not support {from_currency} at the moment.")
            print("Please try again with (SGD | USD | EUR) only.\n")



