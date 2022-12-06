import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password1",
    database = "horizon_travels"
)



# cursor.execute("""
#                SHOW COLUMNS FROM horizon_travels.customer;
# """)

# cursor.execute("INSERT INTO account (username, password, isEmailActivated, userType) VALUES (%s, %s, %s, %s)",
#                ("lightless", "password1", 0, "admin")
# )

# db.commit()

# cursor.execute('SELECT * FROM horizon_travels;')

# for x in cursor:
#     print(x)
