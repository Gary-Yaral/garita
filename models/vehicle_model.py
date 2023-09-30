from db_config.mysql import MysqlDB
from db_constants.common_functions import closeConnection, openConnection

class Vehicle():
  conn = None
  cursor = None

  def find_vehicle(self, plate_number):
    openConnection(self, MysqlDB)
    try:
      query = """
          SELECT 
            vehicles.id AS id, 
            plate_number,
            status_type_id,
            status_type.name AS status_type_name,
            access_type_id,
            access_type.name AS access_type_name,
            status_type_id,
            status_type.name AS status_type_name
            
          FROM vehicles
          INNER JOIN vehicles_type
          ON vehicles_type.id = vehicles.vehicle_type_id
          INNER JOIN status_type
          ON status_type.id = vehicles.status_type_id
          INNER JOIN access_type
          ON access_type.id = vehicles.access_type_id
          WHERE vehicles.plate_number=%s"""
      params = (plate_number,)
      self.cursor.execute(query, params)
      result = self.cursor.fetchone()
      if result == None:
        return (False, None)
      return (True, result)
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      closeConnection(self)

    
VehicleModel = Vehicle()