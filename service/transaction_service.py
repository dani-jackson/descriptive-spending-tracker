from model.transaction import Deposit, Withdrawal, Purchase

class TransactionService:
    def __init__(self, account):
        self.account = account

    def deposit(self, date, description, amount):
        d = Deposit(date, description, amount)
        self.account.add_transaction(d)
        return d

    def withdraw(self, date, description, amount):
        w = Withdrawal(date, description, amount)
        self.account.add_transaction(w)
        return w

    def purchase(self, date, description, amount, tax=0.087, fees=0, shipping=0, category=None):
        p = Purchase(date, description, amount, tax, fees, shipping, category)
        self.account.add_transaction(p)
        return p
