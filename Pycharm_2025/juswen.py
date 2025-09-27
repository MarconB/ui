import mysql.connector
import os
from mysql.connector.errors import IntegrityError

def get_choice(choices):
    while True:
        try:
            choice = int(input('Select: '))
            if choice in choices:
                return choice
        except ValueError:
            pass
        print('-> Invalid input. Try again.')
def clear():
    os.system('cls')

class Database:
    def __init__(self):
        self.db = mysql.connector.connect(host='localhost',user='root',password='Josh_SQL.019',database='logindb')
        self.cursor = self.db.cursor()

    def create_table(self):
        query = """ CREATE TABLE IF NOT EXISTS users(
                    user_id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(50) NOT NULL )"""
        self.cursor.execute(query)
        self.db.commit()

    def db_sign_in(self, username, password):
        query = "INSERT INTO users (username, password) VALUES (%s, %s) "
        self.cursor.execute(query, (username,password))
        self.db.commit()

    def db_log_in(self,username,password):
        query = "SELECT username, password FROM users WHERE username=%s and password=%s  "
        self.cursor.execute(query, (username, password))
        return self.cursor.fetchone()

    def db_view_users(self):
        query = " SELECT * FROM USERS "
        self.cursor.execute(query)
        return self.cursor.fetchall()

class Users:
    def __init__(self, db):
        self.database = db

    def sign_in(self):
        clear()
        print('SIGN NEW USER')
        while True:
            username = input("Username: ")
            password = input("Password: ")
            if username  == '' or password == '':
                print("-> Username or Password cannot be empty.")
                continue
            try:
                self.database.db_sign_in(username,password)
                break
            except IntegrityError:
                print('-> User already taken.')

    def log_in(self):
        clear()
        print("Log In Account")
        username = input("Username: ")
        password = input("Password: ")
        user = self.database.db_log_in(username, password)
        if user:
            print(f'Welcome {user[0]}!')
        else:
            print("-> Invalid username or password.")

    def view_users(self):
        clear()
        print("All users")
        rows = self.database.db_view_users()
        for index, row in enumerate(rows,1):
            print(f'{index}. {row[1]}')

def main():
    db = Database()
    user = Users(db)
    db.create_table()
    while True:
        print("WELCOME TO PISBOK\n1.Log in\n2.Sign in\n3.View Users\n4.Exit")
        choice1 = get_choice([1, 2, 3, 4])
        match choice1:
            case 1:
                user.log_in()
            case 2:
                user.sign_in()
            case 3:
                user.view_users()
            case 4:
                exit("Goodbye!")

if __name__ == "__main__":
    main()