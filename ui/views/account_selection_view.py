from tkinter import ttk
from ui.theme import apply_dark_theme

class AccountSelectionView(ttk.Frame):
    def __init__(self, parent, controller, storage, filename):
        super().__init__(parent)
        self.controller = controller
        self.storage = storage
        self.filename = filename
        self.parent = parent

        apply_dark_theme(self)
        self.configure(style="Dark.TFrame")

        ttk.Label(self, text="Select an Account", font=("Arial", 18), style="Dark.TLabel").pack(pady=20)

        if not controller.profile.accounts:
            ttk.Label(self, text="No accounts found. Create one to begin.", style="Dark.TLabel").pack(pady=10)
            ttk.Button(self, text="Create Account", command=self.open_create, style="Dark.TButton").pack(pady=20)
            return

        for acct in controller.profile.accounts:
            text = f"{acct.acct_type} — {acct.nickname or 'Unnamed'}"
            ttk.Button(
                self,
                text=text,
                command=lambda a=acct: self.open_account(a),
                style="Dark.TButton"
            ).pack(pady=5, fill="both", padx=40)

        ttk.Button(self, text="Create New Account", command=self.open_create, style="Dark.TButton").pack(pady=20)

    def open_account(self, account):
        from ui.views.dashboard_view import DashboardView
        self.controller.select_account(account)

        for w in self.parent.winfo_children():
            w.destroy()

        DashboardView(self.parent, self.controller).pack(fill="both", expand=True)

    def open_create(self):
        from ui.views.create_account_view import CreateAccountView

        for w in self.parent.winfo_children():
            w.destroy()

        CreateAccountView(self.parent, self.controller, self.storage, self.filename).pack(fill="both", expand=True)
