class Account:

    def __init__(
        self,
        name,
        account_type="Other",
        id=None
    ):
        self.id = id
        self.name = name
        self.account_type = account_type

    def __repr__(self):
        return (
            f"Account("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"account_type='{self.account_type}'"
            f")"
        )