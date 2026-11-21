import tkinter as tk

from storage.database_repository import DatabaseRepository

from controller import AppController
from ui.views.dashboard_view import DashboardView


def start_gui():

    root = tk.Tk()

    root.title("Budget Tracker")
    root.geometry("900x600")

    repository = DatabaseRepository()

    controller = AppController(
        root,
        repository
    )

    DashboardView(
        root,
        controller
    ).pack(fill="both", expand=True)

    root.mainloop()

    repository.close()