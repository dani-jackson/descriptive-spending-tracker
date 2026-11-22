# model/recurring_bill.py

class RecurringBill:

    def __init__(
        self,
        transaction_type,
        description,
        merchant,
        amount,
        account_id,
        category_id,
        day_of_month,
        active=True,
        last_generated_month=None,
        id=None
    ):
        self.id = id
        self.transaction_type = transaction_type
        self.description = description
        self.merchant = merchant
        self.amount = amount
        self.account_id = account_id
        self.category_id = category_id
        self.day_of_month = day_of_month
        self.active = active
        self.last_generated_month = last_generated_month