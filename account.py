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
