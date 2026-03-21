## Security Scan Results — 7 findings

### Finding 1: subprocess-shell-true
**What it is:** The code uses `subprocess.call()` with `shell=True`, which executes commands through the system shell. This allows shell injection attacks where malicious input can execute additional commands.
**Risk:** An attacker could inject malicious commands that get executed on the server with the application's privileges.
**Fix:**
```python
# Before (vulnerable)
subprocess.call(user_input, shell=True)

# After (secure)
subprocess.call(user_input.split(), shell=False)
# Or better yet, use a list directly:
subprocess.call(['command', 'arg1', 'arg2'], shell=False)
```

### Finding 2: insecure-hash-algorithm-md5
**What it is:** The code uses MD5 for hashing, which is cryptographically broken and vulnerable to collision attacks. MD5 should not be used for security purposes.
**Risk:** Attackers can generate hash collisions or reverse MD5 hashes, compromising data integrity and authentication.
**Fix:**
```python
# Before (vulnerable)
import hashlib
hash_value = hashlib.md5(data.encode()).hexdigest()

# After (secure)
import hashlib
hash_value = hashlib.sha256(data.encode()).hexdigest()
```

### Finding 3: hardcoded-password
**What it is:** A password is hardcoded directly in the source code as a string literal. This exposes the credential to anyone who can read the code.
**Risk:** Anyone with access to the source code can see the password, leading to unauthorized access.
**Fix:**
```python
# Before (vulnerable)
password = "admin123"

# After (secure)
import os
password = os.getenv('APP_PASSWORD')
# Set via environment variable: export APP_PASSWORD=your_secure_password
```

### Finding 4: hardcoded-password (api_key)
**What it is:** An API key is hardcoded directly in the source code, exposing this sensitive credential to anyone who can access the code.
**Risk:** Exposed API keys can be used by attackers to make unauthorized API calls, potentially incurring costs or accessing sensitive data.
**Fix:**
```python
# Before (vulnerable)
api_key = "sk-1234567890abcdef"

# After (secure)
import os
api_key = os.getenv('API_KEY')
# Set via environment variable: export API_KEY=your_api_key
```

### Finding 5: hardcoded-password (db_password)
**What it is:** A database password is hardcoded in the source code, making it visible to anyone who can read the code.
**Risk:** Database compromise leading to unauthorized access to all stored data and potential data breaches.
**Fix:**
```python
# Before (vulnerable)
db_password = "dbpass456"

# After (secure)
import os
db_password = os.getenv('DB_PASSWORD')
# Set via environment variable: export DB_PASSWORD=your_db_password
```

### Finding 6: sql-injection-format
**What it is:** The code constructs SQL queries using string formatting with user input, which allows attackers to inject malicious SQL code. This bypasses intended query logic.
**Risk:** Attackers can read, modify, or delete database records, potentially accessing all data or destroying the database.
**Fix:**
```python
# Before (vulnerable)
query = f"SELECT * FROM users WHERE username = '{user_input}'"
cursor.execute(query)

# After (secure)
query = "SELECT * FROM users WHERE username = %s"
cursor.execute(query, (user_input,))
```

### Finding 7: os-system-injection
**What it is:** The code uses `os.system()` which executes shell commands and is vulnerable to command injection if user input is included. It's similar to the subprocess issue but with a different function.
**Risk:** Attackers can execute arbitrary system commands on the server, potentially taking full control of the system.
**Fix:**
```python
# Before (vulnerable)
os.system(f"ls {user_directory}")

# After (secure)
import subprocess
subprocess.run(['ls', user_directory], shell=False, capture_output=True)
```