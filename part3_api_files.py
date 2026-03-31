# Name: Maan Lo
# ID: 2511765
# Assignment: GA3 (Part 3)

# =========================================
# File I/O, APIs & Exception Handling
# =========================================

import requests
from datetime import datetime


# =========================
# Task 1 — File Read & Write
# =========================

print("\n=== Task 1: File Operations ===")

# Part A — Write: create file with 5 topics using write mode
with open("python_notes.txt", "w", encoding="utf-8") as f:
    f.write("Topic 1: Variables store data. Python is dynamically typed.\n")
    f.write("Topic 2: Lists are ordered and mutable.\n")
    f.write("Topic 3: Dictionaries store key-value pairs.\n")
    f.write("Topic 4: Loops automate repetitive tasks.\n")
    f.write("Topic 5: Exception handling prevents crashes.\n")

print("File written successfully.")

# Append two more lines using append mode
with open("python_notes.txt", "a", encoding="utf-8") as f:
    f.write("Topic 6: Functions improve code reuse.\n")
    f.write("Topic 7: APIs allow communication between systems.\n")

print("Lines appended.")

# Part B — Read: print each line numbered, strip trailing newline
with open("python_notes.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

print("\nFile Content:")
for i, line in enumerate(lines, 1):
    print(f"{i}. {line.strip()}")

# Count and print total lines
print(f"\nTotal lines: {len(lines)}")

# Keyword search — case-insensitive
keyword = input("\nEnter keyword to search: ").lower()
found = False
for line in lines:
    if keyword in line.lower():
        print(line.strip())
        found = True

if not found:
    print("No matching lines found.")


# =========================
# Task 2 — API Integration
# =========================

print("\n=== Task 2: API Integration ===")

BASE_URL = "https://dummyjson.com/products"

# Helper: log errors to file with timestamp
def log_error(context, error):
    with open("error_log.txt", "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR in {context}: {error}\n")

# Step 1 — Fetch and display 20 products in a formatted table
try:
    response = requests.get(BASE_URL + "?limit=20", timeout=5)
    data = response.json()

    # Print formatted table header
    print(f"\n{'ID':<4} | {'Title':<32} | {'Category':<14} | {'Price':>8} | {'Rating'}")
    print("-" * 75)

    for p in data["products"]:
        print(f"{p['id']:<4} | {p['title']:<32} | {p['category']:<14} | ${p['price']:>7.2f} | {p['rating']}")

    # Step 2 — Filter rating >= 4.5 and sort by price descending
    filtered = [p for p in data["products"] if p["rating"] >= 4.5]
    filtered.sort(key=lambda x: x["price"], reverse=True)

    print(f"\nFiltered Products (rating ≥ 4.5, sorted by price descending):")
    print(f"{'Title':<32} | {'Price':>8} | {'Rating'}")
    print("-" * 50)
    for p in filtered:
        print(f"{p['title']:<32} | ${p['price']:>7.2f} | {p['rating']}")

except requests.exceptions.ConnectionError as e:
    print("Connection failed. Please check your internet.")
    log_error("fetch_products", f"ConnectionError — {e}")

except requests.exceptions.Timeout as e:
    print("Request timed out. Try again later.")
    log_error("fetch_products", f"Timeout — {e}")

except Exception as e:
    print(f"Unexpected error: {e}")
    log_error("fetch_products", str(e))


# Step 3 — Fetch laptops by category
try:
    response = requests.get(BASE_URL + "/category/laptops", timeout=5)
    data = response.json()

    print(f"\nLaptops Available:")
    print(f"{'Title':<35} | {'Price':>8}")
    print("-" * 47)
    for p in data["products"]:
        print(f"{p['title']:<35} | ${p['price']:>7.2f}")

except requests.exceptions.ConnectionError as e:
    print("Connection failed. Please check your internet.")
    log_error("laptops_api", f"ConnectionError — {e}")

except requests.exceptions.Timeout as e:
    print("Request timed out. Try again later.")
    log_error("laptops_api", f"Timeout — {e}")

except Exception as e:
    print(f"Unexpected error: {e}")
    log_error("laptops_api", str(e))


# Step 4 — POST request to simulate creating a new product
try:
    response = requests.post(BASE_URL + "/add", json={
        "title": "My Custom Product",
        "price": 999,
        "category": "electronics",
        "description": "A product I created via API"
    }, timeout=5)

    result = response.json()
    print(f"\nPOST Response (simulated — DummyJSON test API):")
    print(f"  ID       : {result.get('id')}")
    print(f"  Title    : {result.get('title')}")
    print(f"  Price    : ${result.get('price')}")
    print(f"  Category : {result.get('category')}")

except requests.exceptions.ConnectionError as e:
    print("Connection failed. Please check your internet.")
    log_error("post_api", f"ConnectionError — {e}")

except requests.exceptions.Timeout as e:
    print("Request timed out. Try again later.")
    log_error("post_api", f"Timeout — {e}")

except Exception as e:
    print(f"Unexpected error: {e}")
    log_error("post_api", str(e))


# =========================
# Task 3 — Exception Handling
# =========================

print("\n=== Task 3: Exception Handling ===")

# Part A — Guarded calculator
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error: Cannot divide by zero"
    except TypeError:
        return "Error: Invalid input types"

print("\nPart A — safe_divide:")
print(f"  safe_divide(10, 2)     => {safe_divide(10, 2)}")
print(f"  safe_divide(10, 0)     => {safe_divide(10, 0)}")
print(f"  safe_divide('ten', 2)  => {safe_divide('ten', 2)}")


# Part B — Guarded file reader
def read_file_safe(filename):
    try:
        with open(filename, "r") as f:
            content = f.read()
        print(f"  File '{filename}' read successfully.")
        # Print the content so it is visible in output
        print(content)
        return content
    except FileNotFoundError:
        print(f"  Error: File '{filename}' not found.")
    finally:
        # Always runs whether file was found or not
        print("  File operation attempt complete.")

print("\nPart B — read_file_safe:")
read_file_safe("python_notes.txt")
read_file_safe("ghost_file.txt")


# Part C — Robust API calls are already handled in Task 2 above
# (each requests call is wrapped with ConnectionError, Timeout, Exception)

# Part D — Input validation loop for product lookup
print("\nPart D — Product Lookup Loop:")

while True:
    user_input = input("\nEnter a product ID to look up (1–100), or 'quit' to exit: ")

    if user_input.lower() == "quit":
        print("Exiting product lookup.")
        break

    # Validate: must be a digit
    if not user_input.isdigit():
        print("  ⚠ Invalid input! Please enter a whole number.")
        continue

    pid = int(user_input)

    # Validate: must be in range 1–100
    if pid < 1 or pid > 100:
        print("  ⚠ Out of range! Please enter a number between 1 and 100.")
        continue

    # Valid input — make API call
    try:
        res = requests.get(f"{BASE_URL}/{pid}", timeout=5)

        if res.status_code == 404:
            print(f"  Product ID {pid} not found.")
            log_error("lookup_product", f"HTTPError — 404 Not Found for product ID {pid}")
        elif res.status_code == 200:
            product = res.json()
            print(f"  Title : {product['title']}")
            print(f"  Price : ${product['price']:.2f}")
        else:
            print(f"  Unexpected status code: {res.status_code}")
            log_error("lookup_product", f"Unexpected status {res.status_code} for ID {pid}")

    except requests.exceptions.ConnectionError as e:
        print("  Connection failed. Please check your internet.")
        log_error("lookup_product", f"ConnectionError — {e}")

    except requests.exceptions.Timeout as e:
        print("  Request timed out. Try again later.")
        log_error("lookup_product", f"Timeout — {e}")

    except Exception as e:
        print(f"  Unexpected error: {e}")
        log_error("lookup_product", str(e))


# =========================
# Task 4 — Logging to File
# =========================

print("\n=== Task 4: Logging ===")

# Intentionally trigger a ConnectionError by using an unreachable URL
print("\nTriggering forced ConnectionError...")
try:
    requests.get("https://this-host-does-not-exist-xyz.com/api", timeout=5)
except requests.exceptions.ConnectionError as e:
    print("  Connection failed as expected.")
    log_error("forced_connection_error", f"ConnectionError — {e}")
except Exception as e:
    log_error("forced_connection_error", str(e))

# Intentionally trigger an HTTP 404 — checked via status_code, NOT try-except
# because a 404 is a valid HTTP response, not a Python exception
print("\nTriggering forced 404 (product ID 999)...")
try:
    res = requests.get(BASE_URL + "/999", timeout=5)
    if res.status_code != 200:
        print(f"  Received status {res.status_code} — logging error.")
        log_error("forced_404", f"HTTPError — 404 Not Found for product ID 999")
except Exception as e:
    log_error("forced_404", str(e))

# Read and print the full error log
print("\n=== Error Log (error_log.txt) ===")
try:
    with open("error_log.txt", "r") as f:
        log_content = f.read()
    print(log_content)
except FileNotFoundError:
    print("No error log found — no errors were recorded.")