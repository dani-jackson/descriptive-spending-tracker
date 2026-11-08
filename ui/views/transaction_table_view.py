import tkinter as tk
from tkinter import ttk
from util.date_utils import parse_date
from ui.theme import apply_dark_theme


class TransactionTableView(ttk.Frame):
    """
    TransactionTableView
    --------------------
    Displays all transactions in a sortable, filterable table.

    Features:
        • Dark‑mode styling
        • Header bar with Back button
        • Filter bar (text search)
        • Sortable columns
        • Hidden transaction ID column
        • Edit / Delete using unique transaction IDs
    """

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent

        apply_dark_theme(self)
        self.configure(style="Dark.TFrame")

        # ============================================================
        # HEADER BAR (Title + Back)
        # ============================================================
        header = ttk.Frame(self, style="Dark.TFrame")
        header.pack(fill="x", pady=10, padx=10)

        ttk.Label(
            header,
            text="All Transactions",
            font=("Arial", 16),
            style="Dark.TLabel"
        ).pack(side="left")

        ttk.Button(
            header,
            text="Back",
            style="Dark.TButton",
            command=self.go_back
        ).pack(side="right")

        # ============================================================
        # FILTER BAR
        # ============================================================
        filter_frame = ttk.Frame(self, style="Dark.TFrame")
        filter_frame.pack(pady=5)

        ttk.Label(filter_frame, text="Filter:", style="Dark.TLabel").pack(side="left", padx=5)

        self.filter_entry = ttk.Entry(filter_frame, style="Dark.TEntry")
        self.filter_entry.pack(side="left", padx=5)

        ttk.Button(
            filter_frame,
            text="Apply",
            command=self.apply_filter,
            style="Dark.TButton"
        ).pack(side="left", padx=5)

        ttk.Button(
            filter_frame,
            text="Clear",
            command=self.clear_filter,
            style="Dark.TButton"
        ).pack(side="left", padx=5)

        # ============================================================
        # TREEVIEW (TABLE)
        # ============================================================
        tree_frame = ttk.Frame(self, style="Dark.TFrame")
        tree_frame.pack(fill="x", pady=10)

        # NOTE: "id" is a hidden column used for reliable edit/delete
        columns = ("id", "date", "type", "description", "amount", "category")

        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=15,
            style="Dark.Treeview"
        )
        self.tree.pack(fill="x")

        # Headings (user‑visible)
        self.tree.heading("date", text="Date", command=lambda: self.sort_by("date"))
        self.tree.heading("type", text="Type", command=lambda: self.sort_by("type"))
        self.tree.heading("description", text="Description", command=lambda: self.sort_by("description"))
        self.tree.heading("amount", text="Amount", command=lambda: self.sort_by("amount"))
        self.tree.heading("category", text="Category", command=lambda: self.sort_by("category"))

        # Hidden ID column
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=0, stretch=False)

        # Column widths
        self.tree.column("date", width=100)
        self.tree.column("type", width=80)
        self.tree.column("description", width=200)
        self.tree.column("amount", width=100)
        self.tree.column("category", width=120)

        # Data source
        self.transactions = controller.current_account.transactions
        self.sort_reverse = True

        self.populate_table()

        # ============================================================
        # EDIT / DELETE BUTTONS
        # ============================================================
        btn_frame = ttk.Frame(self, style="Dark.TFrame")
        btn_frame.pack(pady=10, fill="x")

        left_buttons = ttk.Frame(btn_frame, style="Dark.TFrame")
        left_buttons.pack(side="left")

        ttk.Button(
            left_buttons,
            text="Edit",
            style="Dark.TButton",
            command=self.edit_selected
        ).pack(side="left", padx=5)

        ttk.Button(
            left_buttons,
            text="Delete",
            style="Dark.TButton",
            command=self.delete_selected
        ).pack(side="left", padx=5)

    # ============================================================
    # TABLE POPULATION
    # ============================================================
    def populate_table(self, filtered=None):
        """Populate the table with all or filtered transactions."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        data = filtered if filtered is not None else self.transactions

        data_sorted = sorted(
            data,
            key=lambda t: parse_date(t.date),
            reverse=self.sort_reverse
        )

        for t in data_sorted:
            if t.__class__.__name__ == "Deposit":
                tag = "deposit"
            elif t.__class__.__name__ == "Withdrawal":
                tag = "withdrawal"
            elif t.__class__.__name__ == "Purchase":
                tag = "purchase"
            else:
                tag = "other"

            display_amount = getattr(t, "total_cost", t.amount)

            self.tree.insert(
                "",
                "end",
                values=(
                    getattr(t, "id", ""),          # hidden ID
                    t.date,
                    t.__class__.__name__,
                    t.description,
                    f"${display_amount:.2f}",
                    getattr(t, "category", "")
                ),
                tags=(tag,)
            )

        # Color coding by type
        self.tree.tag_configure("deposit", foreground="#7CFC00")
        self.tree.tag_configure("withdrawal", foreground="#FFA500")
        self.tree.tag_configure("purchase", foreground="#FF5555")
        self.tree.tag_configure("other", foreground="#AAAAAA")

    # ============================================================
    # SELECTION HELPERS
    # ============================================================
    def get_selected(self):
        """Return the values tuple of the selected row, or None."""
        sel = self.tree.selection()
        if not sel:
            return None
        return self.tree.item(sel[0])["values"]

    # ============================================================
    # DELETE (ID‑BASED)
    # ============================================================
    def delete_selected(self):
        """Delete the selected transaction using its unique ID."""
        row = self.get_selected()
        if not row:
            return

        tx_id = row[0]  # hidden ID column

        for tx in self.controller.current_account.transactions:
            if getattr(tx, "id", None) == tx_id:
                self.controller.current_account.transactions.remove(tx)
                break

        self.controller.storage.save(
            self.controller.profile,
            self.controller.filename
        )
        self.populate_table()

    # ============================================================
    # EDIT (ID‑BASED)
    # ============================================================
    def edit_selected(self):
        """Open AddTransactionView in edit mode for the selected transaction."""
        row = self.get_selected()
        if not row:
            return

        tx_id, date, tx_type, desc, amount_str, category = row
        amount = float(amount_str.replace("$", ""))

        # Find the actual transaction object by ID
        target = None
        for tx in self.controller.current_account.transactions:
            if getattr(tx, "id", None) == tx_id:
                target = tx
                break

        if not target:
            return

        self.controller.editing_transaction = {
            "id": target.id,
            "date": target.date,
            "type": target.__class__.__name__,
            "description": target.description,
            "amount": float(getattr(target, "total_cost", target.amount)),
            "category": getattr(target, "category", "")
        }

        from ui.views.add_transaction_view import AddTransactionView
        for w in self.parent.winfo_children():
            w.destroy()
        AddTransactionView(self.parent, self.controller, edit_mode=True).pack(fill="both", expand=True)

    # ============================================================
    # SORTING / FILTERING
    # ============================================================
    def sort_by(self, column):
        """Sort transactions by the given column."""
        if column == "amount":
            key_func = lambda t: getattr(t, "total_cost", t.amount)
        elif column == "date":
            key_func = lambda t: parse_date(t.date)
        else:
            key_func = lambda t: str(getattr(t, column, "")).lower()

        self.sort_reverse = not self.sort_reverse
        sorted_data = sorted(self.transactions, key=key_func, reverse=self.sort_reverse)
        self.populate_table(sorted_data)

    def apply_filter(self):
        """Filter transactions by text in description, type, or category."""
        text = self.filter_entry.get().lower().strip()

        if not text:
            self.populate_table()
            return

        filtered = [
            t for t in self.transactions
            if text in t.description.lower()
            or text in t.__class__.__name__.lower()
            or text in getattr(t, "category", "").lower()
        ]

        self.populate_table(filtered)

    def clear_filter(self):
        """Clear filter and show all transactions."""
        self.filter_entry.delete(0, tk.END)
        self.populate_table()

    # ============================================================
    # NAVIGATION
    # ============================================================
    def go_back(self):
        """Return to the dashboard view."""
        from ui.views.dashboard_view import DashboardView
        for w in self.parent.winfo_children():
            w.destroy()
        DashboardView(self.parent, self.controller).pack(fill="both", expand=True)
