# Multi-Currency Financial Wallet & Currency Converter

### Video Demo on YouTube:
https://youtu.be/y4_tZOmHot4

## Foreword
I’m excited to share my journey into the world of programming with you. Learning to code is a crucial skill in today’s job market, and I’m eager to leverage this knowledge to open new career opportunities. I hope you find this project as exciting and insightful as I do!

## My First Ever Project
Introducing my first ever programming project - Multi-Currency Financial Wallet & Currency Converter

This project is a culmination of Python knowledge and concept I acquired through the CS50P course. My goal is to showcase the skills I learned and expand my skill set even further to pave the way for a successful career transition.

In this project, I’ve utilized a variety of library modules covered in the course, along with additional ones not covered in the course, like pandas, matplotlib and datetime modules. These tools are incredibly useful, especially for anyone aspiring to equip themselves with more advanced data analytic skills.


## Description
The project is a financial wallet that supports multi-currency with additional currency converter function. Currently, the program supports 3 currencies: SGD, USD and EUR.


## Features
The program offers 3 main functions, accessible by inputting the corresponding choice:

1. **Record Transactions**: Add details of your spending in multi-currencies (SGD|USD|EUR).
2. **Currency Converter**: Convert amounts between different currencies in your balance.
3. **View Transaction Summary**: View a summary of your transaction history within a specified date range.


## Running the Program
To start the program, insert the followings in your terminal: <br> <br>
Go into the project folder:
~~~bash
cd project
~~~

Execute the main script:
~~~bash
python project.py
~~~


You will be presented with the following options:<br>
### Main Menu

1. **Press "W" for Wallet**: Record a new transaction.
2. **Press "C" for Currency Converter**: Convert an amount from your desired currency to another in your balance.
3. **Press "V" for View Transaction Summary**: View a summary of your transaction record within a specified date range.
4. **Press any other keys to Exit**: Exit the Program.

### Choices

#### **1. Wallet (Press "W")**
You will be prompted to input the following details, in order to record a transaction successfully:

- **Date of Transaction**: Enter the date in specific format (yyyy-mm-dd) or leave blank for today's date.
- **Currency**: Enter "SGD", "USD" or "EUR".
- **Amount**: Enter the transaction amount.
- **Type of Transaction**: Enter "I" for Income or "E" for Expense.
- **Category of Transaction** (optional): Enter a category for the transaction.

Each input will be recorded and saved as a transaction in a csv file named "wallet.csv". Any discrepancies in user's input will be handled and re-prompt users for input again.

<br>

#### **2. Currency Converter (Press "C")**
The currency converter will show you a tabulated summary of your amount balance for each currency.

You will be prompted to input the following details, in order to convert a currency successfully:

- **Currency to convert from**: Enter "SGD", "USD" or "EUR".
- **Amount to convert from**: Enter the amount to convert.
- **Currency to convert to**: Enter "SGD", "USD" or "EUR".

After conversion, the program will show you the base exchange rate and the amount you converted.
The currency conversion will be recorded in "wallet.csv" and categorized under "Currency Exchange".<br>
Any discrepancies in user's input e.g. insufficient balance in your wallet will be handled and re-prompt users for input again.

<br>

#### **3. View Transaction Summary (Press "V")**
An overview of your incomes and expenses within a specified date range for each currency.

- **Start date (yyyy-mm-dd)**: Enter a lower date range in specific format (yyyy-mm-dd)
- **End date (yyyy-mm-dd)**: Enter an upper date range in specific format (yyyy-mm-dd)

For date inputs above, can leave either or both dates as blank.<br>
(i) **Both blank**: Show ALL transaction history.<br>
(ii) **Either one blank**: Show earliest date in transaction history to specified end date, or vice versa.

The transaction record within specified date range will be summarized and presented in horizontal bar charts for each currency. Any discrepancies in user's input will be handled and re-prompt users for input again.

<br>

## Modules
### Main Module
1. project.py
- The main script to run the application.
- Asks users for input to record a transaction into csv named "wallet.csv".
- Calls sub-modules like converter.py and summary.py to support currency conversion and view transaction summary respectively.

### Sub-Module
1. converter.py
- Gets live currency exchange rate from API.
- Asks users for input e.g. currencies and amount to convert.
- Performs the currency conversion and records into "wallet.csv".

2. summary.py
- Reads from "wallet.csv" using pandas module to access all transaction record.
- Summarizes the total income, total expense and net spending for each currency within a user-specified date range.
- Plots the Income and Expense breakdown for each currency using horizontal bar charts.
- Visualizes the transaction breakdown by Top 5 Income/Expense categories for each currency.


## Dependencies
To run this project with Python, you need the followings:

To obtain exchange rate for currency conversion:
- Generate API KEY from [Currency Converter API](https://free.currencyconverterapi.com/)


You can install the required dependencies with the following command in your terminal:

~~~bash
pip install -r requirements.txt
~~~


## Future Improvements
- Allows users to edit/delete recorded transaction in case of typo
- Allow users to customize more plots e.g. show spending summary of certain category
- Allow users to view currency exchange rate trend
- Allow users to set a budget and notify them when exceeding the limit
- Supports more currencies for transaction record and currency conversion

## Disclaimers
This is my Final Project submission for CS50's Introduction to Programming with Python.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for more details.
