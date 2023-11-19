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

  def load(self, per_page, current_page):
    openConnection(self, MysqlDB)
    try:
      query = """
          SELECT 
          dni,
          surname,
          username,
          '' AS password,
          user.id As id,
          user.name AS name,
          fk_user_status_id AS user_status_id,
          user_status.status_name AS user_status_name
          FROM user
          INNER JOIN user_status
          ON user_status.user_status_id = user.fk_user_status_id 
          LIMIT %s OFFSET %s; """
      offset = (current_page - 1) * per_page
      params = (per_page, offset)
      self.cursor.execute(query, params)
      result = self.cursor.fetchall()
      if result == None:
        return (False, None)
      return (True, result)
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      closeConnection(self)

  def get_status_types(self):
    openConnection(self, MysqlDB)
    try:
      query = """
          SELECT 
            user_status_id AS id,
            status_name AS name
          FROM user_status;
          """
      params = ()
      self.cursor.execute(query, params)
      result = self.cursor.fetchall()
      if result == None:
        return (False, None)
      return (True, result)
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      closeConnection(self)

  def get_total(self):
    openConnection(self, MysqlDB)
    try:
      query = """
          SELECT COUNT(*) AS total FROM user;
          """
      params = ()
      self.cursor.execute(query, params)
      result = self.cursor.fetchone()
      if result == None:
        return (False, None)
      return (True, result)
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