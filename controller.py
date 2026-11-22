from datetime import datetime, date
import calendar
from service.transaction_service import TransactionService
from service.summary_service import SummaryService
from service.budget_service import BudgetService
from model.account import Account
from model.category import Category
from model.recurring_bill import RecurringBill


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
        return self.repository.get_category(
            category_id
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
    # RECURRING BILLS
    # ------------------------

    def add_recurring_bill(
        self,
        transaction_type,
        description,
        merchant,
        amount,
        account_id,
        category_id,
        day_of_month
    ):
        if day_of_month < 1 or day_of_month > 31:
            raise ValueError(
                "Day of month must be between 1 and 31."
            )
        
        recurring_bill = RecurringBill(
            transaction_type=transaction_type,
            description=description,
            merchant=merchant,
            amount=amount,
            account_id=account_id,
            category_id=category_id,
            day_of_month=day_of_month,
            active=True,
            last_generated_month=None
        )

        return self.repository.add_recurring_bill(
            recurring_bill
        )

    def generate_recurring_transactions(self):

        today = date.today()

        current_month = today.strftime("%Y-%m")

        bills = self.repository.get_active_recurring_bills()

        for bill in bills:
            try:
                bill_day = min(
                    bill["day_of_month"],
                    calendar.monthrange(
                        today.year,
                        today.month
                    )[1]
                )
                if bill_day > today.day:
                    continue
                if bill["last_generated_month"] == current_month:
                    continue
                transaction_date = (
                    f"{today.year}-"
                    f"{today.month:02d}-"
                    f"{bill_day:02d}"
                )
                self.add_transaction(
                    transaction_type=bill["transaction_type"],
                    date=transaction_date,
                    description=bill["description"],
                    amount=bill["amount"],
                    merchant=bill["merchant"],
                    account_id=bill["account_id"],
                    category_id=bill["category_id"]
                )
                self.repository.update_recurring_bill_last_generated_month(
                    bill["id"],
                    current_month
                )

            except Exception as ex:
                print(
                    f"Failed to process recurring bill "
                    f"{bill['id']}: {ex}"
                )

    def get_active_recurring_bills(self):
        return self.repository.get_active_recurring_bills()

    def get_all_recurring_bills(self):
        return self.repository.get_all_recurring_bills()

    def enable_recurring_bill(self, bill_id):
        self.repository.enable_recurring_bill(bill_id)

    def disable_recurring_bill(self, bill_id):
        self.repository.disable_recurring_bill(bill_id)

    def delete_recurring_bill(self, bill_id):
        self.repository.delete_recurring_bill(bill_id)

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