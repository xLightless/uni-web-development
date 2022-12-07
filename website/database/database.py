import mysql.connector

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password1",
    database = "horizon_travels"
)

class DatabaseHandler(object):
    def __init__(
        self,
        host:str = "localhost",
        user:str = "root",
        password:str = "password1",
        database:str = "horizon_travels"
    ):
    
        self.db = mysql.connector.connect(
            host = host,
            user = user,
            password = password,
            database = database
        )
        
        self.cursor = self.db.cursor()
        
        


# cursor = db.cursor()
# # cursor.execute("SELECT accountID, username, password, isEmailActivated, userType FROM ACCOUNT WHERE customerID - %s AND accountID - %s", (2, 2))
# cursor.execute("SELECT * FROM account")
# data = cursor.fetchall()
# print(data)