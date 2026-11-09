import tkinter as tk
from tkinter import ttk
from datetime import datetime

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from ui.theme import apply_dark_theme


class PieChartView(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.parent = parent
        self.controller = controller

        apply_dark_theme(self)
        self.configure(style="Dark.TFrame")

        # -------------------------------------
        # HEADER
        # -------------------------------------

        header = ttk.Frame(
            self,
            style="Dark.TFrame"
        )
        header.pack(
            fill="x",
            pady=10,
            padx=10
        )

        ttk.Label(
            header,
            text="Spending by Category",
            font=("Arial", 16),
            style="Dark.TLabel"
        ).pack(side="left")

        ttk.Button(
            header,
            text="Back",
            command=self.go_back,
            style="Dark.TButton"
        ).pack(side="right")

        # -------------------------------------
        # DATA
        # -------------------------------------

        today = datetime.now()

        totals = controller.get_monthly_totals(
            today.year,
            today.month
        )

        if not totals:

            ttk.Label(
                self,
                text="No spending data available for this month.",
                style="Dark.TLabel"
            ).pack(
                pady=20
            )

            return

        categories = list(totals.keys())
        amounts = list(totals.values())

        # -------------------------------------
        # FIGURE
        # -------------------------------------

        fig = Figure(
            figsize=(7, 5),
            dpi=100,
            facecolor="#1e1e1e"
        )

        ax = fig.add_subplot(
            111,
            facecolor="#1e1e1e"
        )

        wedges, texts, autotexts = ax.pie(
            amounts,
            autopct="%1.1f%%",
            pctdistance=0.75,
            startangle=90,
            wedgeprops=dict(width=0.4),
            textprops={
                "color": "white",
                "fontsize": 10
            }
        )

        ax.legend(
            wedges,
            categories,
            title="Categories",
            loc="center left",
            bbox_to_anchor=(1, 0.5)
        )

        ax.set_aspect("equal")

        fig.tight_layout()

        # -------------------------------------
        # EMBED CHART
        # -------------------------------------

        canvas = FigureCanvasTkAgg(
            fig,
            master=self
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

    # -------------------------------------
    # NAVIGATION
    # -------------------------------------

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
