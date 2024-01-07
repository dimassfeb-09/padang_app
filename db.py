import mysql.connector

class DB():
    
    def __init__(self) -> None:
        host = "localhost"
        user = "root"
        password = "Aa11bb22_"
        database = "padang_app"

        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        
        
