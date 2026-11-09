class SummaryService:

    def __init__(self, repository):
        self.repository = repository

    def monthly_totals(self, year, month):

        return self.repository.get_spending_by_category(
            year,
            month
        )

    def monthly_total_spending(self, year, month):

        return self.repository.get_total_spending_for_month(
            year,
            month
        )

    def monthly_percentages(self, year, month):

        totals = self.repository.get_spending_by_category(
            year,
            month
        )

        grand_total = sum(totals.values())

        if grand_total == 0:
            return {}

        return {
            category:
                round(amount / grand_total * 100, 1)
            for category, amount in totals.items()
        }
