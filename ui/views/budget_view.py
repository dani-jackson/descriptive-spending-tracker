import tkinter as tk
from tkinter import ttk

class BudgetView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style="Dark.TFrame")
        self.controller = controller
        self.account = controller.current_account

        # -----------------------------
        # HEADER BAR (Title + Back)
        # -----------------------------
        header = ttk.Frame(self, style="Dark.TFrame")
        header.pack(fill="x", pady=10, padx=10)

        ttk.Label(
            header,
            text="Category Budgets",
            font=("Arial", 16),
            style="Dark.TLabel"
        ).pack(side="left")

        ttk.Button(
            header,
            text="Back",
            style="Dark.TButton",
            command=self.go_back
        ).pack(side="right")


        # Table of budgets
        self.tree = ttk.Treeview(self, columns=("Category", "Budget"), show="headings", height=10, style="Dark.Treeview")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Budget", text="Budget ($)")
        self.tree.pack(pady=10)

        self.refresh_table()

       # Inputs
        form = ttk.Frame(self, style="Dark.TFrame")
        form.pack(pady=10)

        # Category label + entry
        ttk.Label(form, text="Category:", style="Dark.TLabel").grid(row=0, column=0, padx=5, pady=5)
       # Dropdown of categories
        self.cat_entry = ttk.Combobox(
            form,
            values=self.account.all_categories(),
            state="readonly",
            style="Dark.TCombobox"
        )
        self.cat_entry.grid(row=0, column=1, padx=5)

        # Budget label + entry
        ttk.Label(form, text="Budget:", style="Dark.TLabel").grid(row=1, column=0, padx=5, pady=5)
        self.budget_entry = ttk.Entry(form, style="Dark.TEntry")
        self.budget_entry.grid(row=1, column=1, padx=5, pady=5)


        ttk.Button(form, text="Save Budget", style="Dark.TButton", command=self.save_budget).grid(row=2, column=0, columnspan=2, pady=10)
        btn_frame = ttk.Frame(self, style="Dark.TFrame")
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Edit", style="Dark.TButton", command=self.edit_budget).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete", style="Dark.TButton", command=self.delete_budget).pack(side="left", padx=5)


    def get_selected(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return self.tree.item(sel[0])["values"]
    
    def delete_budget(self):
        row = self.get_selected()
        if not row:
            return
        cat = row[0]
        del self.account.budgets[cat]
        self.controller.storage.save(self.controller.profile, self.controller.filename)
        self.refresh_table()

    def edit_budget(self):
        row = self.get_selected()
        if not row:
            return
        cat, amount = row
        self.cat_entry.delete(0, "end")
        self.cat_entry.insert(0, cat)
        self.budget_entry.delete(0, "end")
        self.budget_entry.insert(0, amount)


    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for cat, amount in self.account.budgets.items():
            if amount is None:
                amount = 0.0
            self.tree.insert("", "end", values=(cat, f"{amount:.2f}"))

    def save_budget(self):
        cat = self.cat_entry.get().strip()
        try:
            amount = float(self.budget_entry.get())
        except ValueError:
            return  # You can add a popup later

        self.account.budgets[cat] = amount
        self.controller.storage.save(self.controller.profile, self.controller.filename)
        self.refresh_table()

        self.cat_entry.delete(0, "end")
        self.budget_entry.delete(0, "end")

    def go_back(self):
        from ui.views.dashboard_view import DashboardView
        for widget in self.master.winfo_children():
            widget.destroy()
        DashboardView(self.master, self.controller).pack(fill="both", expand=True)
