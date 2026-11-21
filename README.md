# Descriptive Spending Tracker

A desktop personal finance application built with Python, Tkinter, and SQLite that helps users track income and expenses using descriptive transactions, custom categories, multiple accounts, spending summaries, budgets, and visual analytics.

The application follows a layered architecture that separates the user interface, business logic, data models, and database access, making it maintainable and easy to extend.

## Features

**Transaction Management**
- Record income and expense transactions
- Add detailed descriptions to transactions
- Categorize transactions for spending analysis
- View all recorded transactions in a sortable table
- Store transaction history permanently in a SQLite database

**Account Management**
- Create and manage multiple accounts

**Category Management**
- Create custom spending and income categories
- Organize transactions for reporting and analysis
- Edit and maintain categories independently of transactions

**Budgeting**
- Set spending budgets
- Compare actual spending against budget targets
- Monitor spending habits over time

**Dashboard**
- Centralized overview of financial activity
- Quick access to major application features
- High-level spending insights

**Spending Analytics**
- Category-based spending summaries
- Income vs. expense reporting
- Pie chart visualizations of spending distribution
- Financial summary views generated from transaction data

**Modern User Interface**
- Built with Tkinter
- Dark theme support
- Multiple dedicated views for financial management
- Desktop application requiring no internet connection

## Architecture

The project follows a layered architecture inspired by MVC principles

UI Layer
    ↓
Controller
    ↓
Service Layer
    ↓
Repository Layer
    ↓
SQLite Database

## Components

### Models
The model package contains the application's domain objects:

- account.py
- category.py
- transaction.py

These classes represent the core financial entities used throughout the system.

### Services
The service package contains business logic:

#### Transaction Service
Handles:

- Transaction creation
- Transaction validation
- Transaction retrieval
- Transaction management

#### Budget Service
Handles:

- Budget calculations
- Budget tracking
- Budget-related business rules

#### Summary Service
Generates:

- Spending summaries
- Financial reports
- Dashboard statistics

### Storage Layer
The storage package provides database access.
**Database Repository**
`storage/database_repository.py`

Responsible for:

- SQLite database operations
- Data persistence
- Query execution
- Object retrieval and storage

### User Interface
The ui/views package contains individual screens for the application.
**Dashboard View**
`dashboard_view.py`
Provides an overview of the user's financial information.

**Add Transaction View**
`add_transaction_view.py`
Allows users to create new income and expense transactions.

**Transaction Table View**
`transaction_table_view.py`
Displays transaction history in a structured table.

**Account View**
`account_view.py`
Account management and balance tracking.

**Category View**
`category_view.py`
Category creation and management.

**Summary View**
`summary_view.py`
Displays spending and financial summaries.

**Pie Chart View**
`pie_chart_view.py`
Visualizes spending breakdowns by category.

## Project Structure
Descriptive Spending Tracker
│
├── controller.py
├── main.py
├── spending_tracker.db
│
├── model
│   ├── account.py
│   ├── category.py
│   └── transaction.py
│
├── service
│   ├── budget_service.py
│   ├── summary_service.py
│   └── transaction_service.py
│
├── storage
│   └── database_repository.py
│
├── ui
│   ├── gui_main.py
│   ├── theme.py
│   │
│   └── views
│       ├── account_view.py
│       ├── add_transaction_view.py
│       ├── category_view.py
│       ├── dashboard_view.py
│       ├── pie_chart_view.py
│       ├── summary_view.py
│       └── transaction_table_view.py
│
└── util
    └── date_utils.py

## Technologies Used
- Python 3
- Tkinter
- ttk Widgets
- SQLite
- Object-Oriented Programming
- MVC-inspired architecture

## Installation
**Clone the Repository**
git clone https://github.com/yourusername/descriptive-spending-tracker.git
cd descriptive-spending-tracker

**Create a Virtual Environment**
Windows:
python -m venv .venv
.venv\Scripts\activate

Linus/macOS:
python3 -m venv .venv
source .venv/bin/activate

**Install Dependencies**
pip install -r requirements.txt

**Run the Application**
python main.py

## Database
The application uses SQLite for persistent local storage.

Database file: spending_tracker.db

This allows all financial data to remain on the user's machine without requiring cloud services or external accounts.

## Future Improvements
- CSV import/export
- Recurring transactions
- Savings goals
- Advanced filtering and search
- Multi-user support

## Educational Goals
This project demonstrates:

- Object-oriented design
- Layered application architecture
- Separation of concerns
- GUI development with Tkinter
- SQLite database integration
- Financial data analysis and visualization
- Service and repository design patterns

