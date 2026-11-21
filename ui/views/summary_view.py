import tkinter as tk
from tkinter import ttk
from datetime import datetime

from ui.theme import apply_dark_theme


class SummaryView(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.parent = parent
        self.controller = controller

        apply_dark_theme(self)
        self.configure(style="Dark.TFrame")

        # ------------------------------------
        # HEADER
        # ------------------------------------

        header = ttk.Frame(
            self,
            style="Dark.TFrame"
        )

        header.pack(
            fill="x",
            padx=10,
            pady=10
        )

        ttk.Label(
            header,
            text="Monthly Summary",
            font=("Arial", 16),
            style="Dark.TLabel"
        ).pack(side="left")

        ttk.Button(
            header,
            text="Back",
            command=self.go_back,
            style="Dark.TButton"
        ).pack(side="right")

        # ------------------------------------
        # GET DATA
        # ------------------------------------

        today = datetime.now()

        totals = controller.get_monthly_totals(
            today.year,
            today.month
        )

        percentages = controller.get_monthly_percentages(
            today.year,
            today.month
        )

        categories = controller.get_categories()

        budget_lookup = {
            c.name: c.monthly_limit
            for c in categories
        }

        total_spending = sum(
            totals.values()
        )

        # ------------------------------------
        # TEXT AREA
        # ------------------------------------

        text = tk.Text(
            self,
            bg="#1e1e1e",
            fg="white",
            insertbackground="white",
            font=("Consolas", 11),
            borderwidth=0,
            highlightthickness=0
        )

        text.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        text.tag_configure(
            "header",
            foreground="#87CEFA"
        )

        text.tag_configure(
            "over",
            foreground="#ff6b6b"
        )

        text.tag_configure(
            "under",
            foreground="#7CFC00"
        )

        if not totals:

            text.insert(
                "end",
                "No spending data found.\n"
            )

            text.config(state="disabled")
            return

        text.insert(
            "end",
            f"{today.strftime('%B %Y')}\n\n",
            "header"
        )

        text.insert(
            "end",
            f"Total Spending: ${total_spending:.2f}\n\n"
        )

        header_line = (
            f"{'Category':<20}"
            f"{'Spent':>12}"
            f"{'Budget':>12}"
            f"{'% Total':>12}"
            f"{'Status':>15}"
        )

        text.insert(
            "end",
            header_line + "\n",
            "header"
        )

        text.insert(
            "end",
            "-" * 75 + "\n"
        )

        for category in sorted(totals.keys()):

            spent = totals[category]

            pct = percentages.get(
                category,
                0
            )

            budget = budget_lookup.get(
                category
            )

            budget_str = (
                f"${budget:.2f}"
                if budget is not None
                else "-"
            )

            status = ""

            tag = None

            if budget is not None:

                if spent > budget:

                    status = (
                        f"OVER ${spent - budget:.2f}"
                    )

                    tag = "over"

                else:

                    status = (
                        f"${budget - spent:.2f} left"
                    )

                    tag = "under"

            line = (
                f"{category:<20}"
                f"${spent:>11.2f}"
                f"{budget_str:>12}"
                f"{pct:>11.1f}%"
                f"{status:>15}"
            )

            if tag:

                text.insert(
                    "end",
                    line + "\n",
                    tag
                )

            else:

                text.insert(
                    "end",
                    line + "\n"
                )

        text.config(
            state="disabled"
        )

        # ------------------------------------
        # BACK BUTTON
        # ------------------------------------

        bottom = ttk.Frame(
            self,
            style="Dark.TFrame"
        )

        bottom.pack(
            pady=10
        )

        ttk.Button(
            bottom,
            text="Back",
            command=self.go_back,
            style="Dark.TButton"
        ).pack()

    # ------------------------------------
    # NAVIGATION
    # ------------------------------------

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