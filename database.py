import sqlite3
import hashlib

def create_table():
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    # Table for user spending
    c.execute('''CREATE TABLE IF NOT EXISTS expenses
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  date TEXT, category TEXT, description TEXT, 
                  amount REAL, username TEXT)''')
    
    # Table for user accounts
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

# Helper to hash passwords for security
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

def add_user(username, password):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("INSERT INTO users(username, password) VALUES (?,?)", (username, make_hashes(password)))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username =? AND password =?", (username, make_hashes(password)))
    data = c.fetchall()
    conn.close()
    return data

def add_expense(date, category, description, amount, username):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    c.execute("INSERT INTO expenses (date, category, description, amount, username) VALUES (?, ?, ?, ?, ?)",
              (date, category, description, amount, username))
    conn.commit()
    conn.close()

def get_expenses(username):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    # Only fetch data belonging to the specific user session
    c.execute("SELECT * FROM expenses WHERE username = ?", (username,))
    data = c.fetchall()
    conn.close()
    return data

def delete_expense(expense_id, username):
    conn = sqlite3.connect("expenses.db")
    c = conn.cursor()
    # Security: Ensure the user can only delete their own data
    c.execute("DELETE FROM expenses WHERE id = ? AND username = ?", (expense_id, username))
    conn.commit()
    conn.close()
