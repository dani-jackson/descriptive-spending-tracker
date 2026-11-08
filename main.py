import tkinter as tk
from controller import AppController
from storage.file_storage import FileStorage
from ui.views.account_selection_view import AccountSelectionView

FILENAME = "accounts.json"

root = tk.Tk()
root.title("Budget Tracker")
root.geometry("800x600")

storage = FileStorage()

try:
    profile = storage.load(FILENAME)
except:
    from model.user_profile import UserProfile
    profile = UserProfile()

controller = AppController(root, profile, storage, FILENAME)

AccountSelectionView(root, controller, storage, FILENAME).pack(fill="both", expand=True)

root.mainloop()
