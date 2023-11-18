from db_config.mysql import MysqlDB
from db_constants.common_functions import closeConnection, openConnection

class Vehicle():
  conn = None
  cursor = None

  # Funcion que hace la busqueda de la placa en la BD
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

  def load(self, per_page, current_page):
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
            vehicle_type_id,
            vehicles_type.name AS vehicle_type_name
            
          FROM vehicles
          INNER JOIN vehicles_type
          ON vehicles_type.id = vehicles.vehicle_type_id
          INNER JOIN status_type
          ON status_type.id = vehicles.status_type_id
          INNER JOIN access_type
          ON access_type.id = vehicles.access_type_id
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

  def get_total(self):
    openConnection(self, MysqlDB)
    try:
      query = """
          SELECT COUNT(*) AS total FROM vehicles;
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

  def get_access_types(self):
    openConnection(self, MysqlDB)
    try:
      query = """
          SELECT * FROM access_type;
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

  def get_status_types(self):
    openConnection(self, MysqlDB)
    try:
      query = """
          SELECT * FROM status_type;
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

  def get_vehicle_types(self):
    openConnection(self, MysqlDB)
    try:
      query = """
          SELECT * FROM vehicles_type;
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

  # Métodos CRUD
  def update(self, _id, plate_number, access_type_id, vehicle_type_id, status_type_id):
    openConnection(self, MysqlDB)
    try:
      # Rescatamos la data para luego compararla
      data = {
        'id': _id,
        'plate_number': plate_number,
        'access_type_id': access_type_id,
        'vehicle_type_id': vehicle_type_id,
        'status_type_id': status_type_id
      }
      # Si ya existe la cedula y no pertenece al mismo chofer entonces retornamos error
      query = """SELECT * FROM vehicles WHERE plate_number = %s"""
      params = (plate_number,)
      self.cursor.execute(query, params)
      result = self.cursor.fetchall()
      isSameVehicle = True
      if len(result) > 0:
        for vehicle in result:
          if vehicle['id'] != _id:
            isSameVehicle = False
      
      if isSameVehicle == False:
        return (False, {'error': 'Ya existe un vehículo con ese número de placa'})
      # Si la cedula pertenece al mismo chofer
      query = """
            UPDATE vehicles
            SET 
              plate_number = %s, 
              access_type_id = %s, 
              vehicle_type_id = %s, 
              status_type_id = %s
            WHERE id = %s
          """
      params = (plate_number, access_type_id, vehicle_type_id, status_type_id, _id)
      self.cursor.execute(query, params)
      # Si los datos enviados on diferentes se actualizará
      if self.cursor.rowcount > 0:
        self.conn.commit()
        return (True, {'message':'Vehículo actualizado correctamente'})  
      # Si no se actualiza verificamos que datos enviados sean iguales a los existentes
      keys = list(data.keys())
      totalKeys = len(keys)
      counter = 0
      for key in keys:
        if str(data[key]) == str(result[0][key]):
          counter = counter + 1
      if totalKeys == counter:
        return (True, {'message':'Vehículo actualizado correctamente'})
      # si se da un error al actualizar
      return (False, {'message':'Ha ocurrido un error al actualizar el registro'})
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      closeConnection(self)  

  def addNew(self, plate_number, access_type_id, vehicle_type_id, status_type_id):
    openConnection(self, MysqlDB)
    try:
      # Si ya existe la cedula en la bse datos entonces retornamos error
      query = """SELECT * FROM vehicles WHERE plate_number = %s"""
      params = (plate_number,)
      self.cursor.execute(query, params)
      result = self.cursor.fetchall()
      if len(result) > 0:
        return (False, {'error': 'Ya existe un vehículo con ese número de placa'})
      
      # Si la cedula no existe en la base de datos
      query = """
            INSERT INTO vehicles(plate_number, access_type_id, vehicle_type_id, status_type_id)
            VALUES(%s, %s, %s, %s)
          """
      params = (plate_number, access_type_id, vehicle_type_id, status_type_id,)
      self.cursor.execute(query, params)
      if self.cursor.rowcount > 0:
        self.conn.commit()
        return (True, {'message':'Vehículo agregado correctamente'})
      return (False, {'message':'Ha ocurrido un error al agregar el registro'})
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      closeConnection(self)  

  def delete(self, _id):
    openConnection(self, MysqlDB)
    try:
      # Si ya existe la cedula y no pertenece al mismo chofer entonces retornamos error
      query = """DELETE FROM vehicles WHERE id = %s"""
      params = (_id,)
      self.cursor.execute(query, params)
      if self.cursor.rowcount > 0:
        self.conn.commit()
        return (True, {'message':'Vehículo eliminado correctamente'})
      return (False, {'message':'Ha ocurrido un error al eliminar el registro'})
        
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      closeConnection(self) 

  # Métodos para filtrar en el datatables
  def filter(self, per_page, current_page, filter):
    openConnection(self, MysqlDB)
    try:
      # Seleccionamos usando el filtro
      query = """
          SELECT 
            vehicles.id AS id, 
            plate_number,
            status_type_id,
            status_type.name AS status_type_name,
            access_type_id,
            access_type.name AS access_type_name,
            vehicle_type_id,
            vehicles_type.name AS vehicle_type_name      
          FROM vehicles
          INNER JOIN vehicles_type
          ON vehicles_type.id = vehicles.vehicle_type_id
          INNER JOIN status_type
          ON status_type.id = vehicles.status_type_id
          INNER JOIN access_type
          ON access_type.id = vehicles.access_type_id
          WHERE
              vehicles.plate_number LIKE CONCAT('%', %s , '%')
              OR vehicles_type.name LIKE CONCAT('%', %s, '%')
              OR access_type.name LIKE CONCAT('%', %s, '%')
              OR status_type.name LIKE CONCAT('%', %s, '%')
          LIMIT %s OFFSET %s;
          """
      offset = (current_page - 1) * per_page
      params = (filter, filter, filter, filter, per_page, offset)
      self.cursor.execute(query, params)
      result = self.cursor.fetchall()
      print(result)
      if result == None:
        return (False, None)
      total = self.get_total_filtered(filter)
      if total[0] == True:
        total = total[1][0]
      return (True, result, total)
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      closeConnection(self)

  # Obtiene el total de registro que trae el filtro
  def get_total_filtered(self, filter):
    openConnection(self, MysqlDB)
    try:
      # Seleccionamos usando el filtro
      query = """
          SELECT COUNT(*) AS total
          FROM vehicles
          INNER JOIN vehicles_type
          ON vehicles_type.id = vehicles.vehicle_type_id
          INNER JOIN status_type
          ON status_type.id = vehicles.status_type_id
          INNER JOIN access_type
          ON access_type.id = vehicles.access_type_id
          WHERE
              vehicles.plate_number LIKE CONCAT('%', %s , '%')
              OR vehicles.vehicle_type_id LIKE CONCAT('%', %s, '%')
              OR vehicles.status_type_id LIKE CONCAT('%', %s, '%')
              OR vehicles.access_type_id LIKE CONCAT('%', %s, '%')
          """
      params = (filter, filter, filter, filter)
      self.cursor.execute(query, params)
      result = self.cursor.fetchall()
      if result == None:
        return (False, None)
      return (True, result)
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      closeConnection(self)

VehicleModel = Vehicle()