class MonthlySummary:
    def __init__(self, year, month, total, by_category):
        self.year = year
        self.month = month
        self.total = total
        self.by_category = by_category  # dict: category -> amount
