from uuid import uuid4


class Transaction:

    DEPOSIT = "Deposit"
    WITHDRAWAL = "Withdrawal"
    PURCHASE = "Purchase"

    VALID_TYPES = {
        DEPOSIT,
        WITHDRAWAL,
        PURCHASE
    }

    def __init__(
        self,
        transaction_type,
        date,
        description,
        amount,
        merchant=None,
        account_id=None,
        category_id=None,
        id=None
    ):
        if transaction_type not in self.VALID_TYPES:
            raise ValueError(
                f"Invalid transaction type: {transaction_type}"
            )

        self.id = id or uuid4().hex

        self.transaction_type = transaction_type
        self.date = date
        self.description = description
        self.amount = float(amount)

        self.merchant = merchant
        self.account_id = account_id
        self.category_id = category_id


    @property
    def signed_amount(self):

        if self.transaction_type == self.DEPOSIT:
            return self.amount

        return -self.amount