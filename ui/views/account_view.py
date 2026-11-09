import tkinter as tk
from tkinter import ttk, messagebox

from ui.theme import apply_dark_theme


class AccountView(ttk.Frame):

    ACCOUNT_TYPES = [
        "Checking",
        "Savings",
        "Credit Card",
        "Cash",
        "Investment",
        "Loan",
        "Other"
    ]

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.parent = parent
        self.controller = controller

        apply_dark_theme(self)
        self.configure(style="Dark.TFrame")

        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------

        header = ttk.Frame(self, style="Dark.TFrame")
        header.pack(fill="x", padx=10, pady=10)

        ttk.Label(
            header,
            text="Manage Accounts",
            font=("Arial", 16),
            style="Dark.TLabel"
        ).pack(side="left")

        ttk.Button(
            header,
            text="Back",
            command=self.go_back,
            style="Dark.TButton"
        ).pack(side="right")

        # -------------------------------------------------
        # TABLE
        # -------------------------------------------------

        self.tree = ttk.Treeview(
            self,
            columns=("id", "name", "type"),
            show="headings",
            height=12,
            style="Dark.Treeview"
        )

        self.tree.heading(
            "name",
            text="Account Name"
        )

        self.tree.heading(
            "type",
            text="Account Type"
        )

        self.tree.heading("id", text="ID")

        self.tree.column(
            "id",
            width=0,
            stretch=False
        )

        self.tree.column(
            "name",
            width=250
        )

        self.tree.column(
            "type",
            width=180
        )

        self.tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # -------------------------------------------------
        # FORM
        # -------------------------------------------------

        form = ttk.Frame(self, style="Dark.TFrame")
        form.pack(pady=10)

        ttk.Label(
            form,
            text="Account Name:",
            style="Dark.TLabel"
        ).grid(
            row=0,
            column=0,
            padx=5,
            pady=5
        )

        self.name_entry = ttk.Entry(
            form,
            width=30,
            style="Dark.TEntry"
        )

        self.name_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Label(
            form,
            text="Account Type:",
            style="Dark.TLabel"
        ).grid(
            row=1,
            column=0,
            padx=5,
            pady=5
        )

        self.account_type_var = tk.StringVar()

        self.account_type_combo = ttk.Combobox(
            form,
            textvariable=self.account_type_var,
            values=self.ACCOUNT_TYPES,
            state="readonly",
            style="Dark.TCombobox",
            width=27
        )

        self.account_type_combo.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        # -------------------------------------------------
        # ACTION BUTTONS
        # -------------------------------------------------

        button_frame = ttk.Frame(
            self,
            style="Dark.TFrame"
        )

        button_frame.pack(
            pady=10
        )

        ttk.Button(
            button_frame,
            text="Add Account",
            command=self.add_account,
            style="Dark.TButton"
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Update",
            command=self.update_account,
            style="Dark.TButton"
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Delete",
            command=self.delete_account,
            style="Danger.TButton"
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            button_frame,
            text="Load Selected",
            command=self.load_selected,
            style="Dark.TButton"
        ).pack(
            side="left",
            padx=5
        )

        self.refresh_table()

    # -------------------------------------------------
    # HELPERS
    # -------------------------------------------------

    def get_selected(self):

        selected = self.tree.selection()

        if not selected:
            return None

        return self.tree.item(
            selected[0]
        )["values"]

    def clear_form(self):

        self.name_entry.delete(
            0,
            tk.END
        )

        self.account_type_var.set("")

    # -------------------------------------------------
    # TABLE
    # -------------------------------------------------

    def refresh_table(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        for account in self.controller.get_accounts():

            self.tree.insert(
                "",
                "end",
                values=(
                    account.id,
                    account.name,
                    account.account_type
                )
            )

    # -------------------------------------------------
    # CREATE
    # -------------------------------------------------

    def add_account(self):

        name = self.name_entry.get().strip()

        account_type = (
            self.account_type_var.get().strip()
        )

        if not name:

            messagebox.showerror(
                "Missing Name",
                "Please enter an account name."
            )
            return

        if not account_type:

            messagebox.showerror(
                "Missing Type",
                "Please select an account type."
            )
            return

        try:

            self.controller.add_account(
                name,
                account_type
            )

            self.refresh_table()
            self.clear_form()

        except Exception as ex:

            messagebox.showerror(
                "Error",
                str(ex)
            )

    # -------------------------------------------------
    # UPDATE
    # -------------------------------------------------

    def update_account(self):

        row = self.get_selected()

        if not row:
            return

        account_id = row[0]

        name = self.name_entry.get().strip()

        account_type = (
            self.account_type_var.get().strip()
        )

        if not name or not account_type:
            return

        self.controller.update_account(
            account_id,
            name,
            account_type
        )

        self.refresh_table()

    # -------------------------------------------------
    # DELETE
    # -------------------------------------------------

    def delete_account(self):

        row = self.get_selected()

        if not row:
            return

        account_id = row[0]

        confirm = messagebox.askyesno(
            "Delete Account",
            "Delete selected account?"
        )

        if not confirm:
            return

        self.controller.delete_account(
            account_id
        )

        self.refresh_table()
        self.clear_form()

    # -------------------------------------------------
    # LOAD
    # -------------------------------------------------

    def load_selected(self):

        row = self.get_selected()

        if not row:
            return

        _, name, account_type = row

        self.clear_form()

        self.name_entry.insert(
            0,
            name
        )

        self.account_type_var.set(
            account_type
        )

    # -------------------------------------------------
    # NAVIGATION
    # -------------------------------------------------

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