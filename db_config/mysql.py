import mysql.connector
from config.env import mysql_config

class MysqlDB:
    config=None

    def __init__(self) -> None:
        self.config = mysql_config

    def connect(self):
        try:
            connection = mysql.connector.connect(**self.config)
            if connection.is_connected():
                print("Open connection")
                return connection
        except mysql.connector.Error as e:
            print(f"Error connecting to the database: {e}")
            return None