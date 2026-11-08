# model/credit_card_account.py

from model.account import Account

class CreditCardAccount(Account):
    def __init__(self, nickname=None, apr=0.24, transactions=None, budgets=None):
        super().__init__(
            "credit",
            nickname=nickname,
            transactions=transactions,
            budgets=budgets
        )
        self.apr = apr

    def monthly_interest(self):
        monthly_rate = self.apr / 12
        return self.balance * monthly_rate

    def to_dict(self):
        base = super().to_dict()
        base["apr"] = self.apr
        return base
