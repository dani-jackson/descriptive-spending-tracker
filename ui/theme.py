import tkinter as tk
from tkinter import ttk

def apply_dark_theme(root):
    """Apply a consistent dark theme to all ttk widgets."""

    style = ttk.Style()

    # Use a stable base theme
    try:
        style.theme_use("clam")
    except:
        pass

    # ------------------------------------------------------------
    # COLOR PALETTE
    # ------------------------------------------------------------
    BG = "#1e1e1e"          # main background
    BG_DARK = "#181818"     # darker panels
    FG = "#ffffff"          # primary text
    FG_MUTED = "#cccccc"    # secondary text
    ACCENT = "#3a82f7"      # blue highlight
    BTN_BG = "#2d2d2d"      # button background
    BTN_BG_HOVER = "#3a3a3a"
    ENTRY_BG = "#2a2a2a"
    ENTRY_FG = "#ffffff"

    # ------------------------------------------------------------
    # FRAMES & LABELS
    # ------------------------------------------------------------
    style.configure("Dark.TFrame", background=BG)
    style.configure("Dark.TLabel", background=BG, foreground=FG)
    style.configure("DarkMuted.TLabel", background=BG, foreground=FG_MUTED)

    # ------------------------------------------------------------
    # BUTTONS
    # ------------------------------------------------------------
    style.configure(
        "Dark.TButton",
        background=BTN_BG,
        foreground=FG,
        padding=6,
        borderwidth=1,
        focusthickness=3,
        focuscolor=ACCENT
    )
    style.map(
        "Dark.TButton",
        background=[("active", BTN_BG_HOVER)],
        foreground=[("active", FG)]
    )
    
    # ------------------------------------------------------------
    # RADIOBUTTONS
    # ------------------------------------------------------------
    style.configure(
        "Dark.TRadiobutton",
        background=BG,
        foreground=FG,
        indicatorcolor=ACCENT,
        focuscolor=ACCENT
)

    # ------------------------------------------------------------
    # ENTRY
    # ------------------------------------------------------------
    style.configure(
        "Dark.TEntry",
        fieldbackground=ENTRY_BG,
        background=ENTRY_BG,
        foreground=ENTRY_FG,
        bordercolor=BG_DARK,
        lightcolor=ACCENT,
        darkcolor=BG_DARK
    )

    # ------------------------------------------------------------
    # COMBOBOX (main widget)
    # ------------------------------------------------------------

    # Create the custom arrow element ONLY once
    try:
        style.element_create("DarkCombobox.downarrow", "from", "clam")
    except tk.TclError:
        # Element already exists — safe to ignore
        pass

    style.layout("Dark.TCombobox", style.layout("TCombobox"))

    style.configure(
        "Dark.TCombobox",
        arrowsize=14,
        background=ENTRY_BG,
        fieldbackground=ENTRY_BG,
        foreground=ENTRY_FG,
        bordercolor=BG_DARK,
        lightcolor=BG_DARK,
        darkcolor=BG_DARK,
        arrowcolor=FG
    )

    style.map(
        "Dark.TCombobox",
        fieldbackground=[("readonly", ENTRY_BG)],
        foreground=[("readonly", ENTRY_FG)],
        background=[("readonly", ENTRY_BG)]
    )

    # ------------------------------------------------------------
    # COMBOBOX DROPDOWN LISTBOX (the popup menu)
    # ------------------------------------------------------------
    root.option_add("*TCombobox*Listbox.background", ENTRY_BG)
    root.option_add("*TCombobox*Listbox.foreground", ENTRY_FG)
    root.option_add("*TCombobox*Listbox.selectBackground", ACCENT)
    root.option_add("*TCombobox*Listbox.selectForeground", "#ffffff")
    root.option_add("*TCombobox*Listbox.font", "Arial 11")

    # ------------------------------------------------------------
    # SEPARATOR
    # ------------------------------------------------------------
    style.configure("Dark.TSeparator", background=BG_DARK)

    # ------------------------------------------------------------
    # TREEVIEW
    # ------------------------------------------------------------
    style.configure(
        "Treeview",
        background=BG_DARK,
        fieldbackground=BG_DARK,
        foreground=FG,
        bordercolor=BG,
        borderwidth=0,
        rowheight=24
    )
    style.configure(
        "Treeview.Heading",
        background=BTN_BG,
        foreground=FG,
        relief="flat"
    )
    style.map(
        "Treeview",
        background=[("selected", ACCENT)],
        foreground=[("selected", "#ffffff")]
    )

    # ------------------------------------------------------------
    # SCROLLBAR
    # ------------------------------------------------------------
    style.configure(
        "Vertical.TScrollbar",
        background=BTN_BG,
        troughcolor=BG_DARK,
        arrowcolor=FG,
        bordercolor=BG_DARK,
        lightcolor=BG_DARK,
        darkcolor=BG_DARK
    )

    # ------------------------------------------------------------
    # APPLY BACKGROUND TO ROOT
    # ------------------------------------------------------------
    try:
        root.configure(background=BG)
    except:
        pass
