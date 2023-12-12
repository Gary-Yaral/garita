from db_config.mysql import conn

class Vehicle():
  conn = None
  cursor = None

  def __init__(self,):
    self.conn = conn

  def new_cursor(self):
    return self.conn.cursor(dictionary=True)

  def load(self, per_page, current_page):
    cursor = self.new_cursor()
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
      cursor.execute(query, params)
      result = cursor.fetchall()
      if not result:
        return (False, None)
      return (True, result)
    except Exception as e:
      print("Error: {}".format(e))
      return (False, None)
    finally:
      cursor.close()

  def get_total(self):
    cursor = self.new_cursor()
    try:
      query = """
          SELECT COUNT(*) AS total FROM vehicles;
          """
      params = ()
      cursor.execute(query, params)
      result = cursor.fetchone()
      if not result:
        return (False, None)
      return (True, result)
    except Exception as e:
      print("Error: {}".format(e))
      return (False, None)
    finally:
      cursor.close()
  
  # Funcion que hace la busqueda de la placa en la BD
  def find_vehicle(self, plate_number):
    cursor = self.new_cursor()
    try:
      query = """
          SELECT 
            vehicles.id AS id, 
            plate_number,
            status_type_id,
            access_type.name AS access_type_name,
            status_type.name AS status_type_name,
            vehicles_type.name AS vehicle_type_name,
            access_type_id,
            status_type_id,
            vehicles_type.id AS vehicle_type_id
          FROM vehicles
          INNER JOIN vehicles_type
          ON vehicles_type.id = vehicles.vehicle_type_id
          INNER JOIN status_type
          ON status_type.id = vehicles.status_type_id
          INNER JOIN access_type
          ON access_type.id = vehicles.access_type_id
          WHERE vehicles.plate_number=%s"""
      params = (plate_number,)
      cursor.execute(query, params)
      result = cursor.fetchone()
      if not result:
        return (False, None)
      return (True, result)
    except Exception as e:
      print("Error: {}".format(e))
      return (False, None)
    finally:
      cursor.close()

  def load_access_type(self):
    cursor = self.new_cursor()
    try:
      query = """
          SELECT * from access_type
            """
      cursor.execute(query)
      result = cursor.fetchall()
      if not result:
        return {"loaded": False }
      return {"loaded": True, "data": result}
    except Exception as e:
      print("Error: {}".format(e))
      {"loaded": False }
    finally:
      cursor.close()

  def load_status_type(self):
    cursor = self.new_cursor()
    try:
      query = """
          SELECT * from status_type
            """
      cursor.execute(query)
      result = cursor.fetchall()
      if not result:
        {"loaded": False }
      return {"loaded": True, "data": result}
    except Exception as e:
      print("Error: {}".format(e))
      {"loaded": False }
    finally:
      cursor.close()

  def load_vehicles_type(self):
    cursor = self.new_cursor()
    try:
      query = """
          SELECT * from vehicles_type
            """
      cursor.execute(query)
      result = cursor.fetchall()
      if not result:
        {"loaded": False }
      return {"loaded": True, "data": result}
    except Exception as e:
      print("Error: {}".format(e))
      {"loaded": False }
    finally:
      cursor.close()
  
  # Consulta datos para formulario de nuevo registro de accesso o salida
  def load_required_data(self):
    try:
      access_types = self.load_access_type()
      status_types = self.load_status_type()
      vehicles_types = self.load_vehicles_type()
      data = {
        "vehicles_types": (),
        "status_types": (),
        "access_types": ()
      } 
      if access_types["loaded"]:
        data["access_types"] = access_types["data"]
      
      if status_types["loaded"]:
        data["status_types"] = status_types["data"]

      if vehicles_types["loaded"]:
        data["vehicles_types"] = vehicles_types["data"]

      return (True, data)
    except Exception as e:
      print("Error: {}".format(e))
      return (False, None)

  # Métodos CRUD
  def update(self, _id, plate_number, access_type_id, vehicle_type_id, status_type_id):
    cursor = self.new_cursor()
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
      cursor.execute(query, params)
      result = cursor.fetchall()
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
      cursor.execute(query, params)
      # Si los datos enviados on diferentes se actualizará
      if cursor.rowcount > 0:
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
      cursor.close()

  def addNew(self, plate_number, access_type_id, vehicle_type_id, status_type_id):
    cursor = self.new_cursor()
    try:
      # Si ya existe la cedula en la bse datos entonces retornamos error
      query = """SELECT * FROM vehicles WHERE plate_number = %s"""
      params = (plate_number,)
      cursor.execute(query, params)
      result = cursor.fetchall()
      if len(result) > 0:
        return (False, {'error': 'Ya existe un vehículo con ese número de placa'})
      
      # Si la cedula no existe en la base de datos
      query = """
            INSERT INTO vehicles(plate_number, access_type_id, vehicle_type_id, status_type_id)
            VALUES(%s, %s, %s, %s)
          """
      params = (plate_number, access_type_id, vehicle_type_id, status_type_id,)
      cursor.execute(query, params)
      if cursor.rowcount > 0:
        self.conn.commit()
        return (True, {'message':'Vehículo agregado correctamente'})
      return (False, {'message':'Ha ocurrido un error al agregar el registro'})
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      cursor.close()

  def delete(self, _id):
    cursor = self.new_cursor()
    try:
      # Si ya existe la cedula y no pertenece al mismo chofer entonces retornamos error
      query = """DELETE FROM vehicles WHERE id = %s"""
      params = (_id,)
      cursor.execute(query, params)
      if cursor.rowcount > 0:
        self.conn.commit()
        return (True, {'message':'Vehículo eliminado correctamente'})
      return (False, {'message':'Ha ocurrido un error al eliminar el registro'})
        
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      cursor.close()

  # Métodos para filtrar en el datatables
  def filter(self, per_page, current_page, filter):
    cursor = self.new_cursor()
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
      cursor.execute(query, params)
      result = cursor.fetchall()
      if not result:
        return (False, None)
      total = self.get_total_filtered(filter)
      if total[0] == True:
        total = total[1][0]
      return (True, result, total)
    except Exception as e:
      print("Error: {}".format(e))
      return (False, None)
    finally:
      cursor.close()
      
  # Obtiene el total de registro que trae el filtro
  def get_total_filtered(self, filter):
    cursor = self.new_cursor()
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
      cursor.execute(query, params)
      result = cursor.fetchall()
      if not result:
        return (False, None)
      return (True, result)
    except Exception as e:
      print("Error: {}".format(e))
      return (False, None)
    finally:
      cursor.close()

VehicleModel = Vehicle()