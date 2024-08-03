import pandas as pd
import matplotlib.pyplot as plt


from datetime import datetime
from tabulate import tabulate


def summary(start_date=None, end_date=None):  # default to None
    df = pd.read_csv("wallet.csv")
    df.index += 1  # indexing 1st column of df to start from "1" instead of "0"
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")  # changing str (in csv) to datetime object

    # Check if user input date or not
    # If user never input date, print ALL duration
    if start_date and end_date:
        start_date = pd.to_datetime(start_date)
        end_date = pd.to_datetime(end_date)
        date_mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[date_mask]

    # If user only input start_date, no end_date
    elif start_date:
        start_date = pd.to_datetime(start_date)
        end_date = df["date"].max()
        date_mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[date_mask]

    # If user only input end_date, no start_date
    elif end_date:
        end_date = pd.to_datetime(end_date)
        start_date = df["date"].min()
        date_mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[date_mask]

    # If user never input start/end date
    else:
        start_date = df["date"].min()
        end_date = df["date"].max()
        filtered_df = df

    # Print summary grouped by "currency"
    currency_group = filtered_df.groupby("currency")  # pandas mod -> to group by currency

    return currency_group, filtered_df, start_date, end_date


def plot(currency_group):
    # Plot transaction breakdown by category and type
    # Looping per Type per currency first (forloop above)
    for currency, row in currency_group:
        for transaction_type in ["Income", "Expense"]:  # loop through "Income", then "Expense"
            category_type_group = row[row["type"] == transaction_type].groupby("category")["amount"].sum().fillna(0)
            top5_category = category_type_group.nlargest(5)  # select the Top 5 categories

            if not top5_category.empty:  # check if top5 DataFrame is not empty
                ax = top5_category.plot(kind="barh", figsize=(10, 6), color="turquoise" if transaction_type == "Income" else "orangered", ec="black")
                plt.xlabel(f"Amount ({currency})")
                plt.ylabel("Category")
                plt.title(f"Top 5 {transaction_type} Transactions Breakdown ({currency})")
                plt.gca().invert_yaxis()  # to display the highest value at the top of barh

                # Show label at the end of each bar
                # i = index of each label
                for i, v in enumerate(top5_category):
                    plt.text(v + 2, i, f"{v:.2f}", color="black", fontweight="bold", va="center", ha="left")  # v + 2 means respective label value + 2 to the right

                if top5_category.max() >= 30:
                    plt.xlim(0,top5_category.max()*1.15)  # set border of barh to be 15% of max value of top5_category at each iteration
                    plt.show()
                else:
                    plt.xlim(0,top5_category.max()*1.25)  # set border of barh to be 25% of max value if max is too small < 30
                    plt.show()

    return


def view_summary():
    print("\nInsert the period of transaction that you're interested in below.")
    print('Leave blank to view ALL transactions.\n')
    while True:
        try:
            start_date = input("Start date (yyyy-mm-dd): ")
            end_date = input("End date (yyyy-mm-dd): ")
            currency_group, filtered_df, start_date, end_date = summary(start_date, end_date)

            if filtered_df.empty:
                print("\nNo transactions found in given date range.\n")
            else:
                # Tabulate the csv table using pandas
                # start/end_date from LHS (return date from summary())
                filtered_df["date"] = filtered_df["date"].dt.strftime("%Y-%m-%d")  # .strftime -> format string to %Y-%m-%d
                display_df = filtered_df.copy()  # copy df for display purpose
                display_df["amount"] = display_df["amount"].apply(lambda x:f"{x:.2f}")  # set "amount" to display in 2 d.p.
                sorted_date_df = display_df.sort_values(by=["date", "type"])  # sort values by date, then type

                print(f"\nTransaction history from {start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}.\n")
                print(tabulate(sorted_date_df, headers="keys", tablefmt="pretty", showindex=False))

            for currency, row in currency_group:
                total_income = row[row["type"] == "Income"]["amount"].sum()
                total_expense = row[row["type"] == "Expense"]["amount"].sum()
                net_spend = total_income - total_expense
                print(f"\nCurrency: {currency}")
                print(f"Income Summary: {currency} {total_income:.2f}")
                print(f"Expense Summary: {currency} {total_expense:.2f}")
                print(f"Net Spend Summary: {currency} {net_spend:.2f}")

            plot(currency_group)
            print("\n----- End of Transaction Summary -----")
            break

        # Calls when summary() function checks the date validity
        except ValueError:
            print("Invalid date format.\n")

    return
