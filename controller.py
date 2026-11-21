from datetime import datetime
from service.transaction_service import TransactionService
from service.summary_service import SummaryService
from service.budget_service import BudgetService

from model.account import Account
from model.category import Category


class AppController:

    def __init__(self, root, repository):

        self.root = root
        self.repository = repository

        self.tx_service = TransactionService(repository)
        self.summary_service = SummaryService(repository)
        self.budget_service = BudgetService(repository)

    # ------------------------
    # Accounts
    # ------------------------

    def add_account(self, name, account_type):

        account = Account(
            name=name,
            account_type=account_type
        )

        return self.repository.add_account(account)

    def update_account(
        self,
        account_id,
        name,
        account_type
    ):

        self.repository.update_account(
            account_id,
            name,
            account_type
        )

    def get_accounts(self):

        return self.repository.get_all_accounts()

    def delete_account(self, account_id):

        self.repository.delete_account(account_id)

    # ------------------------
    # Categories
    # ------------------------

    def add_category(self, name, monthly_limit=None):

        category = Category(
            name=name,
            monthly_limit=monthly_limit
        )

        return self.repository.add_category(category)

    def update_category(
        self,
        category_id,
        name,
        monthly_limit
    ):

        self.repository.update_category(
            category_id,
            name,
            monthly_limit
        )

    def update_category_budget(
        self,
        category_id,
        monthly_limit
    ):

        self.repository.update_category_budget(
            category_id,
            monthly_limit
        )

    def get_categories(self):

        return self.repository.get_all_categories()

    def get_category(
        self,
        category_id
    ):

        row = self.conn.execute("""
            SELECT *
            FROM categories
            WHERE id = ?
        """, (
            category_id,
        )).fetchone()

        if row is None:
            return None

        return Category(
            id=row["id"],
            name=row["name"],
            monthly_limit=row["monthly_limit"]
        )

    def delete_category(self, category_id):

        self.repository.delete_category(category_id)

    # ------------------------
    # Transactions
    # ------------------------

    def add_transaction(
        self,
        transaction_type,
        date,
        description,
        amount,
        merchant=None,
        account_id=None,
        category_id=None
    ):

        return self.tx_service.create_transaction(
            transaction_type,
            date,
            description,
            amount,
            merchant,
            account_id,
            category_id
        )

    def update_transaction(
        self,
        transaction
    ):

        self.repository.update_transaction(
            transaction
        )

    def get_transactions(self):

        return self.repository.get_all_transactions()

    def delete_transaction(self, transaction_id):

        self.repository.delete_transaction(transaction_id)

    # ------------------------
    # Reports
    # ------------------------

    def get_monthly_total(
        self,
        year,
        month
    ):

        return self.summary_service.monthly_total_spending(
            year,
            month
        )

    def get_monthly_totals(
        self,
        year,
        month
    ):

        return self.summary_service.monthly_totals(
            year,
            month
        )

    def get_monthly_percentages(
        self,
        year,
        month
    ):

        return self.summary_service.monthly_percentages(
            year,
            month
        )

    def get_current_month_totals(self):

        today = datetime.now()

        return self.get_monthly_totals(
            today.year,
            today.month
        )


    def get_current_month_percentages(self):

        today = datetime.now()

        return self.get_monthly_percentages(
            today.year,
            today.month
        )