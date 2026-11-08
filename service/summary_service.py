class SummaryService:
    def __init__(self, account):
        self.account = account

    def monthly_totals(self):
        return self.account.monthly_category_totals()

    def monthly_percentages(self):
        return self.account.monthly_category_percentages()

    def monthly_budget_report(self):
        return self.account.monthly_budget_report()
