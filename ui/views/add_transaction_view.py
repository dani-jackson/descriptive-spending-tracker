import tkinter as tk
from tkinter import ttk, messagebox
from ui.theme import apply_dark_theme


class AddTransactionView(ttk.Frame):
    """
    AddTransactionView
    -------------------
    Handles:
        • Adding deposits, withdrawals, and purchases
        • Editing existing transactions (via unique transaction IDs)
        • Dark‑mode UI
        • Scrollable content area
        • Category dropdown + free‑text entry
        • Purchase mode selection (item price vs final total)
    """

    def __init__(self, parent, controller, edit_mode=False):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent
        self.edit_mode = edit_mode

        # Apply dark theme
        apply_dark_theme(self)
        self.configure(style="Dark.TFrame")

        # ============================================================
        # HEADER BAR (fixed at top)
        # ============================================================
        header = ttk.Frame(self, style="Dark.TFrame")
        header.pack(fill="x", pady=10, padx=10)

        ttk.Label(
            header,
            text="Add Transaction",
            font=("Arial", 16),
            style="Dark.TLabel"
        ).pack(side="left")

        ttk.Button(
            header,
            text="Back",
            style="Dark.TButton",
            command=self.go_back
        ).pack(side="right")

        # ============================================================
        # SCROLLABLE CANVAS (all content lives inside self.inner)
        # ============================================================
        outer = ttk.Frame(self, style="Dark.TFrame")
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            outer,
            highlightthickness=0,
            bg="#1e1e1e"
        )
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Inner frame that holds all content
        self.inner = ttk.Frame(canvas, style="Dark.TFrame")
        self.inner_id = canvas.create_window((0, 0), window=self.inner, anchor="nw")

        # Update scrollregion when inner frame changes
        self.inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _on_linux_scroll(event):
            canvas.yview_scroll(1 if event.num == 5 else -1, "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Button-4>", _on_linux_scroll)
        canvas.bind_all("<Button-5>", _on_linux_scroll)

        # Keyboard shortcuts
        self.bind_all("<Escape>", lambda e: self.go_back())
        self.bind_all("<Return>", lambda e: self.add_purchase())

        # ============================================================
        # CONTENT
        # ============================================================
        self._divider("Transaction Details")

        self.date_entry = self._entry("Date (MM/DD/YY)")
        self.desc_entry = self._entry("Description")
        self.amount_entry = self._entry("Amount")

        # ============================================================
        # CATEGORY (Dropdown + Free‑text)
        # ============================================================
        cat_frame = ttk.Frame(self.inner, style="Dark.TFrame")
        cat_frame.pack(fill="x", pady=(10, 5))

        ttk.Label(cat_frame, text="Category:", style="Dark.TLabel").grid(row=0, column=0, padx=5, pady=5)

        self.category_var = tk.StringVar()
        self.category_dropdown = ttk.Combobox(
            cat_frame,
            textvariable=self.category_var,
            values=self.controller.current_account.all_categories(),
            state="readonly",
            width=20,
            style="Dark.TCombobox"
        )
        self.category_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Free‑text entry for new categories
        self.category_entry = tk.Entry(
            cat_frame,
            bg="#1e1e1e",
            fg="#ffffff",
            insertbackground="white",
            width=22
        )
        self.category_entry.grid(row=0, column=2, padx=5, pady=5)

        # Auto‑fill free‑text when selecting from dropdown
        def on_category_select(event):
            self.category_entry.delete(0, "end")
            self.category_entry.insert(0, self.category_var.get())

        self.category_dropdown.bind("<<ComboboxSelected>>", on_category_select)

        # ============================================================
        # PURCHASE OPTIONS
        # ============================================================
        self._divider("Purchase Options")

        self.purchase_mode = tk.StringVar(value="item")

        mode_frame = ttk.Frame(self.inner, style="Dark.TFrame")
        mode_frame.pack(pady=10, fill="x")

        ttk.Radiobutton(
            mode_frame,
            text="Item price (calculate tax)",
            variable=self.purchase_mode,
            value="item",
            style="Dark.TRadiobutton"
        ).pack(anchor="w", padx=10)

        ttk.Radiobutton(
            mode_frame,
            text="Final total (no tax/shipping)",
            variable=self.purchase_mode,
            value="total",
            style="Dark.TRadiobutton"
        ).pack(anchor="w", padx=10)

        # ============================================================
        # EDIT MODE PREFILL
        # ============================================================
        if self.edit_mode and getattr(controller, "editing_transaction", None):
            tx = controller.editing_transaction

            self.date_entry.insert(0, tx["date"])
            self.desc_entry.insert(0, tx["description"])
            self.amount_entry.insert(0, tx["amount"])
            self.category_entry.insert(0, tx["category"])

            if tx["type"] == "Purchase":
                self.purchase_mode.set("item")

        # ============================================================
        # ACTION BUTTONS
        # ============================================================
        self._divider("Actions")

        button_bar = ttk.Frame(self.inner, style="Dark.TFrame")
        button_bar.pack(pady=20)

        ttk.Button(button_bar, text="Add Deposit", command=self.add_deposit, style="Dark.TButton").pack(side="left", padx=8)
        ttk.Button(button_bar, text="Add Withdrawal", command=self.add_withdrawal, style="Dark.TButton").pack(side="left", padx=8)
        ttk.Button(button_bar, text="Add Purchase", command=self.add_purchase, style="Dark.TButton").pack(side="left", padx=8)
        ttk.Button(button_bar, text="Add Another", command=self.clear_fields, style="Dark.TButton").pack(side="left", padx=8)

    # ============================================================
    # HELPERS
    # ============================================================
    def _entry(self, label_text):
        """Creates a labeled entry field."""
        wrapper = ttk.Frame(self.inner, style="Dark.TFrame")
        wrapper.pack(pady=5, fill="x")

        ttk.Label(wrapper, text=label_text, style="Dark.TLabel").pack(anchor="w", padx=5)
        entry = ttk.Entry(wrapper, style="Dark.TEntry")
        entry.pack(fill="x", padx=5, pady=3)
        return entry

    def _divider(self, text):
        """Section divider with label + horizontal line."""
        frame = ttk.Frame(self.inner, style="Dark.TFrame")
        frame.pack(fill="x", pady=(20, 10))

        ttk.Label(frame, text=text, font=("Arial", 12, "bold"), style="Dark.TLabel").pack(anchor="w", padx=5)
        ttk.Separator(self.inner, orient="horizontal", style="Dark.TSeparator").pack(fill="x", padx=5, pady=5)

    def show_toast(self, message):
        """Temporary popup notification."""
        toast = tk.Toplevel(self)
        toast.overrideredirect(True)
        toast.configure(bg="#333333")

        self.update_idletasks()
        x = self.winfo_rootx() + self.winfo_width() // 2 - 100
        y = self.winfo_rooty() + self.winfo_height() - 80
        toast.geometry(f"200x40+{x}+{y}")

        ttk.Label(toast, text=message, style="Dark.TLabel").pack(expand=True)
        toast.after(2000, toast.destroy)

    # ============================================================
    # ACTIONS (with ID‑based edit removal)
    # ============================================================
    def _remove_old_if_editing(self):
        """Removes the original transaction using its unique ID."""
        if not self.edit_mode:
            return

        old = self.controller.editing_transaction
        old_id = old.get("id")

        if not old_id:
            return

        for tx in self.controller.current_account.transactions:
            if getattr(tx, "id", None) == old_id:
                self.controller.current_account.transactions.remove(tx)
                break

    def clear_fields(self):
        self.date_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.purchase_mode.set("item")

    def add_deposit(self):
        self._remove_old_if_editing()

        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid number.")
            return

        self.controller.add_deposit(self.date_entry.get(), self.desc_entry.get(), amount)
        self.show_toast("Deposit added!")
        self.clear_fields()

    def add_withdrawal(self):
        self._remove_old_if_editing()

        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid number.")
            return

        self.controller.add_withdrawal(self.date_entry.get(), self.desc_entry.get(), amount)
        self.show_toast("Withdrawal added!")
        self.clear_fields()

    def add_purchase(self):
        self._remove_old_if_editing()

        use_total = (self.purchase_mode.get() == "total")
        category = self.category_entry.get().strip()

        if category and category not in self.controller.current_account.budgets:
            self.controller.current_account.budgets[category] = None

        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Amount", "Please enter a valid number.")
            return

        try:
            self.controller.add_purchase(
                self.date_entry.get(),
                self.desc_entry.get(),
                amount,
                category,
                tax=0.087,
                fees=0,
                shipping=0,
                use_total=use_total
            )
        except Exception as e:
            messagebox.showerror("Error", f"Could not add purchase:\n{e}")
            return

        self.category_dropdown["values"] = self.controller.current_account.all_categories()
        self.show_toast("Purchase added!")
        self.clear_fields()

    # ============================================================
    # NAVIGATION
    # ============================================================
    def go_back(self):
        """Return to dashboard and unbind scroll events."""
        from ui.views.dashboard_view import DashboardView

        for widget in self.parent.winfo_children():
            widget.destroy()

        try:
            self.unbind_all("<MouseWheel>")
        except:
            pass

        DashboardView(self.parent, self.controller).pack(fill="both", expand=True)
