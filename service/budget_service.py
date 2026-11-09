class BudgetService:

    def __init__(self, repository):
        self.repository = repository

    def is_over_budget(self, category_id, spent):

        category = self.repository.get_category(category_id)

        if category is None:
            return False

        if category.monthly_limit is None:
            return False

        return spent > category.monthly_limit

    def remaining(self, category_id, spent):

        category = self.repository.get_category(category_id)

        if category is None:
            return None

        if category.monthly_limit is None:
            return None

        return category.monthly_limit - spent