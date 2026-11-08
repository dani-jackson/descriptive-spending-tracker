import tkinter as tk
from ui.controller import AppController
from ui.views.dashboard_view import DashboardView

def start_gui(account):
    root = tk.Tk()
    root.title("Budget Tracker")
    root.geometry("600x400")

    controller = AppController(root, account)

    DashboardView(root, controller).pack(fill="both", expand=True)

    root.mainloop()
