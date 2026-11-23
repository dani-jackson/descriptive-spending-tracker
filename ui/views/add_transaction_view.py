import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from tkcalendar import DateEntry
from datetime import date

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

        self.title_label = ttk.Label(
            header,
            text="Add Transaction",
            font=("Arial", 16),
            style="Dark.TLabel"
        )
        self.title_label.pack(side="left")

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

        ttk.Label(
            form,
            text="Date",
            style="Dark.TLabel"
        ).pack(anchor="w")

        self.date_entry = DateEntry(
            form,
            style="Dark.TEntry",
            date_pattern="yyyy-mm-dd"
        )
        self.date_entry.pack(
            fill="x",
            pady=(0, 10)
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

        self.NEW_CATEGORY_OPTION = "+ Add New Category..."

        self.category_dropdown = ttk.Combobox(
            form,
            textvariable=self.category_var,
            values=[
                *self.category_lookup.keys(),
                self.NEW_CATEGORY_OPTION
            ],
            style="Dark.TCombobox",
            state="readonly"
        )
        self.category_dropdown.pack(
            fill="x",
            pady=(0, 20)
        )
        self.category_dropdown.bind(
            "<<ComboboxSelected>>",
            self.on_category_selected
        )

        # --------------------------------------------------
        # RECURRING BILLS
        # --------------------------------------------------

        self.recurring_var = tk.BooleanVar(value=False)

        ttk.Checkbutton(
            form,
            text="Recurring Monthly Bill",
            variable=self.recurring_var
        ).pack(anchor="w", pady=(0, 10))

        # --------------------------------------------------
        # ACTIONS
        # --------------------------------------------------

        button_frame = ttk.Frame(
            form,
            style="Dark.TFrame"
        )
        button_frame.pack()

        self.save_button = ttk.Button(
            button_frame,
            text="Save Transaction",
            command=self.save_transaction,
            style="Dark.TButton"
        )
        self.save_button.pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Clear",
            command=self.clear_fields,
            style="Dark.TButton"
        ).pack(side="left", padx=5)

        self.status_label = ttk.Label(
            form,
            text="",
            style="Dark.TLabel"
        )
        self.status_label.pack(pady=(10, 0))

    # --------------------------------------------------
    # EDITING 
    # --------------------------------------------------
    
        editing_transaction = getattr(self.controller, "editing_transaction", None)
        if editing_transaction:
            self.load_transaction(editing_transaction)

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
        self.date_entry.set_date(date.today())
        self.desc_entry.delete(0, tk.END)
        self.merchant_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.type_var.set(Transaction.PURCHASE)
        self.account_var.set("")
        self.category_var.set("")
        self.recurring_var.set(False)
        self.editing_transaction = None
        self.controller.editing_transaction = None
        self.title_label.config(text="Add Transaction")
        self.save_button.config(text="Save Transaction")

    def on_category_selected(self, event=None):
        if self.category_var.get() != self.NEW_CATEGORY_OPTION:
            return
        category_name = simpledialog.askstring(
            "New Category",
            "Category name:"
        )
        if not category_name:
            self.category_var.set("")
            return
        category_name = category_name.strip()
        if not category_name:
            self.category_var.set("")
            return
        if category_name in self.category_lookup:
            self.category_var.set(category_name)
            messagebox.showinfo(
                "Category Exists",
                f'"{category_name}" already exists.'
            )
            return
        category_id = self.controller.add_category(
            category_name
        )
        self.category_lookup[category_name] = category_id
        self.category_dropdown["values"] = [
            *self.category_lookup.keys(),
            self.NEW_CATEGORY_OPTION
        ]
        self.category_var.set(category_name)

    def load_transaction(self, transaction):
        account_name = next(
            (
                name
                for name, account_id
                in self.account_lookup.items()
                if account_id == transaction.account_id
            ),
            ""
        )
        category_name = next(
            (
                name
                for name, category_id
                in self.category_lookup.items()
                if category_id == transaction.category_id
            ),
            ""
        )
        
        self.editing_transaction = transaction
        self.account_var.set(account_name)
        self.category_var.set(category_name)
        self.type_var.set(transaction.transaction_type)
        self.date_entry.set_date(transaction.date)
        self.desc_entry.delete(0, "end")
        self.desc_entry.insert(0, transaction.description)
        self.amount_entry.delete(0, "end")
        self.amount_entry.insert(0, str(transaction.amount))
        self.merchant_entry.delete(0, "end")
        self.merchant_entry.insert(0, transaction.merchant or "")
        self.title_label.config(text="Edit Transaction")
        self.save_button.config(text="Update Transaction")

    # --------------------------------------------------
    # SAVE
    # --------------------------------------------------

    def save_transaction(self):
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror(
                "Invalid Amount",
                "Please enter a valid amount."
            )
            return
        account_id = self.account_lookup.get(self.account_var.get())
        category_id = self.category_lookup.get(self.category_var.get())

        try:
            # Editing an existing transaction
            if self.editing_transaction is not None:
                self.editing_transaction.transaction_type = (self.type_var.get())
                self.editing_transaction.date = (self.date_entry.get())
                self.editing_transaction.description = (self.desc_entry.get())
                self.editing_transaction.amount = (amount)
                self.editing_transaction.merchant = (self.merchant_entry.get())
                self.editing_transaction.account_id = (account_id)
                self.editing_transaction.category_id = (category_id)
                self.controller.update_transaction(self.editing_transaction)
                self.editing_transaction = None
                self.controller.editing_transaction = None

                message = ("Transaction updated successfully.")
              

            else:
                self.controller.add_transaction(
                    transaction_type=self.type_var.get(),
                    date=self.date_entry.get(),
                    description=self.desc_entry.get(),
                    amount=amount,
                    merchant=self.merchant_entry.get(),
                    account_id=account_id,
                    category_id=category_id
                )

                message = ("Transaction added successfully.")

                if self.recurring_var.get():
                    self.controller.add_recurring_bill(
                        transaction_type=self.type_var.get(),
                        description=self.desc_entry.get(),
                        merchant=self.merchant_entry.get(),
                        amount=amount,
                        account_id=account_id,
                        category_id=category_id,
                        day_of_month=self.date_entry.get_date().day
                    )

                    message += " Recurring bill created."

            self.clear_fields()
            self.desc_entry.focus_set()
            self.status_label.config(
                text=message,
                style="Success.TLabel"
            )

            self.after(3000, lambda: self.status_label.config(text=""))

        except Exception as ex:
            messagebox.showerror("Error", str(ex))

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