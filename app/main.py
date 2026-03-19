# intentionally vulnerable app — for security scanning demo

import sqlite3
import os
import subprocess
import hashlib

# VULN 1: Hardcoded credentials (semgrep: generic.secrets)

GITHUB_TOKEN = "ghp_fakeTok3nForDemoOnly12345678901"
password = "supersecret123"
api_key = "AKIAIOSFODNN7EXAMPLE3"
db_password = "admin:password123@localhost"

# VULN 2: SQL injection (semgrep: python.lang.security.audit.sqli)
def get_user(user_input):
    conn = sqlite3.connect("test.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE name = '%s'" % user_input)
    return cur.fetchall()

# VULN 3: OS command injection (semgrep: python.lang.security.audit.subprocess)
def run_command(user_input):
    os.system("ls " + user_input)
    subprocess.call("ping " + user_input, shell=True)

# VULN 4: Weak hashing (semgrep: python.lang.security.audit.md5)
def hash_password(pwd):
    return hashlib.md5(pwd.encode()).hexdigest()

# VULN 5: Hardcoded AWS key pattern
AWS_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
```
