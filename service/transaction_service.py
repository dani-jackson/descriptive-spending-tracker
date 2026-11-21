from model.transaction import Transaction


class TransactionService:

    def __init__(self, repository):
        self.repository = repository

    def create_transaction(
        self,
        transaction_type,
        date,
        description,
        amount,
        merchant=None,
        account_id=None,
        category_id=None
    ):

        transaction = Transaction(
            transaction_type=transaction_type,
            date=date,
            description=description,
            amount=amount,
            merchant=merchant,
            account_id=account_id,
            category_id=category_id
        )

        self.repository.add_transaction(
            transaction
        )

        return transaction