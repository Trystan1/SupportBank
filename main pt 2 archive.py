import csv
import logging
logging.basicConfig(filename='SupportBank.log', filemode='w', level=logging.DEBUG)

import datetime
from bank import Bank

def generateUsers(transactions):
    # Search the first two columns of the csv and add unique names to the user list
    userlist = []
    for i in range(0, len(transactions)):

        if transactions[i]["From"] in userlist:
            pass
        else:
            userlist.append(transactions[i]["From"])

        if transactions[i]["To"] in userlist:
            pass
        else:
            userlist.append(transactions[i]["To"])
    return userlist

def generateTransactions(csv_reader):
    transactions = {}
    i = 0
    modifier = 0

    for row in csv_reader:
        found_error = False

        # exception to handle bad data in amount column
        try:
            row["Amount"] = int(float(row["Amount"]) * 100)
        except:
            logging.error(f'A number was not entered in the "Amount" field on line {i+2}, this line has been removed '
                          f'from the input dataset')
            found_error = True

        # exception to handle errors in the date column
        try:
            datetime.datetime.strptime(row["Date"], '%d/%m/%Y')
        except:
            logging.error(f'Unrecognised date format on line {i+2}, this line has been removed from the input dataset')
            found_error = True

        if found_error is False:
            transactions[i + modifier] = row
        else:
            modifier -= 1

        i += 1

    return transactions

def doTransactions(transactions,supportBank):
    for i in range(0, len(transactions)):
        # access the account of the person with outgoing money
        accountFrom = supportBank.getAccount(str(transactions[i]["From"]))
        # decrement the account balance of the person with outgoing money
        accountFrom.balanceChange(-transactions[i]["Amount"])
        # retrieve the new balance for the person with outgoing money
        newBalance = accountFrom.balanceStatement()
        # generate a statement for the transaction
        fromStatement = (f'On {transactions[i]["Date"]}, £{transactions[i]["Amount"]/100} was taken from '
                                f'{transactions[i]["From"]} by {transactions[i]["To"]} for the purpose of '
                                f'{transactions[i]["Narrative"]}, New Balance: {newBalance}')
        # store transaction statement in user's account
        accountFrom.transactionRecord(fromStatement)

        # access the account of the person with incoming money
        accountTo = supportBank.getAccount(str(transactions[i]["To"]))
        # increment the account balance of the person with incoming money
        accountTo.balanceChange(transactions[i]["Amount"])
        # retrieve the new balance for the person with incoming money
        newBalance = accountTo.balanceStatement()
        # generate a statement for the transaction
        toStatement = (f'On  {transactions[i]["Date"]}, £{transactions[i]["Amount"]/100} was given to '
                                f'{transactions[i]["To"]} by {transactions[i]["From"]} for the purpose of '
                                f'{transactions[i]["Narrative"]}, New Balance: {newBalance}')
        # store transaction statement in user's account
        accountTo.transactionRecord(toStatement)

def main():

    # initialise instance of class Bank
    supportBank = Bank()
    now = datetime.datetime.now()
    print(f'Program start at {now.strftime("%Y-%m-%d %H:%M:%S")}')
    logging.info(f'Program start at {now.strftime("%Y-%m-%d %H:%M:%S")}')

    # with open('Transactions2014.csv') as csv_file:
    with open('DodgyTransactions2015.csv') as csv_file:
        logging.info(f'attempting to read file: {csv_file.name}')
        # create dictionary from csv file
        csv_reader = csv.DictReader(csv_file)
        # read all transactions into a dictionary for ease of access (csv_reader is weird)
        transactions = generateTransactions(csv_reader)
        # print(transactions)
        # generate list of strings of names
        userlist = generateUsers(transactions)
        # print(userlist)
        csv_file.close()

    # create dictionary in class bank, containing an account for each member of the userlist
    for i in range(0, len(userlist)):
        supportBank.putAccount(userlist[i])

    # calculate and record all transactions in each User's account
    doTransactions(transactions, supportBank)

    # here we have the user interface loop
    run = True
    while run == True:
        User_input = input('Welcome to the Bank \nList All for a list of all users and their current balances \n'
                           'List \'User\' for all of the transactions of a given user \nPlease make your entry: ')

        if User_input == 'Quit':
            now = datetime.datetime.now()
            logging.info(f'User quit the program at {now.strftime("%Y-%m-%d %H:%M:%S")}')
            run = False
        elif User_input == 'List All':
            logging.info(f'User requested "List All"')
            for i in range(0, len(userlist)):
                currentBalance = supportBank.getAccount(userlist[i]).balanceStatement()
                print(f'{userlist[i]}, Balance: {currentBalance}')

        elif User_input[5:8] != 'All':
            New_input = User_input.replace('List ', '')
            logging.info(f'User requested {New_input}\'s transaction history')
            statement = supportBank.getAccount(New_input).transactionStatement()
            print(*statement, sep="\n")

if __name__ == "__main__":
  main()