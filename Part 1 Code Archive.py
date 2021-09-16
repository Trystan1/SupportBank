## account.py

class Account:

  name = ''

  def __init__(self, name):
    # initialise variables with the initialisation method to keep them unique to each account
    self.name = name
    self.balance = 0
    self.transactionHistory = []

  def getName(self):
    # return the name of the subclass when called
    return self.name

  def balanceStatement(self):
    # return the balance of the subclass in £ (all transactions recorded in pence)
    return self.balance/100

  def balanceChange(self, moneyIn):
    self.balance += moneyIn

  def transactionRecord(self, statement):
    self.transactionHistory.append(statement)

  def transactionStatement(self):
    return self.transactionHistory

## bank.py

from account import Account

class Bank:
  # initialise empty dictionary of accounts
  accounts = {}

  def putAccount(self, name):
    # add a name and the class 'Account' to the dictionary 'accounts'
    self.accounts[name] = Account(name)

  def getAccount(self, name) -> Account:
    # return the Account subclass relating to the account name
    return self.accounts[name]

  # def __str__(self):
  #   return f'{}' # this is how you return strings

## main.py

import csv
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
    for row in csv_reader:
        transactions[i] = row
        transactions[i]["Amount"] = int(float(row["Amount"])*100)
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

    with open('Transactions2014.csv') as csv_file:
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
            run = False
        elif User_input == 'List All':
            for i in range(0, len(userlist)):
                currentBalance = supportBank.getAccount(userlist[i]).balanceStatement()
                print(f'{userlist[i]}, Balance: {currentBalance}')

        elif User_input[5:8] != 'All':
            New_input = User_input.replace('List ', '')
            print(f'{New_input}')
            statement = supportBank.getAccount(New_input).transactionStatement()
            print(*statement, sep="\n")
            # print(f'{len(statement)}')

if __name__ == "__main__":
  main()