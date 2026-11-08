import tkinter as tk
from tkinter import ttk
from ui.theme import apply_dark_theme


class SummaryView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Dark.TFrame")
        self.controller = controller
        apply_dark_theme(self)
        self.configure(style="Dark.TFrame")

        # -----------------------------
        # HEADER BAR
        # -----------------------------
        header = ttk.Frame(self, style="Dark.TFrame")
        header.pack(fill="x", pady=10, padx=10)

        ttk.Label(
            header,
            text="Monthly Summary",
            font=("Arial", 16),
            style="Dark.TLabel"
        ).pack(side="left")

        ttk.Button(
            header,
            text="Back",
            style="Dark.TButton",
            command=self.go_back
        ).pack(side="right")

        # -----------------------------
        # FETCH SUMMARY DATA
        # -----------------------------
        totals = controller.summary_service.monthly_totals()
        percentages = controller.summary_service.monthly_percentages()
        budgets = controller.summary_service.monthly_budget_report()

        # -----------------------------
        # TEXT AREA
        # -----------------------------
        text_frame = ttk.Frame(self, style="Dark.TFrame")
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        text = tk.Text(
            text_frame,
            width=100,
            height=40,
            bg="#1e1e1e",
            fg="#ffffff",
            insertbackground="white",
            highlightthickness=0,
            borderwidth=0,
            font=("Consolas", 11)
        )
        text.pack(fill="both", expand=True)

        # -----------------------------
        # COLOR TAGS
        # -----------------------------
        text.tag_configure("over", foreground="#ff6b6b")      # red
        text.tag_configure("under", foreground="#7CFC00")     # green
        text.tag_configure("header", foreground="#87CEFA")    # light blue
        text.tag_configure("grid", foreground="#888888")      # gray grid lines

        if not totals:
            text.insert("end", "No transactions found.\n")
        else:
            for (year, month), cats in sorted(totals.items()):
                text.insert("end", f"\n===== {month}/{year} =====\n", "header")

                month_total = sum(abs(v) for v in cats.values())
                text.insert("end", f"Total spending: ${month_total:.2f}\n\n")

                # -----------------------------------------
                # CATEGORY ORDERING
                # -----------------------------------------
                special = ["Deposit", "Withdrawal"]
                regular = [c for c in cats.keys() if c not in special]
                regular.sort()
                ordered = regular + special

                # -----------------------------------------
                # TABLE HEADER
                # -----------------------------------------
                header_line = (
                    f"{'Category':<15} "
                    f"{'Spent':>10}   "
                    f"{'Budget':>10}   "
                    f"{'% of Total':>10}   "
                    f"{'Status':<20}"
                )
                text.insert("end", header_line + "\n", "header")
                text.insert("end", "-" * 75 + "\n", "grid")

                # -----------------------------------------
                # TABLE ROWS
                # -----------------------------------------
                for cat in ordered:
                    spent = abs(cats[cat])
                    pct = percentages[(year, month)].get(cat, 0)

                    # Deposits should not show a percentage
                    if cat == "Deposit":
                        pct_str = "—"
                    else:
                        pct_str = f"{pct:>5.1f}%"

                    budget_info = budgets[(year, month)].get(cat, {})
                    budget = budget_info.get("budget")
                    over = budget_info.get("over")
                    under = budget_info.get("under")

                    # Budget column
                    budget_str = "—" if budget is None else f"${budget:.2f}"

                    # Status column
                    if budget is None:
                        status = ""
                        tag = None
                    else:
                        if over > 0:
                            status = f"OVER by ${over:.2f}"
                            tag = "over"
                        elif under > 0:
                            status = f"under by ${under:.2f}"
                            tag = "under"
                        else:
                            status = "on budget"
                            tag = "under"

                    # Build row
                    line = (
                    f"{cat:<15} "
                    f"${spent:>9.2f}   "
                    f"{budget_str:>10}   "
                    f"{pct_str:>10}   "
                    f"{status:<20}"
)

                    if tag:
                        text.insert("end", line + "\n", tag)
                    else:
                        text.insert("end", line + "\n")

                text.insert("end", "\n")

        # -----------------------------
        # BACK BUTTON (BOTTOM)
        # -----------------------------
        back_frame = ttk.Frame(self, style="Dark.TFrame")
        back_frame.pack(pady=20)

        ttk.Button(
            back_frame,
            text="Back",
            style="Dark.TButton",
            command=self.go_back
        ).pack()

    def go_back(self):
        from ui.views.dashboard_view import DashboardView
        for widget in self.master.winfo_children():
            widget.destroy()
        DashboardView(self.master, self.controller).pack(fill="both", expand=True)
