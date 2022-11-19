import sqlite3

# Create new database
conn = sqlite3.connect('LicensingManagementDB.db')

# Create Cursor to execute queries
cur = conn.cursor()

# Drop table from database
try:
    conn.execute('''Drop table Users''')
    # Save changes
    conn.commit()
    print('Users table dropped.')
except:
    print('Users table did not exist.')

# Create table in database
cur.execute('''CREATE TABLE Users(
Users_ID INTEGER PRIMARY KEY NOT NULL,
Username TEXT NOT NULL,
Password TEXT NOT NULL,
RoleLevel INTEGER NOT NULL);
''')

# Save changes
conn.commit()
print('Users Table created.')

# Users data
users = [(1, 'akanotz', 'akanotz', 1)]

# Insert bidders into table
cur.executemany("INSERT INTO Users VALUES (?, ?, ?, ?)", users)

# Save changes
conn.commit()

# Close database connection
conn.close()
print('Connection closed.')
