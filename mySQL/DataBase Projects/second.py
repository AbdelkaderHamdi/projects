import sqlite3
from datetime import date

class DatabaseManager:
    def __init__(self, db_path='bank.db'):
        self.db_path = db_path
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connect_to_db()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_db()

    def connect_to_db(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.cursor = self.connection.cursor()
            print('Connected successfully.')
        except sqlite3.Error as e:
            print(f'Error connecting to database: {e}')

    def close_db(self):
        if self.connection:
            self.connection.close()
            print('Connection to database is closed.')

    def commit_db(self):
        if self.connection:
            self.connection.commit()

class Customer:
    def __init__(self, full_name, email, phone_number, address, date_of_birth):
        self.full_name = full_name
        self.email = email
        self.phone_number = phone_number
        self.address = address
        self.date_of_birth = date_of_birth

class CustomerManager(DatabaseManager):
    def __init__(self, db_path='bank.db'):
        super().__init__(db_path)
        self.create_customer_table()

    def create_customer_table(self):
        with self:
            try:
                self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS customers (
                    customerID INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    phone_number TEXT NOT NULL,
                    address TEXT NOT NULL,
                    date_of_birth DATE NOT NULL
                )
                """)
                self.commit_db()
            except sqlite3.Error as e:
                print(f'Error creating table: {e}')

    def insert_customer(self, customer):
        with self:
            try:
                self.cursor.execute("""
                INSERT INTO customers (full_name, email, phone_number, address, date_of_birth)
                VALUES (?, ?, ?, ?, ?)
                """, (customer.full_name, customer.email, customer.phone_number, customer.address, customer.date_of_birth))
                self.commit_db()
                print('Customer added successfully!')
                return self.cursor.lastrowid
            except sqlite3.Error as e:
                print(f'Error inserting customer: {e}')
                return None

    def get_customer_id_by_name(self, full_name):
        with self:
            try:
                self.cursor.execute("SELECT customerID FROM customers WHERE full_name = ?", (full_name,))
                result = self.cursor.fetchone()
                return result[0] if result else None
            except sqlite3.Error as e:
                print(f'Error fetching customerID: {e}')
                return None

class Account:
    def __init__(self, account_type, balance, customer_id, status="Active", opened_date=None):
        self.account_type = account_type
        self.balance = balance
        self.customer_id = customer_id
        self.status = status
        self.opened_date = opened_date or date.today()

class AccountManager(DatabaseManager):
    def __init__(self, db_path='bank.db'):
        super().__init__(db_path)
        self.create_accounts_table()

    def create_accounts_table(self):
        with self:
            try:
                self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS accounts (
                    account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_type TEXT NOT NULL,
                    balance REAL NOT NULL,
                    customer_id INTEGER NOT NULL,
                    opened_date DATE NOT NULL,
                    status TEXT NOT NULL,
                    FOREIGN KEY (customer_id) REFERENCES customers(customerID)
                )
                """)
                self.commit_db()
            except sqlite3.Error as e:
                print(f'Error creating table: {e}')

    def insert_account(self, account):
        with self:
            try:
                self.cursor.execute("""
                INSERT INTO accounts (account_type, balance, customer_id, opened_date, status)
                VALUES (?, ?, ?, ?, ?)
                """, (account.account_type, account.balance, account.customer_id, account.opened_date, account.status))
                self.commit_db()
                print(f"Account for CustomerID {account.customer_id} added successfully!")
                return self.cursor.lastrowid
            except sqlite3.Error as e:
                print(f'Error inserting account: {e}')
                return None




# Example usage
if __name__ == "__main__":
    customer_manager = CustomerManager()
    new_customer = Customer("John Doe", "john@example.com", "+1234567890", "123 Main St", "1990-01-01")
    customer_id = customer_manager.insert_customer(new_customer)

    if customer_id:
        account_manager = AccountManager()
        new_account = Account("Savings", 1000.00, customer_id)
        account_id = account_manager.insert_account(new_account)

        if account_id:
            print(f"New account created with ID: {account_id}")