import tkinter as tk
from tkinter import ttk, messagebox

from ui.theme import apply_dark_theme


class CategoryView(ttk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        self.parent = parent
        self.controller = controller

        apply_dark_theme(self)
        self.configure(style="Dark.TFrame")

        # -----------------------------------
        # HEADER
        # -----------------------------------

        header = ttk.Frame(self, style="Dark.TFrame")
        header.pack(fill="x", padx=10, pady=10)

        ttk.Label(
            header,
            text="Manage Categories",
            font=("Arial", 16),
            style="Dark.TLabel"
        ).pack(side="left")

        ttk.Button(
            header,
            text="Back",
            command=self.go_back,
            style="Dark.TButton"
        ).pack(side="right")

        # -----------------------------------
        # TABLE
        # -----------------------------------

        self.tree = ttk.Treeview(
            self,
            columns=("id", "name", "budget"),
            show="headings",
            height=12,
            style="Dark.Treeview"
        )

        self.tree.heading("name", text="Category")
        self.tree.heading("budget", text="Monthly Budget")

        self.tree.heading("id", text="ID")

        self.tree.column("id", width=0, stretch=False)
        self.tree.column("name", width=250)
        self.tree.column("budget", width=150)

        self.tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # -----------------------------------
        # FORM
        # -----------------------------------

        form = ttk.Frame(self, style="Dark.TFrame")
        form.pack(pady=10)

        ttk.Label(
            form,
            text="Category Name:",
            style="Dark.TLabel"
        ).grid(row=0, column=0, padx=5, pady=5)

        self.name_entry = ttk.Entry(
            form,
            width=30,
            style="Dark.TEntry"
        )
        self.name_entry.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        ttk.Label(
            form,
            text="Monthly Budget:",
            style="Dark.TLabel"
        ).grid(row=1, column=0, padx=5, pady=5)

        self.budget_entry = ttk.Entry(
            form,
            width=30,
            style="Dark.TEntry"
        )
        self.budget_entry.grid(
            row=1,
            column=1,
            padx=5,
            pady=5
        )

        # -----------------------------------
        # BUTTONS
        # -----------------------------------

        button_frame = ttk.Frame(
            self,
            style="Dark.TFrame"
        )

        button_frame.pack(pady=10)

        ttk.Button(
            button_frame,
            text="Add Category",
            command=self.add_category,
            style="Dark.TButton"
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Update",
            command=self.update_category,
            style="Dark.TButton"
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Delete",
            command=self.delete_category,
            style="Dark.TButton"
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Clear Budget",
            command=self.clear_budget,
            style="Dark.TButton"
        ).pack(side="left", padx=5)

        ttk.Button(
            button_frame,
            text="Load Selected",
            command=self.load_selected,
            style="Dark.TButton"
        ).pack(side="left", padx=5)

        self.refresh_table()

    # -----------------------------------
    # HELPERS
    # -----------------------------------

    def get_selected(self):

        selected = self.tree.selection()

        if not selected:
            return None

        return self.tree.item(selected[0])["values"]

    def clear_form(self):

        self.name_entry.delete(0, tk.END)
        self.budget_entry.delete(0, tk.END)

    # -----------------------------------
    # TABLE
    # -----------------------------------

    def refresh_table(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        categories = self.controller.get_categories()

        for category in categories:

            budget = (
                category.monthly_limit
                if category.monthly_limit is not None
                else 0.0
            )

            self.tree.insert(
                "",
                "end",
                values=(
                    category.id,
                    category.name,
                    f"{budget:.2f}"
                )
            )

    # -----------------------------------
    # CREATE
    # -----------------------------------

    def add_category(self):

        name = self.name_entry.get().strip()

        if not name:

            messagebox.showerror(
                "Missing Name",
                "Category name required."
            )

            return

        budget_text = self.budget_entry.get().strip()

        budget = None

        if budget_text:

            try:
                budget = float(budget_text)
            except ValueError:
                messagebox.showerror(
                    "Invalid Budget",
                    "Budget must be numeric."
                )
                return

        self.controller.add_category(
            name,
            budget
        )

        self.refresh_table()
        self.clear_form()

    # -----------------------------------
    # UPDATE
    # -----------------------------------

    def update_category(self):

        row = self.get_selected()

        if not row:
            return

        category_id = row[0]

        name = self.name_entry.get().strip()

        if not name:
            return

        budget_text = self.budget_entry.get().strip()

        budget = None

        if budget_text:

            try:
                budget = float(budget_text)
            except ValueError:
                return

        self.controller.update_category(
            category_id,
            name,
            budget
        )

        self.refresh_table()

    # -----------------------------------
    # DELETE
    # -----------------------------------

    def delete_category(self):

        row = self.get_selected()

        if not row:
            return

        category_id = row[0]

        confirm = messagebox.askyesno(
            "Delete Category",
            "Delete selected category?"
        )

        if not confirm:
            return

        self.controller.delete_category(
            category_id
        )

        self.refresh_table()
        self.clear_form()

    # -----------------------------------
    # CLEAR BUDGET
    # -----------------------------------

    def clear_budget(self):

        row = self.get_selected()

        if not row:
            return

        category_id = row[0]

        self.controller.update_category_budget(
            category_id,
            None
        )

        self.refresh_table()

    # -----------------------------------
    # LOAD
    # -----------------------------------

    def load_selected(self):

        row = self.get_selected()

        if not row:
            return

        _, name, budget = row

        self.clear_form()

        self.name_entry.insert(
            0,
            name
        )

        if float(budget) > 0:

            self.budget_entry.insert(
                0,
                budget
            )

    # -----------------------------------
    # NAVIGATION
    # -----------------------------------

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