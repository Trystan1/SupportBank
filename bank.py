from account import Account

class Bank:
  accounts = {}

  def putAccount(self, name):
    self.accounts[name] = Account()

  def getAccount(self, name) -> Account:
    pass