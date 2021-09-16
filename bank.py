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