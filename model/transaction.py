from uuid import uuid4


class Transaction:
    def __init__(self, date, description, amount, id=None):
        self.id = id or uuid4().hex
        self.date = date
        self.description = description
        self.amount = float(amount)

    def amount_signed(self):
        raise NotImplementedError("Subclasses must implement amount_signed()")

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.__class__.__name__,
            "date": self.date,
            "description": self.description,
            "amount": self.amount
        }

    @staticmethod
    def from_dict(data):
        ttype = data["type"]
        date = data["date"]
        desc = data["description"]
        amount = data["amount"]
        id = data.get("id")

        if ttype == "Deposit":
            return Deposit(date, desc, amount, id=id)

        if ttype == "Withdrawal":
            return Withdrawal(date, desc, amount, id=id)

        if ttype == "Purchase":
            p = Purchase(
                date,
                desc,
                amount,
                category=data.get("category"),
                tax=data.get("tax", 0.087),
                fees=data.get("fees", 0),
                shipping=data.get("shipping", 0),
                use_total=data.get("use_total", False),
                id=id
            )

            if "total_cost" in data:
                p.total_cost = float(data["total_cost"])

            return p

        raise ValueError(f"Unknown transaction type: {ttype}")


class Deposit(Transaction):
    def __init__(self, date, description, amount, id=None):
        super().__init__(date, description, amount, id=id)

    def amount_signed(self):
        return self.amount


class Withdrawal(Transaction):
    def __init__(self, date, description, amount, id=None):
        super().__init__(date, description, amount, id=id)

    def amount_signed(self):
        return -self.amount


class Purchase(Transaction):
    def __init__(self, date, description, amount,
                 category=None, tax=0.087, fees=0, shipping=0,
                 use_total=False, id=None):

        super().__init__(date, description, amount, id=id)

        self.category = category
        self.tax = tax
        self.fees = fees
        self.shipping = shipping
        self.use_total = use_total

        if use_total:
            self.total_cost = float(amount)
        else:
            self.total_cost = float(amount) + (float(amount) * tax) + fees + shipping

    def amount_signed(self):
        return -self.total_cost

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "category": self.category,
            "tax": self.tax,
            "fees": self.fees,
            "shipping": self.shipping,
            "use_total": self.use_total,
            "total_cost": self.total_cost
        })
        return base
