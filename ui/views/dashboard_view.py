from tkinter import ttk
from ui.theme import apply_dark_theme
from ui.views.summary_view import SummaryView
from ui.views.budget_view import BudgetView

class DashboardView(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent

        apply_dark_theme(self)
        self.configure(style="Dark.TFrame")

        ttk.Label(self, text=f"{controller.current_account.acct_type} — {controller.current_account.nickname}",
                  font=("Arial", 18), style="Dark.TLabel").pack(pady=20)

        ttk.Button(self, text="Add Transaction", command=self.open_add, style="Dark.TButton").pack(pady=10)
        ttk.Button(self, text="View All Transactions", command=self.open_table, style="Dark.TButton").pack(pady=10)
        ttk.Button(self, text="Monthly Summary", command=self.open_summary, style="Dark.TButton").pack(pady=10)
        ttk.Button(self, text="Spending Pie Chart", command=self.open_pie, style="Dark.TButton").pack(pady=10)
        ttk.Button(self, text="Set Budgets", style="Dark.TButton", command=self.open_budgets).pack(pady=10)

        ttk.Button(self, text="Switch Account", command=self.switch_account, style="Dark.TButton").pack(pady=30)

    def open_add(self):
        from ui.views.add_transaction_view import AddTransactionView
        self._swap(AddTransactionView)

    def open_table(self):
        from ui.views.transaction_table_view import TransactionTableView
        self._swap(TransactionTableView)

    def open_summary(self):
        from ui.views.summary_view import SummaryView
        self._swap(SummaryView)

    def open_pie(self):
        from ui.views.pie_chart_view import PieChartView
        self._swap(PieChartView)

    def open_budgets(self):
        self._swap(BudgetView)

    def switch_account(self):
        from ui.views.account_selection_view import AccountSelectionView
        self._swap(AccountSelectionView, extra_args=(self.controller,))

    def _swap(self, view_class, extra_args=()):
        for w in self.parent.winfo_children():
            w.destroy()
        view_class(self.parent, self.controller, *extra_args).pack(fill="both", expand=True)
