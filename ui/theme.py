import tkinter as tk
from tkinter import ttk


def apply_dark_theme(root):
    """Apply application-wide dark theme."""

    style = ttk.Style()

    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    # ------------------------------------------------------------
    # COLORS
    # ------------------------------------------------------------

    BG = "#1e1e1e"
    BG_DARK = "#181818"

    FG = "#ffffff"
    FG_MUTED = "#cccccc"

    ACCENT = "#3a82f7"

    BTN_BG = "#2d2d2d"
    BTN_BG_HOVER = "#3a3a3a"

    ENTRY_BG = "#2a2a2a"
    ENTRY_FG = "#ffffff"

    DANGER = "#b00020"
    DANGER_HOVER = "#d32f2f"

    SUCCESS = "#7CFC00"
    WARNING = "#FFA500"
    ERROR = "#ff6b6b"

    # ------------------------------------------------------------
    # FRAMES
    # ------------------------------------------------------------

    style.configure(
        "Dark.TFrame",
        background=BG
    )

    # ------------------------------------------------------------
    # LABELS
    # ------------------------------------------------------------

    style.configure(
        "Dark.TLabel",
        background=BG,
        foreground=FG
    )

    style.configure(
        "DarkMuted.TLabel",
        background=BG,
        foreground=FG_MUTED
    )

    style.configure(
        "Success.TLabel",
        background=BG,
        foreground=SUCCESS
    )

    style.configure(
        "Warning.TLabel",
        background=BG,
        foreground=WARNING
    )

    style.configure(
        "Error.TLabel",
        background=BG,
        foreground=ERROR
    )

    # ------------------------------------------------------------
    # BUTTONS
    # ------------------------------------------------------------

    style.configure(
        "Dark.TButton",
        background=BTN_BG,
        foreground=FG,
        padding=6,
        borderwidth=1
    )

    style.map(
        "Dark.TButton",
        background=[
            ("active", BTN_BG_HOVER)
        ]
    )

    # ------------------------------------------------------------
    # DANGER BUTTONS
    # ------------------------------------------------------------

    style.configure(
        "Danger.TButton",
        background=DANGER,
        foreground="#ffffff",
        padding=6
    )

    style.map(
        "Danger.TButton",
        background=[
            ("active", DANGER_HOVER)
        ]
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
    # COMBOBOX
    # ------------------------------------------------------------

    try:
        style.element_create(
            "DarkCombobox.downarrow",
            "from",
            "clam"
        )
    except tk.TclError:
        pass

    style.layout(
        "Dark.TCombobox",
        style.layout("TCombobox")
    )

    style.configure(
        "Dark.TCombobox",
        foreground=ENTRY_FG,
        background=ENTRY_BG,
        fieldbackground=ENTRY_BG,
        selectbackground=ACCENT,
        selectforeground=FG,
        arrowcolor=FG,
        arrowsize=14
    )

    style.map(
        "Dark.TCombobox",
        foreground=[
            ("readonly", ENTRY_FG)
        ],
        fieldbackground=[
            ("readonly", ENTRY_BG),
            ("!disabled", ENTRY_BG)
        ],
        background=[
            ("readonly", ENTRY_BG),
            ("!disabled", ENTRY_BG)
        ],
        selectbackground=[
            ("readonly", ACCENT)
        ],
        selectforeground=[
            ("readonly", FG)
        ]
    )

    # ------------------------------------------------------------
    # COMBOBOX DROPDOWN
    # ------------------------------------------------------------

    root.option_add(
        "*TCombobox*Listbox.background",
        ENTRY_BG
    )

    root.option_add(
        "*TCombobox*Listbox.foreground",
        ENTRY_FG
    )

    root.option_add(
        "*TCombobox*Listbox.selectBackground",
        ACCENT
    )

    root.option_add(
        "*TCombobox*Listbox.selectForeground",
        "#ffffff"
    )

    root.option_add(
        "*TCombobox*Listbox.font",
        "Arial 11"
    )

    # ------------------------------------------------------------
    # SEPARATORS
    # ------------------------------------------------------------

    style.configure(
        "Dark.TSeparator",
        background=BG_DARK
    )

    # ------------------------------------------------------------
    # TREEVIEW
    # ------------------------------------------------------------

    style.configure(
        "Dark.Treeview",
        background=BG_DARK,
        fieldbackground=BG_DARK,
        foreground=FG,
        rowheight=24,
        borderwidth=0
    )

    style.configure(
        "Dark.Treeview.Heading",
        background=BTN_BG,
        foreground=FG,
        relief="flat"
    )

    style.map(
        "Dark.Treeview",
        background=[
            ("selected", ACCENT)
        ],
        foreground=[
            ("selected", "#ffffff")
        ]
    )

    style.map(
        "Dark.Treeview.Heading",
        background=[
            ("active", BTN_BG_HOVER)
        ]
    )

    # ------------------------------------------------------------
    # SCROLLBARS
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

    style.configure(
        "Horizontal.TScrollbar",
        background=BTN_BG,
        troughcolor=BG_DARK,
        arrowcolor=FG,
        bordercolor=BG_DARK,
        lightcolor=BG_DARK,
        darkcolor=BG_DARK
    )

    # ------------------------------------------------------------
    # ROOT WINDOW
    # ------------------------------------------------------------

    try:
        root.configure(background=BG)
    except Exception:
        pass