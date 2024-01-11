import mysql.connector


class DB:
    def __init__(self) -> None:
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "padang_app"
        self.port = 3307

        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
        )
