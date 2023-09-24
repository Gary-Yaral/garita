from db_config.mysql import MysqlDB
from db_constants.common_functions import closeConnection, openConnection

class User():
  conn = None
  cursor = None

  def find_user(self, user):
    openConnection(self, MysqlDB)
    try:
      query = """
          SELECT *
          FROM user 
          WHERE user.username=%s"""
      params = (user,)
      self.cursor.execute(query, params)
      return self.cursor.fetchone()
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      closeConnection(self)

  def find_user_status(self, status_id):
    openConnection(self, MysqlDB)
    try:
      query = """
          SELECT *
          FROM user_status 
          WHERE user_status_id=%s"""
      params = (status_id,)
      self.cursor.execute(query, params)
      return self.cursor.fetchone()
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      closeConnection(self)

  def get_user_roles(self, user_id):
    openConnection(self, MysqlDB)
    try:
      query = """
          SELECT *
          FROM user_rol 
          INNER JOIN rol
          ON rol.rol_id = user_rol.fk_rol_id
          WHERE fk_user_id=%s"""
      params = (user_id,)
      self.cursor.execute(query, params)
      return self.cursor.fetchall()
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      print("en finnaly")
      closeConnection(self)
    
UserSystem = User()