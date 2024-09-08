import sqlite3


class Person:
    def __init__(self, first_name='mohamed', last_name='hamdi', age=14, db_path='tutorial.db'):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        
        # Connect to the database
        try:
            self.con = sqlite3.connect(db_path)
            self.cursor = self.con.cursor()
            self.create_table()
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")

    def create_table(self):
        try:
            self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS person (
                Pid INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT,
                age INTEGER NOT NULL
            );
            """)
            self.con.commit()

        except sqlite3.Error as e:
            print(f"Error creating table: {e}")



    def select_person(self, first_name):
        try:
            self.cursor.execute("""
            SELECT * FROM person WHERE first_name=?
            """, (first_name,))
            
            rows = self.cursor.fetchall()
            if rows:
                self.first_name = rows[0][1]
                self.last_name = rows[0][2]
                self.age = rows[0][3]
                print(f"Person found: {self.first_name} {self.last_name}, Age: {self.age}")
            else:
                print("No person found with that name!")

        except sqlite3.Error as e:
            print(f"Error selecting person: {e}")



    def insert_person(self):
        try:
            self.cursor.execute("""
            INSERT INTO person (first_name, last_name, age) 
            VALUES (?, ?, ?)
            """, (self.first_name, self.last_name, self.age))
            self.con.commit()
            print(f"{self.first_name} {self.last_name} added successfully.")

        except sqlite3.Error as e:
            print(f"Error inserting person: {e}")


    def update_person(self, pid, first_name=None, last_name=None, age=None):
        try:
            # Build the update query dynamically
            updates = []
            values = []
            if first_name:
                updates.append("first_name = ?")
                values.append(first_name)
            if last_name:
                updates.append("last_name = ?")
                values.append(last_name)
            if age:
                updates.append("age = ?")
                values.append(age)

            values.append(pid)

            query = f"UPDATE person SET {', '.join(updates)} WHERE Pid = ?"
            self.cursor.execute(query, values)
            self.con.commit()
            print(f"Person with Pid {pid} updated successfully.")

        except sqlite3.Error as e:
            print(f"Error updating person: {e}")


    def delete_person(self, pid):
        try:
            self.cursor.execute("DELETE FROM person WHERE Pid = ?", (pid,))
            self.con.commit()
            print(f"Person with Pid {pid} deleted successfully.")

        except sqlite3.Error as e:
            print(f"Error deleting person: {e}")


    def list_all_people(self):
        try:
            self.cursor.execute("SELECT * FROM person")
            rows = self.cursor.fetchall()
            if rows:
                for row in rows:
                    print(f"Pid: {row[0]}, Name: {row[1]} {row[2]}, Age: {row[3]}")
            else:
                print("No people found.")

        except sqlite3.Error as e:
            print(f"Error listing people: {e}")


    def close_connection(self):
        try:
            self.con.close()
        except sqlite3.Error as e:
            print(f"Error closing the connection: {e}")



# Example usage:
p1 = Person("Ahmed", "Smith", 25)
p1.insert_person()

p1.select_person('Ahmed')

p1.update_person(pid=1, first_name="Ali", age=30)

p1.list_all_people()

p1.delete_person(pid=1)

p1.close_connection()
