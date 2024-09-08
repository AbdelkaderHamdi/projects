import sqlite3 

class DatabaseManager:
    def __init__(self, db_path='bank.db'):
        self.db_path= db_path
        self.connection= None
        self.cursor = None
        self.connect_to_db()

    def connect_to_db(self): 
        try : 
            self.connection = sqlite3.connect(self.db_path)
            self.cursor= self.connection.cursor()
            print('Connected successfully.')
        except sqlite3.Error as e : 
            print(f'Error Connecting to database: {e}')
    
    def close_db(self): 
        if self.connection: 
            self.connection.close()
            print('Connection to database is closed.')

    def commit_db(self): 
        if self.connection: 
            self.connection.commit()
        

class Customers(DatabaseManager): 
    def __init__(self, full_name, email, phoneNumber, address, dateOfBirth , db_path='bank.db'):
        super().__init__(db_path)
        self.full_name= full_name
        self.email= email
        self.phoneNumber= phoneNumber
        self.address= address
        self.dateOfBirth= dateOfBirth
        self.create_customer_table()
      
    def create_customer_table(self):
        try: 
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS customer (
                                customerID INTEGER PRIMARY KEY AUTOINCREMENT, 
                                full_name TEXT NOT NULL ,
                                email TEXT NOT NULL , 
                                phoneNumber INTEGER NOT NULL , 
                                address TEXT NOT NULL , 
                                dateOfBirth DATE NOT NULL 
                                );
                                """)
            self.commit_db()

        except sqlite3.error as e : 
            print(f'Error Creating Table : {e}')

    def insert_customer(self): 
        try : 
            self.connection.execute("""
            INSERT INTO customers (full_name, email, phoneNumber, address, dateOfBirth)
            VALUES (?, ? , ? , ?, ?)""" , (self.full_name, self.email, self.phoneNumber, self.address, self.dateOfBirth))
            self.commit_db()
            print('Customer added successfully!')
        except sqlite3.Error as e : 
            print(f'Inserting customer Error : {e}')
    
    @classmethod
    def get_customerID_by_name(self, full_name): 
        try : 
            self.connection.execute("""
            SELECT customerID FROM customers WHERE full_name=? """ , (full_name))
            result= self.cursor.fetchone()
            if result: 
                return result[0]
            return None
        
        except sqlite3.Error as e : 
            print(f'Error fetching customerID: {e}')
            return None


class Accounts(DatabaseManager): 
    def __init__(self, account_type, balance, opened_date,customerID, status , db_path='bank.db'):
         super().__init__(db_path)
         self.account_type= account_type
         self.balance= balance
         self.opened_date= opened_date
         self.customerID = customerID
         self.status= status
         self.create_accounts_table()

    def create_accounts_table(self):
        try: 
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Accounts (
                                AccountID INTEGER PRIMARY KEY AUTOINCREMENT,
                                AccountType TEXT NOT NULL,
                                Balance REAL NOT NULL,
                                CustomerID INTEGER NOT NULL,
                                OpenedDate DATE,
                                Status TEXT NOT NULL,
                                FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
                                );
                                """)
            self.commit()
        except sqlite3.Error as e : 
            print(f'Error Creating Table : {e}')

    def insert_account(self): 
        try: 
            self.connection.execute("""
            INSERT INTO Accounts(AccountType, Balance, CustomerID, OpenedDate, Status)
            VALUES (? , ? , ? , ?, ? )""", (self.account_type, self.balance, self.customerID, self.opened_date, self.status))
            self.commit_db()
            print(f"Account for CustomerID {self.customer_id} added successfully!")
        except sqlite3.Error as e : 
            print(f'Inserting account Error : {e}')
        


 
 











