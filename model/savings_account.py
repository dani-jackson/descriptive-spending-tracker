# model/savings_account.py

from model.account import Account

class SavingsAccount(Account):
    def __init__(self, nickname=None, apy=0.02, transactions=None, budgets=None):
        super().__init__(
            "savings",
            nickname=nickname,
            transactions=transactions,
            budgets=budgets
        )
        self.apy = apy

    def monthly_interest(self):
        # Convert APY → monthly compounding rate
        monthly_rate = (1 + self.apy) ** (1/12) - 1
        return self.balance * monthly_rate

    def to_dict(self):
        base = super().to_dict()
        base["apy"] = self.apy
        return base
