from service.transaction_service import TransactionService
from service.summary_service import SummaryService

class AppController:
    def __init__(self, root, profile, storage, filename):
        self.root = root
        self.profile = profile
        self.storage = storage
        self.filename = filename
        self.current_account = None

        self.tx_service = None
        self.summary_service = None

    def select_account(self, account):
        self.current_account = account
        self.tx_service = TransactionService(account)
        self.summary_service = SummaryService(account)
        self.storage.save(self.profile, self.filename)

    def add_deposit(self, date, desc, amount):
        self.tx_service.deposit(date, desc, amount)
        self.storage.save(self.profile, self.filename)

    def add_withdrawal(self, date, desc, amount):
        self.tx_service.withdraw(date, desc, amount)
        self.storage.save(self.profile, self.filename)

    def add_purchase(self, date, desc, amount, category, tax, fees, shipping, use_total=False):
        print("Account now has", len(self.current_account.transactions), "transactions")

        from model.transaction import Purchase
        purchase = Purchase(date, desc, amount, category, tax, fees, shipping, use_total)
        self.current_account.add_transaction(purchase)
        self.storage.save(self.profile, self.filename)


    def get_monthly_summary(self):
        return self.summary_service.monthly_totals()
