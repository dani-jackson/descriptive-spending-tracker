class BudgetService:
    def __init__(self, account):
        self.account = account

    def is_over_budget(self, category, spent):
        limit = self.account.get_budget(category)
        return limit is not None and spent > limit

    def remaining(self, category, spent):
        limit = self.account.get_budget(category)
        if limit is None:
            return None
        return limit - spent
