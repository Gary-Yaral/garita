import mysql.connector
from config.env import mysql_config
import mysql.connector.pooling as pooling

class MysqlDB:
    config = None
    connection_pool = None
    conn = None

    def __init__(self):
        self.config = mysql_config
        self.connection_pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **self.config)

    def connect(self):
        try:
            self.conn = self.connection_pool.get_connection()
            if self.conn.is_connected():
                print("Open connection")
                return self.conn
        except mysql.connector.Error as e:
            print(f"Error connecting to the database: {e}")
            return None

    def close_connection(self):
        if self.conn != None:
            try:
                conn.close()
                print("Connection closed")
            except mysql.connector.Error as e:
                print(f"Error closing connection: {e}")

    def close_all_connections(self):
        if self.connection_pool:
            try:
                self.connection_pool.close()
                print("All connections closed")
            except mysql.connector.Error as e:
                print(f"Error closing connections: {e}")


conn = MysqlDB().connect()