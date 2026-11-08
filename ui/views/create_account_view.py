import tkinter as tk
from tkinter import ttk, messagebox

from ui.theme import apply_dark_theme

# Subclass imports
from model.checking_account import CheckingAccount
from model.savings_account import SavingsAccount
from model.credit_card_account import CreditCardAccount


class CreateAccountView(ttk.Frame):
    def __init__(self, parent, controller, storage, filename):
        super().__init__(parent)
        self.controller = controller
        self.storage = storage
        self.filename = filename
        self.parent = parent

        apply_dark_theme(self)
        self.configure(style="Dark.TFrame")

        ttk.Label(
            self,
            text="Create New Account",
            font=("Arial", 18),
            style="Dark.TLabel"
        ).pack(pady=20)

        # ------------------------------
        # Account Type
        # ------------------------------
        ttk.Label(self, text="Account Type", style="Dark.TLabel").pack(pady=5)

        self.type_var = tk.StringVar(value="Checking")
        type_box = ttk.Combobox(
            self,
            textvariable=self.type_var,
            values=["Checking", "Savings", "Credit Card", "Cash", "Other"],
            state="readonly",
            style="Dark.TCombobox"
        )
        type_box.pack(pady=5)

        # When account type changes, update extra fields
        self.type_var.trace_add("write", self.update_extra_fields)

        # ------------------------------
        # Nickname
        # ------------------------------
        ttk.Label(self, text="Nickname", style="Dark.TLabel").pack(pady=5)
        self.nickname_entry = ttk.Entry(self, style="Dark.TEntry")
        self.nickname_entry.pack(pady=5)

        # ------------------------------
        # Dynamic extra fields (APR/APY)
        # ------------------------------
        self.extra_frame = ttk.Frame(self, style="Dark.TFrame")
        self.extra_frame.pack(pady=10)

        # Initialize with default (Checking)
        self.update_extra_fields()

        # ------------------------------
        # Buttons
        # ------------------------------
        bar = ttk.Frame(self, style="Dark.TFrame")
        bar.pack(pady=20)

        ttk.Button(bar, text="Create", command=self.create, style="Dark.TButton").pack(side="left", padx=10)
        ttk.Button(bar, text="Cancel", command=self.go_back, style="Dark.TButton").pack(side="left", padx=10)

    # ============================================================
    # Dynamic APR/APY fields
    # ============================================================
    def update_extra_fields(self, *args):
        # Clear previous widgets
        for w in self.extra_frame.winfo_children():
            w.destroy()

        acct_type = self.type_var.get()

        if acct_type == "Savings":
            ttk.Label(self.extra_frame, text="APY (%)", style="Dark.TLabel").pack(pady=5)
            self.apy_entry = ttk.Entry(self.extra_frame, style="Dark.TEntry")
            self.apy_entry.pack(pady=5)

        elif acct_type == "Credit Card":
            ttk.Label(self.extra_frame, text="APR (%)", style="Dark.TLabel").pack(pady=5)
            self.apr_entry = ttk.Entry(self.extra_frame, style="Dark.TEntry")
            self.apr_entry.pack(pady=5)

        # No extra fields for Checking, Cash, Other

    # ============================================================
    # Create account
    # ============================================================
    def create(self):
        nickname = self.nickname_entry.get().strip()
        acct_type = self.type_var.get()

        if not nickname:
            messagebox.showerror("Missing Nickname", "Please enter a nickname for the account.")
            return

        # ------------------------------
        # Create correct subclass
        # ------------------------------
        if acct_type == "Checking":
            acct = CheckingAccount(nickname)

        elif acct_type == "Savings":
            try:
                apy = float(self.apy_entry.get()) / 100
            except Exception:
                messagebox.showerror("Invalid APY", "Please enter a valid APY percentage.")
                return
            acct = SavingsAccount(nickname, apy=apy)

        elif acct_type == "Credit Card":
            try:
                apr = float(self.apr_entry.get()) / 100
            except Exception:
                messagebox.showerror("Invalid APR", "Please enter a valid APR percentage.")
                return
            acct = CreditCardAccount(nickname, apr=apr)

        elif acct_type == "Cash":
            # Behaves like checking
            acct = CheckingAccount(nickname)

        else:  # Other
            acct = CheckingAccount(nickname)

        # ------------------------------
        # Save to profile + storage
        # ------------------------------
        self.controller.profile.add_account(acct)
        self.storage.save(self.controller.profile, self.filename)

        self.go_back()

    # ============================================================
    # Navigation
    # ============================================================
    def go_back(self):
        from ui.views.account_selection_view import AccountSelectionView

        for w in self.parent.winfo_children():
            w.destroy()

        AccountSelectionView(self.parent, self.controller, self.storage, self.filename).pack(fill="both", expand=True)
