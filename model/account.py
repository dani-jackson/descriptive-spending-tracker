# model/account.py

from collections import defaultdict
from datetime import datetime

# Import ALL transaction types, including the base Transaction class
from model.transaction import Deposit, Withdrawal, Purchase, Transaction


class Account:
    """
    Base Account class shared by Checking, Savings, and Credit accounts.
    Handles:
        • Transactions
        • Budgets
        • Balance calculation
        • Serialization
        • Monthly reports
    """

    def __init__(self, acct_type, nickname=None, transactions=None, budgets=None):
        self.acct_type = acct_type
        self.nickname = nickname or ""
        self.transactions = transactions or []
        self.budgets = budgets or {}   # <-- budgets now persist correctly
        self.balance = 0
        self._recalculate_balance()

    # ---------------------------------------------------------
    # Date Parsing
    # ---------------------------------------------------------
    def _parse_date(self, date_str):
        """Try multiple date formats until one works."""
        formats = [
            "%Y-%m-%d",
            "%m/%d/%y",
            "%m/%d/%Y",
            "%Y/%m/%d",
            "%y-%m-%d",
        ]

        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                pass

        raise ValueError(f"Unrecognized date format: {date_str}")

    # ---------------------------------------------------------
    # Balance Handling
    # ---------------------------------------------------------
    def _recalculate_balance(self):
        self.balance = sum(t.amount_signed() for t in self.transactions)

    def add_transaction(self, tx):
        self.transactions.append(tx)
        self._recalculate_balance()

    # ---------------------------------------------------------
    # Default: no interest (overridden by Savings/Credit)
    # ---------------------------------------------------------
    def monthly_interest(self):
        return 0

    # ---------------------------------------------------------
    # Serialization
    # ---------------------------------------------------------
    def to_dict(self):
        """Convert account to a JSON‑serializable dictionary."""
        return {
            "type": self.acct_type,
            "nickname": self.nickname,
            "transactions": [t.to_dict() for t in self.transactions],
            "budgets": self.budgets,   # <-- budgets saved correctly
        }

    @staticmethod
    def from_dict(data):
        """
        Rebuild an Account (or subclass) from saved JSON.
        Ensures budgets are loaded for ALL account types.
        """
        acct_type = data["type"]
        nickname = data.get("nickname")
        transactions = [Transaction.from_dict(t) for t in data.get("transactions", [])]
        budgets = data.get("budgets", {})

        # Import subclasses here to avoid circular imports
        from model.checking_account import CheckingAccount
        from model.savings_account import SavingsAccount
        from model.credit_card_account import CreditCardAccount

        if acct_type == "checking":
            return CheckingAccount(
                nickname=nickname,
                transactions=transactions,
                budgets=budgets
            )

        elif acct_type == "savings":
            return SavingsAccount(
                nickname=nickname,
                apy=data.get("apy", 0.02),
                transactions=transactions,
                budgets=budgets
            )

        elif acct_type == "credit":
            return CreditCardAccount(
                nickname=nickname,
                apr=data.get("apr", 0.24),
                transactions=transactions,
                budgets=budgets
            )

        else:
            raise ValueError(f"Unknown account type: {acct_type}")

    # ---------------------------------------------------------
    # Category Helpers
    # ---------------------------------------------------------
    def all_categories(self):
        """Return sorted list of all categories from budgets + purchases."""
        cats = set(self.budgets.keys())

        for tx in self.transactions:
            if hasattr(tx, "category") and tx.category:
                cats.add(tx.category)

        return sorted(cats)

    # ---------------------------------------------------------
    # Monthly Category Totals
    # ---------------------------------------------------------
    def monthly_category_totals(self):
        totals = defaultdict(lambda: defaultdict(float))

        for tx in self.transactions:
            dt = self._parse_date(tx.date)
            ym = (dt.year, dt.month)

            if hasattr(tx, "category") and tx.category:
                category = tx.category
            elif isinstance(tx, Deposit):
                category = "Deposit"
            elif isinstance(tx, Withdrawal):
                category = "Withdrawal"
            else:
                category = "Other"

            totals[ym][category] += tx.amount_signed()

        return totals

    # ---------------------------------------------------------
    # Monthly Category Percentages
    # ---------------------------------------------------------
    def monthly_category_percentages(self):
        totals = self.monthly_category_totals()
        percentages = {}

        for ym, cats in totals.items():
            month_total = sum(abs(v) for v in cats.values())
            pct_map = {}

            for cat, amount in cats.items():
                pct_map[cat] = (abs(amount) / month_total * 100) if month_total > 0 else 0

            percentages[ym] = pct_map

        return percentages

    # ---------------------------------------------------------
    # Monthly Budget Report
    # ---------------------------------------------------------
    def monthly_budget_report(self):
        totals = self.monthly_category_totals()
        report = {}

        for ym, cats in totals.items():
            month_report = {}

            for cat, spent in cats.items():
                spent = abs(spent)
                budget = self.budgets.get(cat)

                if budget is None:
                    month_report[cat] = {
                        "spent": spent,
                        "budget": None,
                        "over": None,
                        "under": None,
                    }
                else:
                    diff = budget - spent
                    month_report[cat] = {
                        "spent": spent,
                        "budget": budget,
                        "over": -diff if diff < 0 else 0,
                        "under": diff if diff > 0 else 0,
                    }

            report[ym] = month_report

        return report

    # ---------------------------------------------------------
    # Spending by Category (Pie Chart)
    # ---------------------------------------------------------
    def spending_by_category(self):
        totals = {}

        for tx in self.transactions:
            if isinstance(tx, Purchase):
                category = tx.category or "Uncategorized"
                amount = abs(getattr(tx, "total_cost", tx.amount))
                totals[category] = totals.get(category, 0) + amount

        return totals
