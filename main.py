import csv
from account import Account

def readFile():
    # mostly copied from https://realpython.com/python-csv/#parsing-csv-files-with-pythons-built-in-csv-library
    with open('Transactions2014.csv') as f:
        csv_reader = csv.reader(f, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {",".join(row)}')
                line_count += 1

            else:
                print(f'\t on {row[0]} ,{row[1]} gave {row[2]} {row[3]} for the amount of £{row[4]}')
                line_count += 1
        print(f'Processed {line_count} lines.')
        f.close()

def readFiletoDict():
    # mostly copied from https://realpython.com/python-csv/#parsing-csv-files-with-pythons-built-in-csv-library
    with open('Transactions2014.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {",".join(row)}')
                line_count += 1

            print(f'\t on {row["Date"]} ,{row["From"]} gave {row["To"]} {row["Narrative"]} for the amount of £{row["Amount"]}')
            line_count += 1
        print(f'Processed {line_count} lines.')
        csv_file.close()

def main():
    # mostly copied from https://realpython.com/python-csv/#parsing-csv-files-with-pythons-built-in-csv-library
    with open('Transactions2014.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            # if line_count == 0:
            #     print(f'Column names are {",".join(row)}')
            #     line_count += 1

            # this works, now just need to prevent duplication of accounts
            account = Account(row["From"])
            print(f'{account.name}')
            # print(f'\t on {row["Date"]} ,{row["From"]} gave {row["To"]} {row["Narrative"]} for the amount of £{row["Amount"]}')
            # line_count += 1

            # print(Account.name)
            # processing of account statements here
        # print(Account.name)
        csv_file.close()

main()


# from bank import Bank
#
# def main():
#   supportBank = Bank()
#   supportBank.putAccount('Bob')
#
# if __name__ == "__main__":
#   main()