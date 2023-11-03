from db_config.mysql import MysqlDB
from db_constants.common_functions import closeConnection, openConnection

class Driver():
  conn = None
  cursor = None

  def load(self, per_page, current_page):
    openConnection(self, MysqlDB)
    try:
      print(per_page, current_page)
      query = """
          SELECT 
            driver.id AS id, dni, 
            driver.drive_type_id AS type_id, 
            driver.name AS name, 
            driver_type.name AS type,
            surname
          FROM driver
          INNER JOIN driver_type
          ON driver_type.id = driver.drive_type_id
          LIMIT %s OFFSET %s;
          """
      offset = (current_page - 1) * per_page
      print(offset)
      print(per_page, offset)
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
  def get_total(self):
    openConnection(self, MysqlDB)
    try:
      query = """
          SELECT COUNT(*) AS total FROM driver;
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
    
DriverModel = Driver()