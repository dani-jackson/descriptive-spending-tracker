import tkinter as tk

from controller import AppController
from storage.database_repository import DatabaseRepository

from ui.theme import apply_dark_theme
from ui.views.dashboard_view import DashboardView


def main():

    root = tk.Tk()

    root.title("Budget Tracker")
    root.geometry("1000x700")

    apply_dark_theme(root)

    repository = DatabaseRepository()

    controller = AppController(
        root,
        repository
    )

    DashboardView(
        root,
        controller
    ).pack(
        fill="both",
        expand=True
    )

    try:
        root.mainloop()
    finally:
        repository.close()


if __name__ == "__main__":
    main()
