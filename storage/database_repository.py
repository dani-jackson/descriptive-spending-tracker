import sqlite3

from model.transaction import Transaction
from model.account import Account
from model.category import Category


class DatabaseRepository:

    def __init__(self, db_name="spending_tracker.db"):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row

        self.conn.execute("PRAGMA foreign_keys = ON")

        self.create_tables()

    # -----------------------------
    # DATABASE SETUP
    # -----------------------------

    def create_tables(self):

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                account_type TEXT NOT NULL
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                monthly_limit REAL
            )
        """)

        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id TEXT PRIMARY KEY,
                transaction_type TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT NOT NULL,
                amount REAL NOT NULL,
                merchant TEXT,
                account_id INTEGER,
                category_id INTEGER,
                FOREIGN KEY(account_id)
                    REFERENCES accounts(id),
                FOREIGN KEY(category_id)
                    REFERENCES categories(id)
            )
        """)

        self.conn.commit()

    # -----------------------------
    # ACCOUNT METHODS
    # -----------------------------

    def add_account(self, account):

        cursor = self.conn.execute("""
            INSERT INTO accounts(
                name,
                account_type
            )
            VALUES (?, ?)
        """, (
            account.name,
            account.account_type
        ))

        self.conn.commit()

        return cursor.lastrowid

    def get_account(self, account_id):

        row = self.conn.execute("""
            SELECT *
            FROM accounts
            WHERE id = ?
        """, (account_id,)).fetchone()

        if row is None:
            return None

        return Account(
            id=row["id"],
            name=row["name"],
            account_type=row["account_type"]
        )

    def get_all_accounts(self):

        rows = self.conn.execute("""
            SELECT *
            FROM accounts
            ORDER BY name
        """).fetchall()

        return [
            Account(
                id=row["id"],
                name=row["name"],
                account_type=row["account_type"]
            )
            for row in rows
        ]

    def delete_account(self, account_id):

        self.conn.execute("""
            DELETE FROM accounts
            WHERE id = ?
        """, (account_id,))

        self.conn.commit()

    def update_account(
        self,
        account_id,
        name,
        account_type
    ):

        self.conn.execute("""
            UPDATE accounts
            SET
                name = ?,
                account_type = ?
            WHERE id = ?
        """, (
            name,
            account_type,
            account_id
        ))

        self.conn.commit()

    # -----------------------------
    # CATEGORY METHODS
    # -----------------------------

    def add_category(self, category):

        cursor = self.conn.execute("""
            INSERT INTO categories(
                name,
                monthly_limit
            )
            VALUES (?, ?)
        """, (
            category.name,
            category.monthly_limit
        ))

        self.conn.commit()

        return cursor.lastrowid

    def get_category(self, category_id):

        row = self.conn.execute("""
            SELECT *
            FROM categories
            WHERE id = ?
        """, (category_id,)).fetchone()

        if row is None:
            return None

        return Category(
            id=row["id"],
            name=row["name"],
            monthly_limit=row["monthly_limit"]
        )

    def get_all_categories(self):

        rows = self.conn.execute("""
            SELECT *
            FROM categories
            ORDER BY name
        """).fetchall()

        return [
            Category(
                id=row["id"],
                name=row["name"],
                monthly_limit=row["monthly_limit"]
            )
            for row in rows
        ]

    def delete_category(self, category_id):

        self.conn.execute("""
            DELETE FROM categories
            WHERE id = ?
        """, (category_id,))

        self.conn.commit()

    def update_category(
        self,
        category_id,
        name,
        monthly_limit
    ):

        self.conn.execute("""
            UPDATE categories
            SET
                name = ?,
                monthly_limit = ?
            WHERE id = ?
        """, (
            name,
            monthly_limit,
            category_id
        ))

        self.conn.commit()

    def update_category_budget(
        self,
        category_id,
        monthly_limit
    ):

        self.conn.execute("""
            UPDATE categories
            SET
                monthly_limit = ?
            WHERE id = ?
        """, (
            monthly_limit,
            category_id
        ))

        self.conn.commit()

    # -----------------------------
    # TRANSACTION METHODS
    # -----------------------------

    def add_transaction(self, transaction):

        self.conn.execute("""
            INSERT INTO transactions (
                id,
                transaction_type,
                date,
                description,
                amount,
                merchant,
                account_id,
                category_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            transaction.id,
            transaction.transaction_type,
            transaction.date,
            transaction.description,
            transaction.amount,
            transaction.merchant,
            transaction.account_id,
            transaction.category_id
        ))

        self.conn.commit()

    def update_transaction(
        self,
        transaction
    ):

        self.conn.execute("""
            UPDATE transactions
            SET
                transaction_type = ?,
                date = ?,
                description = ?,
                amount = ?,
                merchant = ?,
                account_id = ?,
                category_id = ?
            WHERE id = ?
        """, (
            transaction.transaction_type,
            transaction.date,
            transaction.description,
            transaction.amount,
            transaction.merchant,
            transaction.account_id,
            transaction.category_id,
            transaction.id
        ))

        self.conn.commit()

    def delete_transaction(self, transaction_id):

        self.conn.execute("""
            DELETE FROM transactions
            WHERE id = ?
        """, (transaction_id,))

        self.conn.commit()

    def get_transaction(self, transaction_id):

        row = self.conn.execute("""
            SELECT *
            FROM transactions
            WHERE id = ?
        """, (transaction_id,)).fetchone()

        if row is None:
            return None

        return self._row_to_transaction(row)

    def get_all_transactions(self):

        rows = self.conn.execute("""
            SELECT *
            FROM transactions
            ORDER BY date DESC
        """).fetchall()

        return [
            self._row_to_transaction(row)
            for row in rows
        ]

    # -----------------------------
    # FILTERING
    # -----------------------------

    def get_transactions_by_category(self, category_id):

        rows = self.conn.execute("""
            SELECT *
            FROM transactions
            WHERE category_id = ?
            ORDER BY date DESC
        """, (category_id,)).fetchall()

        return [
            self._row_to_transaction(row)
            for row in rows
        ]

    def get_transactions_by_account(self, account_id):

        rows = self.conn.execute("""
            SELECT *
            FROM transactions
            WHERE account_id = ?
            ORDER BY date DESC
        """, (account_id,)).fetchall()

        return [
            self._row_to_transaction(row)
            for row in rows
        ]

    def search_transactions(self, text):

        rows = self.conn.execute("""
            SELECT *
            FROM transactions
            WHERE description LIKE ?
               OR merchant LIKE ?
            ORDER BY date DESC
        """, (
            f"%{text}%",
            f"%{text}%"
        )).fetchall()

        return [
            self._row_to_transaction(row)
            for row in rows
        ]

    # -----------------------------
    # REPORTING
    # -----------------------------

    def get_total_spending_for_month(self, year, month):

        result = self.conn.execute("""
            SELECT
                SUM(amount)
            FROM transactions
            WHERE transaction_type = 'Purchase'
              AND strftime('%Y', date) = ?
              AND strftime('%m', date) = ?
        """, (
            str(year),
            str(month).zfill(2)
        )).fetchone()

        return result[0] or 0

    def get_spending_by_category(self, year, month):

        rows = self.conn.execute("""
            SELECT
                c.name,
                SUM(t.amount) AS total
            FROM transactions t
            JOIN categories c
                ON t.category_id = c.id

            WHERE t.transaction_type = 'Purchase'
              AND strftime('%Y', t.date) = ?
              AND strftime('%m', t.date) = ?

            GROUP BY c.name
            ORDER BY total DESC
        """, (
            str(year),
            str(month).zfill(2)
        )).fetchall()

        return {
            row["name"]: row["total"]
            for row in rows
        }

    # -----------------------------
    # INTERNAL HELPER
    # -----------------------------

    def _row_to_transaction(self, row):

        return Transaction(
            transaction_type=row["transaction_type"],
            date=row["date"],
            description=row["description"],
            amount=row["amount"],
            merchant=row["merchant"],
            account_id=row["account_id"],
            category_id=row["category_id"],
            id=row["id"]
        )

    # -----------------------------
    # CLEANUP
    # -----------------------------

    def close(self):
        self.conn.close()