from tkinter import ttk

from ui.theme import apply_dark_theme
from ui.views.category_view import CategoryView


class DashboardView(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.parent = parent
        self.controller = controller

        apply_dark_theme(self)
        self.configure(style="Dark.TFrame")

        ttk.Label(
            self,
            text="Budget Tracker",
            font=("Arial", 18),
            style="Dark.TLabel"
        ).pack(pady=20)

        ttk.Label(
            self,
            text="Track transactions, budgets, and spending trends",
            style="Dark.TLabel"
        ).pack(pady=(0, 20))

        ttk.Button(
            self,
            text="Add Transaction",
            command=self.open_add,
            style="Dark.TButton"
        ).pack(pady=10)

        ttk.Button(
            self,
            text="View Transactions",
            command=self.open_table,
            style="Dark.TButton"
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Manage Accounts",
            command=self.open_accounts,
            style="Dark.TButton"
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Monthly Summary",
            command=self.open_summary,
            style="Dark.TButton"
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Spending Pie Chart",
            command=self.open_pie,
            style="Dark.TButton"
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Manage Budgets",
            command=self.open_budgets,
            style="Dark.TButton"
        ).pack(pady=10)

    def open_add(self):
        from ui.views.add_transaction_view import AddTransactionView
        self._swap(AddTransactionView)

    def open_accounts(self):
        from ui.views.account_view import AccountView
        self._swap(AccountView)

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
        self._swap(CategoryView)

    def _swap(self, view_class):

        for widget in self.parent.winfo_children():
            widget.destroy()

        view_class(
            self.parent,
            self.controller
        ).pack(
            fill="both",
            expand=True
        )