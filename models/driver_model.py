from db_config.mysql import MysqlDB
from db_constants.common_functions import closeConnection, openConnection

class Driver():
  conn = None
  cursor = None

  def filter(self, per_page, current_page, filter):
    openConnection(self, MysqlDB)
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
      self.cursor.execute(query, params)
      result = self.cursor.fetchall()
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

  def get_total_filtered(self, filter):
    openConnection(self, MysqlDB)
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
      self.cursor.execute(query, params)
      result = self.cursor.fetchall()
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

  def get_types(self):
    openConnection(self, MysqlDB)
    try:
      query = """
          SELECT * FROM driver_type;
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

  def update(self, _id, dni, name, surname, type_id):
    openConnection(self, MysqlDB)
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
      self.cursor.execute(query, params)
      result = self.cursor.fetchall()
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
      self.cursor.execute(query, params)
      # Si los datos enviados on diferentes se actualizará
      if self.cursor.rowcount > 0:
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
      closeConnection(self)  

  def addNew(self, dni, name, surname, type_id):
    openConnection(self, MysqlDB)
    try:
      # Si ya existe la cedula en la bse datos entonces retornamos error
      query = """SELECT * FROM driver WHERE dni = %s"""
      params = (dni,)
      self.cursor.execute(query, params)
      result = self.cursor.fetchall()
      if len(result) > 0:
        return (False, {'error': 'Ya existe un usuario con ese número de cedula'})
      
      # Si la cedula no existe en la base de datos
      query = """
            INSERT INTO driver(dni, name, surname, drive_type_id)
            VALUES(%s, %s, %s, %s)
          """
      params = (dni, name, surname, type_id,)
      self.cursor.execute(query, params)
      if self.cursor.rowcount > 0:
        self.conn.commit()
        return (True, {'message':'Chofer agregado correctamente'})
      return (False, {'message':'Ha ocurrido un error al eliminar el registro'})
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      closeConnection(self)  

  def delete(self, _id):
    openConnection(self, MysqlDB)
    try:
      # Si ya existe la cedula y no pertenece al mismo chofer entonces retornamos error
      query = """DELETE FROM driver WHERE id = %s"""
      params = (_id,)
      self.cursor.execute(query, params)
      if self.cursor.rowcount > 0:
        self.conn.commit()
        return (True, {'message':'Chofer eliminado correctamente'})
      return (False, {'message':'Ha ocurrido un error al eliminar el registro'})
        
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      closeConnection(self)  

  
DriverModel = Driver()