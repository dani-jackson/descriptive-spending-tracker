import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from ui.theme import apply_dark_theme


class PieChartView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent

        apply_dark_theme(self)
        self.configure(style="Dark.TFrame")

        # -----------------------------
        # HEADER BAR (Title + Back)
        # -----------------------------
        header = ttk.Frame(self, style="Dark.TFrame")
        header.pack(fill="x", pady=10, padx=10)

        ttk.Label(
            header,
            text="Category Spending Pie Chart",
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
        # GET DATA
        # -----------------------------
        totals = controller.current_account.spending_by_category()

        if not totals:
            ttk.Label(self, text="No purchase data available", style="Dark.TLabel").pack(pady=20)
            return

        categories = list(totals.keys())
        amounts = list(totals.values())

        # -----------------------------
        # CREATE MATPLOTLIB FIGURE
        # -----------------------------
        fig = Figure(figsize=(6, 5), dpi=100, facecolor="#1e1e1e")
        ax = fig.add_subplot(111, facecolor="#1e1e1e")

        # Donut-style pie chart
        wedges, texts, autotexts = ax.pie(
            amounts,
            autopct="%1.1f%%",
            pctdistance=0.75,      # moves % labels outward
            startangle=90,
            wedgeprops=dict(width=0.4),  # donut effect
            textprops={"color": "white", "fontsize": 10}
        )

        # Legend instead of labels on the pie
        ax.legend(
            wedges,
            categories,
            title="Categories",
            loc="center left",
            bbox_to_anchor=(1, 0.5),
            labelcolor="white",
            facecolor="#1e1e1e",
            edgecolor="#1e1e1e"
        )

        # Keep circle shape
        ax.set_aspect("equal")

        # Improve spacing
        fig.tight_layout()

        # -----------------------------
        # EMBED IN TKINTER
        # -----------------------------
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    # -----------------------------
    # NAVIGATION
    # -----------------------------
    def go_back(self):
        from ui.views.dashboard_view import DashboardView
        for widget in self.parent.winfo_children():
            widget.destroy()
        DashboardView(self.parent, self.controller).pack(fill="both", expand=True)
