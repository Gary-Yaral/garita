from db_config.mysql import conn
import mysql.connector
from db_constants.global_constants import VehicleStatus, RegisterType

class Register():
  conn = None
  cursor = None

  def __init__(self,):
    self.conn = conn

  def new_cursor(self):
    return self.conn.cursor(dictionary=True)

  def filter(self, per_page, current_page, filter):
    cursor = self.new_cursor()
    try:
      # Seleccionamos usando el filtro
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
          WHERE
              driver.name LIKE CONCAT('%', %s , '%')
              OR driver.surname LIKE CONCAT('%', %s, '%')
              OR driver.dni LIKE CONCAT('%', %s, '%')
              OR driver_type.name LIKE CONCAT('%', %s, '%')
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
    finally:
      cursor.close()

  def get_total_filtered(self, filter):
    cursor = self.new_cursor()
    try:
      # Seleccionamos usando el filtro
      query = """
          SELECT COUNT(*) AS total
          FROM driver
          INNER JOIN driver_type
          ON driver_type.id = driver.drive_type_id
          WHERE
              driver.name LIKE CONCAT('%', %s , '%')
              OR driver.surname LIKE CONCAT('%', %s, '%')
              OR driver.dni LIKE CONCAT('%', %s, '%')
              OR driver_type.name LIKE CONCAT('%', %s, '%');
          """
      params = (filter, filter, filter, filter)
      cursor.execute(query, params)
      result = cursor.fetchall()
      if not result:
        return (False, None)
      return (True, result)
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      cursor.close()

  def load(self, per_page, current_page):
    cursor = self.new_cursor()
    try:
      query = """
          SELECT 
            driver.dni,
            CONCAT(driver.name, ' ', driver.surname) AS driver_name,
            CONCAT(us.name, ' ', us.surname) AS username,
            vehicles.plate_number AS plate_number,
            atype.name AS access_type,
            rt.name AS register_type,
            vt.name AS vehicle_type,
            ar.kms,
            ar.observation,
            ar.destiny,
            ar.current_time AS registered_date
          FROM access_register AS ar
          INNER JOIN driver
          ON driver.id = ar.driver_id
          INNER JOIN vehicles
          ON vehicles.id = ar.vehicle_id
          INNER JOIN access_type AS atype
          ON atype.id = vehicles.access_type_id
          INNER JOIN `user` AS us
          ON us.id = ar.user_id
          INNER JOIN register_type AS rt
          ON rt.id = ar.register_type_id
          INNER JOIN vehicles_type AS vt
          ON vt.id = vehicles.vehicle_type_id
          LIMIT %s OFFSET %s;
          """
      offset = (current_page - 1) * per_page
      params = (per_page, offset)
      cursor.execute(query, params)
      result = cursor.fetchall()
      if not result:
        return (False, None)
      return (True, result)
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      cursor.close()

  def get_total(self):
    cursor = self.new_cursor()
    try:
      query = """
          SELECT COUNT(*) AS total FROM driver;
          """
      params = ()
      cursor.execute(query, params)
      result = cursor.fetchone()
      if not result:
        return (False, None)
      return (True, result)
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      cursor.close()

  def get_types(self):
    cursor = self.new_cursor()
    try:
      query = """
          SELECT * FROM driver_type;
          """
      params = ()
      cursor.execute(query, params)
      result = cursor.fetchall()
      if not result:
        return (False, None)
      return (True, result)
    except mysql.connector.Error as e:
      print("Error: {}".format(e))
    finally:
      cursor.close()

  def update(self, _id, dni, name, surname, type_id):
    cursor = self.new_cursor()
    try:
      # Rescatamos la data para luego compararla
      data = {
        'dni':dni, 
        'name':name, 
        'surname': surname, 
        'drive_type_id': type_id
      }
      # Si ya existe la cedula y no pertenece al mismo chofer entonces retornamos error
      query = """SELECT * FROM driver WHERE dni = %s"""
      params = (dni,)
      cursor.execute(query, params)
      result = cursor.fetchall()
      isSameDriver = True
      if len(result) > 0:
        for drive in result:
          if drive['id'] != _id:
            isSameDriver = False
      
      if isSameDriver == False:
        return (False, {'error': 'Ya existe un usuario con ese número de cedula'})
      # Si la cedula pertenece al mismo chofer
      query = """
            UPDATE driver
            SET 
              dni = %s, 
              name = %s, 
              surname = %s, 
              drive_type_id = %s
            WHERE id = %s
          """
      params = (dni, name, surname, type_id, _id)
      cursor.execute(query, params)
      # Si los datos enviados on diferentes se actualizará
      if cursor.rowcount > 0:
        self.conn.commit()
        return (True, {'message':'Chofer actualizado correctamente'})  
      # Si no se actualiza verificamos que datos enviados sean iguales a los existentes
      keys = list(data.keys())
      totalKeys = len(keys)
      counter = 0
      for key in keys:
        if str(data[key]) == str(result[0][key]):
          counter = counter + 1
      if totalKeys == counter:
        return (True, {'message':'Chofer actualizado correctamente'})
      # si se da un error al actualizar
      return (False, {'message':'Ha ocurrido un error al actualizar el registro'})
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      cursor.close()

  def addNew(self, driver_id, vehicle_id, user_id, kms, destiny, observation, status_type_id):
    cursor = self.new_cursor()
    print(VehicleStatus.DENTRO)
    try:
      query = """
        INSERT INTO access_register(
          driver_id, 
          vehicle_id, 
          user_id,
          kms,
          destiny,
          observation,
          register_type_id
        ) VALUES(%s, %s, %s, %s, %s, %s, %s)
        """
      params = ()
      register_type_id = 0
      if status_type_id == VehicleStatus.DENTRO:
        register_type_id = RegisterType.SALIDA
      
      if status_type_id == VehicleStatus.FUERA:
        register_type_id = RegisterType.SALIDA
        return (True, "va a ingresar")
      
      params = (driver_id, vehicle_id, user_id, kms, destiny, observation, register_type_id)
      cursor.execute(query, params)
      if cursor.rowcount > 0:
        self.conn.commit()
        return (True, {'message':'Registro agregado correctamente'})
      return (False, {'message':'Ha ocurrido un error al agregar el registro'})
    except Exception as e:
      print("Error: {}".format(e))
      return (False, {'error':'Ha ocurrido un error al agregar el registro'})
    finally:
      cursor.close()

  def delete(self, _id):
    cursor = self.new_cursor()
    try:
      # Si ya existe la cedula y no pertenece al mismo chofer entonces retornamos error
      query = """DELETE FROM driver WHERE id = %s"""
      params = (_id,)
      cursor.execute(query, params)
      if cursor.rowcount > 0:
        self.conn.commit()
        return (True, {'message':'Chofer eliminado correctamente'})
      return (False, {'message':'Ha ocurrido un error al eliminar el registro'})
        
    except Exception as e:
      print("Error: {}".format(e)) 
    finally:
      cursor.close()

  def get_home_arrival_data(self):
    cursor = self.new_cursor()
    try:
      # Si ya existe la cedula y no pertenece al mismo chofer entonces retornamos error
      query = """
        SELECT vt.name, COALESCE(COUNT(acr.vehicle_id), 0) AS total
        FROM vehicles_type AS vt
        LEFT JOIN (
            SELECT v.vehicle_type_id, acr.vehicle_id
            FROM access_register AS acr
            INNER JOIN vehicles AS v ON v.id = acr.vehicle_id
            WHERE DATE(acr.arrival_time) = DATE(CURRENT_TIMESTAMP())
        ) AS acr ON vt.id = acr.vehicle_type_id
        GROUP BY vt.name;"""
      
      
      params = ()
      cursor.execute(query, params)
      result = cursor.fetchall()
      if result: 
        return (True, result)
      return (False, None)
    except Exception as e:
      print("Error: {}".format(e)) 
      return (False, None)
    finally:
      cursor.close()

  def get_home_exit_data(self):
    cursor = self.new_cursor()
    try:
      # Si ya existe la cedula y no pertenece al mismo chofer entonces retornamos error
      query = """
        SELECT vt.name, COALESCE(COUNT(acr.vehicle_id), 0) AS total
        FROM vehicles_type AS vt
        LEFT JOIN (
            SELECT v.vehicle_type_id, acr.vehicle_id
            FROM access_register AS acr
            INNER JOIN vehicles AS v ON v.id = acr.vehicle_id
            WHERE DATE(acr.exit_time) = DATE(CURRENT_TIMESTAMP())
        ) AS acr ON vt.id = acr.vehicle_type_id
        GROUP BY vt.name;"""
      
      
      params = ()
      cursor.execute(query, params)
      result = cursor.fetchall()
      if result: 
        return (True, result)
      return (False, None)
    except Exception as e:
      print("Error: {}".format(e)) 
      return (False, None)
    finally:
      cursor.close()

  
RegisterModel = Register()