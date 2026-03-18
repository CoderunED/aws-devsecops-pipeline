# Sample vulnerable Flask app
# Note: intentionally contains security flaws for scanning demo

import sqlite3
import os

# VULNERABILITY 1: Hardcoded secret key
SECRET_KEY = "hardcoded-secret-abc123"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"

# VULNERABILITY 2: SQL Injection
def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # dangerous: user input directly in query
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return cursor.fetchall()

# VULNERABILITY 3: Command injection
def ping_host(host):
    os.system("ping -c 1 " + host)

# VULNERABILITY 4: Weak comparison
def check_admin(password):
    if password == "admin123":
        return True
    return False

if __name__ == "__main__":
    print("app running")
