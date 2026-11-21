import tkinter as tk
from tkinter import ttk, messagebox

from util.date_utils import parse_date
from ui.theme import apply_dark_theme


class TransactionTableView(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.parent = parent
        self.controller = controller

        apply_dark_theme(self)
        self.configure(style="Dark.TFrame")

        self.sort_reverse = True

        # ----------------------------------------
        # HEADER
        # ----------------------------------------

        header = ttk.Frame(self, style="Dark.TFrame")
        header.pack(fill="x", padx=10, pady=10)

        ttk.Label(
            header,
            text="All Transactions",
            font=("Arial", 16),
            style="Dark.TLabel"
        ).pack(side="left")

        ttk.Button(
            header,
            text="Back",
            command=self.go_back,
            style="Dark.TButton"
        ).pack(side="right")

        # ----------------------------------------
        # FILTER BAR
        # ----------------------------------------

        filter_frame = ttk.Frame(
            self,
            style="Dark.TFrame"
        )
        filter_frame.pack(
            fill="x",
            pady=5
        )

        ttk.Label(
            filter_frame,
            text="Filter:",
            style="Dark.TLabel"
        ).pack(
            side="left",
            padx=5
        )

        self.filter_entry = ttk.Entry(
            filter_frame,
            style="Dark.TEntry"
        )
        self.filter_entry.pack(
            side="left",
            padx=5
        )

        ttk.Button(
            filter_frame,
            text="Apply",
            command=self.apply_filter,
            style="Dark.TButton"
        ).pack(
            side="left",
            padx=5
        )

        ttk.Button(
            filter_frame,
            text="Clear",
            command=self.clear_filter,
            style="Dark.TButton"
        ).pack(
            side="left",
            padx=5
        )

        # ----------------------------------------
        # TABLE
        # ----------------------------------------

        table_frame = ttk.Frame(
            self,
            style="Dark.TFrame"
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        columns = (
            "id",
            "date",
            "type",
            "description",
            "merchant",
            "amount"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            style="Dark.Treeview"
        )

        self.tree.pack(
            fill="both",
            expand=True
        )

        self.tree.heading(
            "date",
            text="Date",
            command=lambda: self.sort_by("date")
        )

        self.tree.heading(
            "type",
            text="Type",
            command=lambda: self.sort_by("type")
        )

        self.tree.heading(
            "description",
            text="Description",
            command=lambda: self.sort_by("description")
        )

        self.tree.heading(
            "merchant",
            text="Merchant",
            command=lambda: self.sort_by("merchant")
        )

        self.tree.heading(
            "amount",
            text="Amount",
            command=lambda: self.sort_by("amount")
        )

        #
        # Hidden ID column
        #
        self.tree.heading("id", text="ID")

        self.tree.column(
            "id",
            width=0,
            stretch=False
        )

        self.tree.column(
            "date",
            width=120
        )

        self.tree.column(
            "type",
            width=120
        )

        self.tree.column(
            "description",
            width=250
        )

        self.tree.column(
            "merchant",
            width=180
        )

        self.tree.column(
            "amount",
            width=100
        )

        # ----------------------------------------
        # BUTTONS
        # ----------------------------------------

        button_frame = ttk.Frame(
            self,
            style="Dark.TFrame"
        )
        button_frame.pack(
            pady=10
        )

        ttk.Button(
            button_frame,
            text="Delete Selected",
            command=self.delete_selected,
            style="Dark.TButton"
        ).pack(
            side="left",
            padx=5
        )

        self.transactions = (
            self.controller.get_transactions()
        )

        self.populate_table()

    # ----------------------------------------
    # TABLE
    # ----------------------------------------

    def populate_table(self, filtered=None):

        for item in self.tree.get_children():
            self.tree.delete(item)

        data = (
            filtered
            if filtered is not None
            else self.transactions
        )

        data = sorted(
            data,
            key=lambda t: parse_date(t.date),
            reverse=self.sort_reverse
        )

        for tx in data:

            tag = tx.transaction_type.lower()

            self.tree.insert(
                "",
                "end",
                values=(
                    tx.id,
                    tx.date,
                    tx.transaction_type,
                    tx.description,
                    tx.merchant or "",
                    f"${tx.amount:.2f}"
                ),
                tags=(tag,)
            )

        self.tree.tag_configure(
            "deposit",
            foreground="#7CFC00"
        )

        self.tree.tag_configure(
            "withdrawal",
            foreground="#FFA500"
        )

        self.tree.tag_configure(
            "purchase",
            foreground="#FF5555"
        )

    # ----------------------------------------
    # HELPERS
    # ----------------------------------------

    def get_selected(self):

        selection = self.tree.selection()

        if not selection:
            return None

        return self.tree.item(
            selection[0]
        )["values"]

    # ----------------------------------------
    # DELETE
    # ----------------------------------------

    def delete_selected(self):

        row = self.get_selected()

        if not row:
            messagebox.showwarning(
                "No Selection",
                "Select a transaction first."
            )
            return

        tx_id = row[0]

        confirm = messagebox.askyesno(
            "Delete Transaction",
            "Are you sure?"
        )

        if not confirm:
            return

        self.controller.delete_transaction(
            tx_id
        )

        self.transactions = (
            self.controller.get_transactions()
        )

        self.populate_table()

    # ----------------------------------------
    # SORTING
    # ----------------------------------------

    def sort_by(self, column):

        if column == "amount":

            key_func = lambda t: t.amount

        elif column == "date":

            key_func = lambda t: parse_date(
                t.date
            )

        elif column == "type":

            key_func = lambda t: (
                t.transaction_type.lower()
            )

        elif column == "merchant":

            key_func = lambda t: (
                t.merchant or ""
            ).lower()

        else:

            key_func = lambda t: (
                getattr(
                    t,
                    column,
                    ""
                )
            ).lower()

        self.sort_reverse = (
            not self.sort_reverse
        )

        sorted_data = sorted(
            self.transactions,
            key=key_func,
            reverse=self.sort_reverse
        )

        self.populate_table(
            sorted_data
        )

    # ----------------------------------------
    # FILTERING
    # ----------------------------------------

    def apply_filter(self):

        text = (
            self.filter_entry
            .get()
            .lower()
            .strip()
        )

        if not text:

            self.populate_table()
            return

        filtered = [

            t

            for t in self.transactions

            if text in t.description.lower()
            or text in t.transaction_type.lower()
            or text in (t.merchant or "").lower()
        ]

        self.populate_table(filtered)

    def clear_filter(self):

        self.filter_entry.delete(
            0,
            tk.END
        )

        self.populate_table()

    # ----------------------------------------
    # NAVIGATION
    # ----------------------------------------

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