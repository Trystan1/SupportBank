import csv
import datetime
import json
import xml.etree.ElementTree as ET
from bank import Bank
import logging
logging.basicConfig(filename='SupportBank.log', filemode='w', level=logging.DEBUG)


def readCsv(filename):
    with open(filename) as csv_file:
        # create dictionary from csv file
        csv_reader = csv.DictReader(csv_file)

        # read all transactions into a dictionary for ease of access (csv_reader is weird)
        transactions = {}
        i = 0
        modifier = 0
        for row in csv_reader:
            found_error = False

            # exception to handle bad data in amount column
            try:
                row["Amount"] = int(float(row["Amount"]) * 100)
            except ValueError:
                logging.error(
                    f'A number was not entered in the "Amount" field on line {i + 2}, this line has been removed '
                    f'from the input dataset')
                found_error = True
            # exception to handle errors in the date column
            try:
                datetime.datetime.strptime(row["Date"], '%d/%m/%Y')
            except ValueError:
                logging.error(
                    f'Unrecognised date format on line {i + 2}, this line has been removed from the input dataset')
                found_error = True

            if found_error is False:
                transactions[i + modifier] = row
            else:
                modifier -= 1

            i += 1

        csv_file.close()

    return transactions


def readJson(filename):
    with open(filename, 'r') as myfile:
        data = myfile.read()
        json_reader = json.loads(data)

        i = 0
        modifier = 0
        transactions = {}
        for row in json_reader:

            found_error = False

            try:
                # amount needs to be converted into pence, date reversed and formatted with '/' instead of '-'
                int(float(row['amount']) * 100)
            except ValueError:
                logging.error(f'unexpected amount entry on line {i} ')
                found_error = True
            try:
                date_val = str(f'{row["date"][8:10]}/{row["date"][5:7]}/{row["date"][0:4]}')
                datetime.datetime.strptime(date_val, '%d/%m/%Y')
            except ValueError:
                logging.error(f'Date input on line {i} is not of recognised format')
                found_error = True

            if found_error is False:
                # copy dictionary across in same format as csv was
                transactions[i+modifier] = row
                transactions[i+modifier]['amount'] = int(float(row['amount']) * 100)
                transactions[i+modifier]['date'] = str(f'{row["date"][8:10]}/{row["date"][5:7]}/{row["date"][0:4]}')
                # rename dictionary keys to match previous style
                transactions[i+modifier]['Date'] = transactions[i].pop('date')
                transactions[i+modifier]['From'] = transactions[i].pop('fromAccount')
                transactions[i+modifier]['To'] = transactions[i].pop('toAccount')
                transactions[i+modifier]['Narrative'] = transactions[i].pop('narrative')
                transactions[i+modifier]['Amount'] = transactions[i].pop('amount')
            else:
                modifier -= 1
            i += 1

        return transactions


def readXml(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    i = 0
    modifier = 0
    transactions = {}
    for child in root:
        found_error = False

        # convert date into dd/mm/yyyy from xml file's days since 1900
        date_str = child.attrib["Date"]
        new_date = datetime.datetime(1900, 1, 1, 0, 0) + datetime.timedelta(int(date_str) - 1)
        new_date = new_date.strftime("%d/%m/%Y")

        try:
            int(float(child[1].text) * 100)
        except ValueError:
            logging.error(f'unrecognised value in amount field on line {i}')
            found_error = True
        try:
            datetime.datetime.strptime(new_date, '%d/%m/%Y')
        except ValueError:
            logging.error(f'unrecognised date format on line {i}')
            found_error = True

        if found_error is False:
            # define dictionary key headers on each iteration
            transactions[i+modifier] = {"Date": None, "From": None, "To": None, "Narrative": None, "Amount": None}
            transactions[i+modifier]["Date"] = new_date
            transactions[i+modifier]["From"] = child[2][0].text
            transactions[i+modifier]["To"] = child[2][1].text
            transactions[i+modifier]["Narrative"] = child[0].text
            transactions[i+modifier]["Amount"] = int(float(child[1].text)*100)
        else:
            modifier -= 1
        i += 1

    return transactions


def generateUsers(transactions, supportBank):
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

    # rearrange userlist into alphabetical order
    userlist = sorted(userlist)

    # create dictionary in class bank, containing an account for each member of the userlist
    for i in range(0, len(userlist)):
        supportBank.putAccount(userlist[i])

    return userlist


def doTransactions(transactions, supportBank):
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
                         f'{transactions[i]["Narrative"]}, New Balance: £{newBalance}')
        # store transaction statement in user's account
        accountFrom.transactionRecord(fromStatement)

        # access the account of the person with incoming money
        accountTo = supportBank.getAccount(str(transactions[i]["To"]))
        # increment the account balance of the person with incoming money
        accountTo.balanceChange(transactions[i]["Amount"])
        # retrieve the new balance for the person with incoming money
        newBalance = accountTo.balanceStatement()
        # generate a statement for the transaction
        toStatement = (f'On {transactions[i]["Date"]}, £{transactions[i]["Amount"]/100} was given to '
                       f'{transactions[i]["To"]} by {transactions[i]["From"]} for the purpose of '
                       f'{transactions[i]["Narrative"]}, New Balance: £{newBalance}')
        # store transaction statement in user's account
        accountTo.transactionRecord(toStatement)


def file_UI():
    run_UI = True
    transactions = {}
    filename = ''
    file_input = input('\nWelcome to the Bank \nWhich file do you want to import? \n1. Transactions2014.csv \n2. '
                       'DodgyTransactions2015.csv\n3. Transactions2013.json \n4. Transactions2012.xml'
                       '\nMake entry here:')
    if file_input == '1':
        filename = 'Transactions2014.csv'
        logging.info(f'User opened file: {filename}')
        transactions = readCsv(filename)
    elif file_input == '2':
        filename = 'DodgyTransactions2015.csv'
        logging.info(f'User opened file: {filename}')
        transactions = readCsv(filename)
    elif file_input == '3':
        filename = 'Transactions2013.json'
        logging.info(f'User opened file: {filename}')
        transactions = readJson(filename)
    elif file_input == '4':
        filename = 'Transactions2012.xml'
        logging.info(f'User opened file: {filename}')
        transactions = readXml(filename)
    elif file_input == 'Quit':
        run_UI = False
    else:
        print('Invalid data file selected')
        logging.error("Invalid data file selected")

    return transactions, run_UI, filename


def output_UI(userlist, transactions, supportBank, filename):
    run = True
    while run is True and transactions != {}:
        User_input = input(f'\nYou have loaded file {filename} \nList All for a list of all users and their current '
                           f'balances \nList \'User\' for all of the transactions of a given user \nPlease make your '
                           f'entry: ')

        if User_input == 'Quit':
            logging.info(f'User exited the output_UI')
            run = False
        elif User_input == 'List All':
            logging.info(f'User requested "List All"')
            for i in range(0, len(userlist)):
                currentBalance = supportBank.getAccount(userlist[i]).balanceStatement()
                print(f'{userlist[i]}, Balance: £{currentBalance}')
        elif User_input[5:8] != 'All':
            try:
                New_input = User_input.replace('List ', '')
                logging.info(f'User requested {New_input}\'s transaction history')
                statement = supportBank.getAccount(New_input).transactionStatement()
                print(*statement, sep="\n")
            except KeyError:
                print('Invalid command entered')
                logging.error(f'invalid command entered')
                run = False


def main():
    now = datetime.datetime.now()
    logging.info(f'Program start at {now.strftime("%Y-%m-%d %H:%M:%S")}')

    run_UI = True
    while run_UI is True:
        # initialise instance of class Bank
        supportBank = Bank()
        # prompt user for filename
        transactions, run_UI, filename = file_UI()
        if run_UI is False: break
        # generate list of strings of names (alphabetically sorted) and create an account for each of them
        userlist = generateUsers(transactions, supportBank)
        # calculate and record all transactions in each User's account
        doTransactions(transactions, supportBank)
        # prompt user for account display options
        output_UI(userlist, transactions, supportBank, filename)

    now = datetime.datetime.now()
    logging.info(f'User quit the program at {now.strftime("%Y-%m-%d %H:%M:%S")}')


if __name__ == "__main__":
    main()
