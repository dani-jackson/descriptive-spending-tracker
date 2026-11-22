import tkinter as tk
from tkinter import ttk, messagebox

from ui.theme import apply_dark_theme

class RecurringBillsView(ttk.Frame):

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
            text="Recurring Bills",
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
    # TREE VIEW
    # --------------------------------------------------
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
            "description",
            "amount",
            "day",
            "active"
        )

        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            style="Dark.Treeview"
        )

        self.tree.heading(
            "description",
            text="Description"
        )

        self.tree.heading(
            "amount",
            text="Amount"
        )

        self.tree.heading(
            "day",
            text="Day"
        )

        self.tree.heading(
            "active",
            text="Active"
        )

        self.tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    # --------------------------------------------------
    # BUTTONS
    # --------------------------------------------------

        buttons = ttk.Frame(self, style="Dark.TFrame")
        buttons.pack(pady=10)

        ttk.Button(
            buttons,
            text="Enable",
            command=self.enable_selected,
            style="Dark.TButton"
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons,
            text="Disable",
            command=self.disable_selected,
            style="Dark.TButton"
        ).pack(side="left", padx=5)

        ttk.Button(
            buttons,
            text="Delete",
            command=self.delete_selected,
            style="Dark.TButton"
        ).pack(side="left", padx=5)

    # --------------------------------------------------
    # REFRESH METHOD
    # --------------------------------------------------

    def refresh(self):
        self.tree.delete(
            *self.tree.get_children()
        )
        bills = self.controller.get_all_recurring_bills()
        for bill in bills:
            self.tree.insert(
                "",
                "end",
                iid=bill["id"],
                values=(
                    bill["description"],
                    f"${bill['amount']:.2f}",
                    bill["day_of_month"],
                    "Yes" if bill["active"] else "No"
                )
            )

    # --------------------------------------------------
    # MAGAGEMENT METHODS
    # --------------------------------------------------

    def enable_selected(self):
        bill_id = self.selected_bill_id()
        if bill_id is None:
            return
        self.controller.enable_recurring_bill(
            bill_id
        )
        self.refresh()

    def disable_selected(self):
        bill_id = self.selected_bill_id()
        if bill_id is None:
            return
        self.controller.disable_recurring_bill(
            bill_id
        )
        self.refresh()

    def delete_selected(self):
        bill_id = self.selected_bill_id()
        if bill_id is None:
            return
        confirmed = messagebox.askyesno(
            "Delete",
            "Delete this recurring bill?"
        )
        if not confirmed:
            return
        self.controller.delete_recurring_bill(
            bill_id
        )
        self.refresh()

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