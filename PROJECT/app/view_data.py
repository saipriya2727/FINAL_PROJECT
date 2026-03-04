import sqlite3

# connect to database
conn = sqlite3.connect("../database/health.db")

cursor = conn.cursor()

print("------ USERS TABLE ------")

cursor.execute("SELECT * FROM users")

users = cursor.fetchall()

for user in users:
    print(user)

print("\n------ REPORTS TABLE ------")

cursor.execute("SELECT * FROM reports")

reports = cursor.fetchall()

for report in reports:
    print(report)

conn.close()