import mysql.connector
from mysql.connector import pooling
from config.env import mysql_config

class MysqlDB:
    config = None
    connection = None

    def __init__(self) -> None:
        self.config = mysql_config

    def connect(self):
        try:
            self.connection = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **self.config)
            conn = self.connection.get_connection()
            if conn.is_connected():
                print("Open connection")
                return conn
        except mysql.connector.Error as e:
            print(f"Error connecting to the database: {e}")
            return None

    def close_connection(self):
        if self.connection:
            try:
                self.connection.closeall()
                print("Connections closed")
            except mysql.connector.Error as e:
                print(f"Error closing connections: {e}")

