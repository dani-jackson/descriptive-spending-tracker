class Category:

    def __init__(
        self,
        name,
        monthly_limit=None,
        id=None
    ):
        self.id = id
        self.name = name
        self.monthly_limit = monthly_limit

    def __repr__(self):
        return (
            f"Category("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"monthly_limit={self.monthly_limit}"
            f")"
        )