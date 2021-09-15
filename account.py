class Account:

  name = ''

  def __init__(self, name):
    self.name = name
    self.balance = 0
    self.transactionHistory = []

  def getName(self):
    return self.name

  def balanceStatement(self):
    return self.balance/100

  def balanceChange(self, moneyIn):
    self.balance += moneyIn

  def transactionRecord(self, statement):
    self.transactionHistory.append(statement)

  def transactionStatement(self):
    return self.transactionHistory
