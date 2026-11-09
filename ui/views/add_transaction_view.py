import tkinter as tk
from tkinter import ttk, messagebox

from model.transaction import Transaction
from ui.theme import apply_dark_theme


class AddTransactionView(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.parent = parent
        self.controller = controller

        apply_dark_theme(self)
        self.configure(style="Dark.TFrame")

        # --------------------------------------------------
        # HEADER
        # --------------------------------------------------

        header = ttk.Frame(self, style="Dark.TFrame")
        header.pack(fill="x", padx=10, pady=10)

        ttk.Label(
            header,
            text="Add Transaction",
            font=("Arial", 16),
            style="Dark.TLabel"
        ).pack(side="left")

        ttk.Button(
            header,
            text="Back",
            command=self.go_back,
            style="Dark.TButton"
        ).pack(side="right")

        # --------------------------------------------------
        # FORM
        # --------------------------------------------------

        form = ttk.Frame(self, style="Dark.TFrame")
        form.pack(fill="both", expand=True, padx=20, pady=20)

        self.type_var = tk.StringVar(
            value=Transaction.PURCHASE
        )

        ttk.Label(
            form,
            text="Transaction Type",
            style="Dark.TLabel"
        ).pack(anchor="w")

        self.type_dropdown = ttk.Combobox(
            form,
            textvariable=self.type_var,
            values=[
                Transaction.DEPOSIT,
                Transaction.WITHDRAWAL,
                Transaction.PURCHASE
            ],
            style="Dark.TCombobox",
            state="readonly"
        )
        self.type_dropdown.pack(fill="x", pady=(0, 10))

        self.date_entry = self._entry(
            form,
            "Date (YYYY-MM-DD)"
        )

        self.desc_entry = self._entry(
            form,
            "Description"
        )

        self.merchant_entry = self._entry(
            form,
            "Merchant"
        )

        self.amount_entry = self._entry(
            form,
            "Amount"
        )

        # --------------------------------------------------
        # ACCOUNTS
        # --------------------------------------------------

        ttk.Label(
            form,
            text="Account",
            style="Dark.TLabel"
        ).pack(anchor="w")

        accounts = controller.get_accounts()

        self.account_lookup = {
            account.name: account.id
            for account in accounts
        }

        self.account_var = tk.StringVar()

        self.account_dropdown = ttk.Combobox(
            form,
            textvariable=self.account_var,
            values=list(self.account_lookup.keys()),
            style="Dark.TCombobox",
            state="readonly"
        )

        self.account_dropdown.pack(
            fill="x",
            pady=(0, 10)
        )

        # --------------------------------------------------
        # CATEGORIES
        # --------------------------------------------------

        ttk.Label(
            form,
            text="Category",
            style="Dark.TLabel"
        ).pack(anchor="w")

        categories = controller.get_categories()

        self.category_lookup = {
            category.name: category.id
            for category in categories
        }

        self.category_var = tk.StringVar()

        self.category_dropdown = ttk.Combobox(
            form,
            textvariable=self.category_var,
            values=list(self.category_lookup.keys()),
            style="Dark.TCombobox",
            state="readonly"
        )

        self.category_dropdown.pack(
            fill="x",
            pady=(0, 20)
        )

        # --------------------------------------------------
        # ACTIONS
        # --------------------------------------------------

        button_frame = ttk.Frame(
            form,
            style="Dark.TFrame"
        )
        button_frame.pack()

        ttk.Button(
            button_frame,
            text="Save Transaction",
            command=self.save_transaction,
            style="Dark.TButton"
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_fields,
            style="Dark.TButton"
        ).pack(side="left", padx=5)

    # --------------------------------------------------
    # HELPERS
    # --------------------------------------------------

    def _entry(self, parent, label):

        ttk.Label(
            parent,
            text=label,
            style="Dark.TLabel"
        ).pack(anchor="w")

        entry = ttk.Entry(
            parent,
            style="Dark.TEntry"
        )

        entry.pack(
            fill="x",
            pady=(0, 10)
        )

        return entry

    def clear_fields(self):

        self.date_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.merchant_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

        self.type_var.set(
            Transaction.PURCHASE
        )

        self.account_var.set("")
        self.category_var.set("")

    # --------------------------------------------------
    # SAVE
    # --------------------------------------------------

    def save_transaction(self):

        try:
            amount = float(
                self.amount_entry.get()
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Amount",
                "Please enter a valid amount."
            )

            return

        account_id = self.account_lookup.get(
            self.account_var.get()
        )

        category_id = self.category_lookup.get(
            self.category_var.get()
        )

        try:

            self.controller.add_transaction(
                transaction_type=self.type_var.get(),
                date=self.date_entry.get(),
                description=self.desc_entry.get(),
                amount=amount,
                merchant=self.merchant_entry.get(),
                account_id=account_id,
                category_id=category_id
            )

            messagebox.showinfo(
                "Success",
                "Transaction added successfully."
            )

            self.clear_fields()

        except Exception as ex:

            messagebox.showerror(
                "Error",
                str(ex)
            )

    # --------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------

    def go_back(self):

        from ui.views.dashboard_view import DashboardView

        for widget in self.parent.winfo_children():
            widget.destroy()

        DashboardView(
            self.parent,
            self.controller
        ).pack(
            fill="both",
            expand=True
        )