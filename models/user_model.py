import mysql.connector
from db_config.mysql import MysqlDB
from db_constants.common_functions import closeConnection, openConnection
from pwd_md.pass_config import hash_password

DEFAULT_ROL_ID = 2
ADMIN_STATUS_ID = 3
ADMIN_ROL_ID = 1

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
          user_status.status_name AS user_status_name,
          rol_name,
          rol_id
          FROM user
          INNER JOIN user_status
          ON user_status.user_status_id = user.fk_user_status_id 
          INNER JOIN user_rol
          ON user_rol.fk_user_id = user.id
          INNER JOIN rol
          ON user_rol.fk_rol_id = rol.rol_id
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
          FROM user_status
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
  
    # Métodos CRUD
  
  def update(self, _id, dni, name, surname, username, password, status):
    openConnection(self, MysqlDB)
    try:
      # Rescatamos la data para luego compararla
      data = {
        'id': _id,
        'dni': dni,
        'name': name,
        'surname': surname,
        'password': password,
        'fk_user_status_id': status
      }

      # Si ya existe la cedula en la base datos entonces retornamos error
      query = """SELECT * FROM user WHERE dni = %s"""
      params = (dni,)
      self.cursor.execute(query, params)
      result = self.cursor.fetchall()
      if len(result) > 0:
        isSame = False
        for data in result:
          if data['id'] == _id:
            isSame = True
        if not isSame:
          return (False, {'error': 'Ya existe un usuario con ese número de cédula'})
      
       # Si ya existe el nombre de usuario en la bse datos entonces retornamos error
      query = """SELECT * FROM user WHERE username = %s"""
      params = (username,)
      self.cursor.execute(query, params)
      result = self.cursor.fetchall()
      if len(result) > 0:
        isSame = False
        for data in result:
          if data['id'] == _id:
            isSame = True
        if not isSame:
          return (False, {'error': 'Ya existe ese nombre de usuario'})

      # Creamos la query de actualizacion 
      query = """
        UPDATE user
        SET 
          dni = %s, 
          name = %s, 
          surname = %s, 
          username = %s,  
          fk_user_status_id = %s
        WHERE id = %s
      """
      params = (dni, name, surname, username, status, _id)
      # Si no envian contraseña
      if password != '':
        encryptedPass = hash_password(password)
        params = (dni, name, surname, username, encryptedPass, status, _id)
        query = """
          UPDATE user
          SET 
            dni = %s, 
            name = %s, 
            surname = %s, 
            username = %s,  
            password = %s,
            fk_user_status_id = %s
          WHERE id = %s
        """
  
      self.cursor.execute(query, params)
      # Si los datos enviados on diferentes se actualizará
      if self.cursor.rowcount > 0:
        self.conn.commit()
        return (True, {'message':'Usuario actualizado correctamente'})  
      # Si no se actualiza verificamos que datos enviados sean iguales a los existentes
      keys = list(data.keys())
      totalKeys = len(keys)
      counter = 0
      for key in keys:
        print(str(data[key]))
        print(str(data[key]) == str(result[0][key]))
        if str(data[key]) == str(result[0][key]):
          counter = counter + 1
      if totalKeys == counter:
        return (True, {'message':'Usuario actualizado correctamente'})
      # si se da un error al actualizar
      return (False, {'message':'Ha ocurrido un error al actualizar el registro'})
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      closeConnection(self)  

  def delete(self, _id):
    openConnection(self, MysqlDB)
    try:
      # mensaje satisfactorio
      result_ok = (True, {'message':'Usuario eliminado correctamente'})
      result_err = (False, {'message':'Ha ocurrido un error al eliminar el registro'})

       # Verificamos que no sea administrador y lo eliminamos
      query = """SELECT fk_rol_id AS rol_id FROM user_rol WHERE fk_user_id = %s"""
      params = (_id,)
      self.cursor.execute(query, params)
      result = self.cursor.fetchall()
      if len(result) > 0:
        if result[0]['rol_id'] != ADMIN_ROL_ID:
          query = """DELETE FROM user WHERE id = %s"""
          params = (_id,)
          self.cursor.execute(query, params)
          if self.cursor.rowcount > 0:
            self.conn.commit()
            return result_ok
          return result_err
        
      # Si es administrador verificamos que no sea el ultimo administrador
      query = """SELECT * FROM user_rol WHERE fk_rol_id = %s"""
      params = (ADMIN_ROL_ID,)
      self.cursor.execute(query, params)
      result = self.cursor.fetchall()
      if len(result) > 1 :
        query = """DELETE FROM user WHERE id = %s"""
        params = (_id,)
        self.cursor.execute(query, params)
        if self.cursor.rowcount > 0:
          self.conn.commit()
          return result_ok
        return result_err
      
      return (False, {'error': 'Este usuario es el único administrador y no se puede borrar'})
        
    except mysql.connector.Error as e:
      print("Error: {}".format(e))
      if e.errno == 1451:
        return (False, {'error':'No es posible eliminar el registro, tiene registros vinculados'})
    finally:
      closeConnection(self) 
  
  # Métodos para filtrar en el datatables
  def filter(self, per_page, current_page, filter):
    openConnection(self, MysqlDB)
    try:
      # Seleccionamos usando el filtro
      query = """
          SELECT 
          dni,
          surname,
          username,
          '' AS password,
          user.id As id,
          user.name AS name,
          fk_user_status_id AS user_status_id,
          user_status.status_name AS user_status_name,
          rol_name,
          rol_id
          FROM user
          INNER JOIN user_status
          ON user_status.user_status_id = user.fk_user_status_id 
          INNER JOIN user_rol
          ON user_rol.fk_user_id = user.id
          INNER JOIN rol
          ON rol.rol_id = user_rol.fk_rol_id
          WHERE
              user.dni LIKE CONCAT('%', %s , '%')
              OR user.name LIKE CONCAT('%', %s , '%')
              OR user.surname LIKE CONCAT('%', %s , '%')
              OR user.username LIKE CONCAT('%', %s, '%')
              OR user_status.status_name LIKE CONCAT('%', %s, '%')
              OR rol.rol_name LIKE CONCAT('%', %s, '%')
          LIMIT %s OFFSET %s;
          """
      offset = (current_page - 1) * per_page
      params = (filter, filter, filter, filter, filter, filter, per_page, offset)
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

  # Obtiene el total de registro que trae el filtro
  def get_total_filtered(self, filter):
    openConnection(self, MysqlDB)
    try:
      # Seleccionamos usando el filtro
      query = """
          SELECT COUNT(*) AS total
          FROM user
          INNER JOIN user_status
          ON user_status.user_status_id = user.fk_user_status_id
          WHERE
              user.dni LIKE CONCAT('%', %s , '%')
              OR user.name LIKE CONCAT('%', %s , '%')
              OR user.surname LIKE CONCAT('%', %s , '%')
              OR user.username LIKE CONCAT('%', %s, '%')
              OR user_status.status_name LIKE CONCAT('%', %s, '%');
          """
      params = (filter, filter, filter, filter, filter)
      self.cursor.execute(query, params)
      result = self.cursor.fetchall()
      if result == None:
        return (False, None)
      return (True, result)
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      closeConnection(self)

  def add_new(self, dni, name, surname, username, password, status, rol_id):
    openConnection(self, MysqlDB)
    try:
      # Si ya existe la cedula en la bse datos entonces retornamos error
      query = """SELECT * FROM user WHERE dni = %s"""
      params = (dni,)
      self.cursor.execute(query, params)
      result = self.cursor.fetchall()
      if len(result) > 0:
        return (False, {'error': 'Ya existe un usuario con ese número de cédula'})
      
       # Si ya existe el nombre de usuario en la bse datos entonces retornamos error
      query = """SELECT * FROM user WHERE BINARY username = %s"""
      params = (username,)
      self.cursor.execute(query, params)
      result = self.cursor.fetchall()
      if len(result) > 0:
        return (False, {'error': 'Ya existe ese nombre de usuario'})
      
      # Agregmos solo si la cedula y el nombre de usuario no existen en la BD
      query = """
            INSERT INTO user(dni, name, surname, username, password, fk_user_status_id)
            VALUES(%s, %s, %s, %s, %s, %s)
          """
      encryptedPass = hash_password(password)
      params = (dni, name, surname, username, encryptedPass, status)
      self.cursor.execute(query, params)
      if self.cursor.rowcount > 0:
        self.conn.commit()
        result = self.add_role(dni, rol_id)
        if result[0] == True:
          return (True, {'message':'Usuario agregado correctamente'})
        return (False, {'message':'Ha ocurrido un error al agregar el rol al usuario'})
      return (False, {'message':'Ha ocurrido un error al agregar el registro'})
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      closeConnection(self)  

  def add_role(self, dni, rol_id):
    openConnection(self, MysqlDB)
    try:
      # Buscamos el usuario que se acaba de registrar con su dni
      query = """SELECT * FROM user WHERE dni = %s"""
      params = (dni,)
      self.cursor.execute(query, params)
      result = self.cursor.fetchall()
      if len(result) > 0: 
        user_id = result[0]["id"]
        query = """INSERT INTO user_rol(fk_rol_id,
          fk_user_id) VALUES(%s, %s)"""
        params = (rol_id, user_id)
        self.cursor.execute(query, params)
        result = self.cursor.fetchall()      
      if self.cursor.rowcount > 0:
        self.conn.commit()
        return (True, {'message':'Rol agregado correctamente al usuario'})
      return (False, {'message':'Ha ocurrido un error al agregar el registro'})
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      closeConnection(self)

  def get_roles(self):
    openConnection(self, MysqlDB)
    try:
      # Buscamos el usuario que se acaba de registrar con su dni
      query = """SELECT rol_id AS id, rol_name AS name FROM rol"""
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

UserSystem = User()