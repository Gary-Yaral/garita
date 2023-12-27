import mysql.connector
from config.env import mysql_config
import mysql.connector.pooling as pooling

class MysqlDB:
    _pool = None
    pool_name = 'pool_querys' 

    @staticmethod
    def get_instance():
        if MysqlDB._pool is None:
            MysqlDB._pool = pooling.MySQLConnectionPool(pool_name=MysqlDB.pool_name, pool_size=5, **mysql_config)
        return MysqlDB._pool