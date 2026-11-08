# model/checking_account.py

from model.account import Account

class CheckingAccount(Account):
    def __init__(self, nickname=None, transactions=None, budgets=None):
        super().__init__(
            "checking",
            nickname=nickname,
            transactions=transactions,
            budgets=budgets
        )
