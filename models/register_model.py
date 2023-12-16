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
            ar.id AS id,
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
            DATE_FORMAT(ar.current_time, '%Y-%m-%d %H:%i') AS registered_date
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
           WHERE
              driver.dni LIKE CONCAT('%', %s , '%')
              OR driver.name LIKE CONCAT('%', %s , '%')
              OR driver.surname LIKE CONCAT('%', %s , '%')
              OR us.name LIKE CONCAT('%', %s , '%')
              OR us.surname LIKE CONCAT('%', %s , '%')
              OR vehicles.plate_number LIKE CONCAT('%', %s, '%')
              OR atype.name LIKE CONCAT('%', %s , '%')
              Or rt.name LIKE CONCAT('%', %s , '%')
              OR vt.name LIKE CONCAT('%', %s , '%')
              OR ar.kms LIKE CONCAT('%', %s , '%')
              OR ar.observation LIKE CONCAT('%', %s , '%')
              OR ar.destiny LIKE CONCAT('%', %s , '%')
              OR ar.current_time LIKE CONCAT('%', %s , '%')
          LIMIT %s OFFSET %s;
          """
      offset = (current_page - 1) * per_page
      params = (
        filter, 
        filter, 
        filter, 
        filter, 
        filter, 
        filter, 
        filter, 
        filter, 
        filter, 
        filter, 
        filter, 
        filter, 
        filter,
        per_page, 
        offset
      )
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
           WHERE
              driver.dni LIKE CONCAT('%', %s , '%')
              OR driver.name LIKE CONCAT('%', %s , '%')
              OR driver.surname LIKE CONCAT('%', %s , '%')
              OR us.name LIKE CONCAT('%', %s , '%')
              OR us.surname LIKE CONCAT('%', %s , '%')
              OR vehicles.plate_number LIKE CONCAT('%', %s, '%')
              OR atype.name LIKE CONCAT('%', %s , '%')
              Or rt.name LIKE CONCAT('%', %s , '%')
              OR vt.name LIKE CONCAT('%', %s , '%')
              OR ar.kms LIKE CONCAT('%', %s , '%')
              OR ar.observation LIKE CONCAT('%', %s , '%')
              OR ar.destiny LIKE CONCAT('%', %s , '%')
              OR ar.current_time LIKE CONCAT('%', %s , '%')
          """
      params = (
        filter, 
        filter, 
        filter, 
        filter, 
        filter, 
        filter, 
        filter, 
        filter, 
        filter, 
        filter, 
        filter, 
        filter, 
        filter
      )
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
            ar.id AS id,
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
            DATE_FORMAT(ar.current_time, '%Y-%m-%d %H:%i') AS registered_date
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
          SELECT COUNT(*) AS total FROM access_register;
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

  def update(self, driver_id, kms, destiny, observation, _id):
    cursor = self.new_cursor()
    try:
      # Rescatamos la data para luego compararla
      data = {
        'driver_id':driver_id, 
        'kms':kms, 
        'destiny': destiny, 
        'observation':observation 
      }
      # Si ya existe la cedula y no pertenece al mismo chofer entonces retornamos error
      query = """SELECT * FROM access_register WHERE id = %s"""
      params = (_id,)
      cursor.execute(query, params)
      found_register = cursor.fetchall()

      # Actualizamos los datos
      query = """
        UPDATE access_register SET
          driver_id = %s,  
          kms = %s,
          destiny = %s,
          observation = %s
        WHERE id = %s
        """
      params = (driver_id, kms, destiny, observation, _id)
      cursor.execute(query, params)
      # Si los datos enviados on diferentes se actualizará
      if cursor.rowcount > 0:
        self.conn.commit()
        return (True, {'message':'Registro actualizado correctamente'})  
      # Si no se actualiza verificamos que datos enviados sean iguales a los existentes
      print(found_register)
      keys = list(data.keys())
      totalKeys = len(keys)
      counter = 0
      for key in keys:
        if str(data[key]) == str(found_register[0][key]):
          counter = counter + 1
      if totalKeys == counter:
        return (True, {'message':'Registro actualizado correctamente'})
      # si se da un error al actualizar
      return (False, {'message':'Ha ocurrido un error al actualizar el registro'})
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      cursor.close()

  def addNew(self, driver_id, vehicle_id, user_id, kms, destiny, observation, status_type_id):
    cursor = self.new_cursor()
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
      new_status_id = 0
      if status_type_id == VehicleStatus.DENTRO:
        register_type_id = RegisterType.SALIDA
        new_status_id = VehicleStatus.FUERA
      
      if status_type_id == VehicleStatus.FUERA:
        register_type_id = RegisterType.ENTRADA     
        new_status_id = VehicleStatus.DENTRO
      params = (driver_id, vehicle_id, user_id, kms, destiny, observation, register_type_id)
      cursor.execute(query, params)
      if cursor.rowcount > 0:
        self.conn.commit()
        if self.update_status(new_status_id, vehicle_id):
          return (True, {'message':'Registro agregado correctamente'})
        else:
          return (False, {'message':'Ha ocurrido un error al editar el estado del vehículo'})
      return (False, {'message':'Ha ocurrido un error al agregar el registro'})
    except Exception as e:
      print("Error: {}".format(e))
      return (False, {'error':'Ha ocurrido un error al agregar el registro'})
    finally:
      cursor.close()

  # Actualiza el estado del vehiculo en cada registro 
  def update_status(self, new_status_id, _id):
    cursor = self.new_cursor()
    try:
      query = """
        UPDATE vehicles
        SET status_type_id=%s
        WHERE id = %s;
        """
      params = (new_status_id, _id)
      cursor.execute(query, params)
      if cursor.rowcount > 0:
        self.conn.commit()
        return (True, {'message':'Estado actualizado correctamente'})
      return (False, {'message':'Ha ocurrido un error al actualizar el estado del vehículo'})
    except Exception as e:
      print("Error: {}".format(e))
      return (False, {'error':'Ha ocurrido un error al agregar el registro'})
    finally:
      cursor.close()

  def delete(self, _id):
    cursor = self.new_cursor()
    try:
      # Si ya existe la cedula y no pertenece al mismo chofer entonces retornamos error
      query = """DELETE FROM access_register WHERE id = %s"""
      params = (_id,)
      cursor.execute(query, params)
      if cursor.rowcount > 0:
        self.conn.commit()
        return (True, {'message':'Registro eliminado correctamente'})
      return (False, {'message':'Ha ocurrido un error al eliminar el registro'})
        
    except Exception as e:
      print("Error: {}".format(e)) 
      return (False, {'error':'Ha ocurrido un error al eliminar el registro'})
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
            WHERE DATE(acr.current_time) = DATE(CURRENT_TIMESTAMP()) AND register_type_id = %s
        ) AS acr ON vt.id = acr.vehicle_type_id
        GROUP BY vt.name;"""
      
      
      params = (RegisterType.ENTRADA,)
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
            WHERE DATE(acr.current_time) = DATE(CURRENT_TIMESTAMP()) AND register_type_id = %s
        ) AS acr ON vt.id = acr.vehicle_type_id
        GROUP BY vt.name;"""
      
      
      params = (RegisterType.SALIDA,)
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

  def get_register(self, _id):
    cursor = self.new_cursor()
    try:
      # Si ya existe la cedula y no pertenece al mismo chofer entonces retornamos error
      query = """
        SELECT ar.id, ar.destiny, ar.kms, ar.observation, driver.dni, vehicles.plate_number FROM access_register as ar
        INNER JOIN vehicles
        ON vehicles.id = ar.vehicle_id 
        INNER JOIN driver
        ON driver.id = ar.driver_id
        WHERE ar.id = %s"""
      params = (_id,)
      cursor.execute(query, params)
      result = cursor.fetchone()
      if result: 
        return (True, result)
      return (False, None)
    except Exception as e:
      print("Error: {}".format(e)) 
      return (False, None)
    finally:
      cursor.close()
  
RegisterModel = Register()