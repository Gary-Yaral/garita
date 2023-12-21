import mysql.connector
from db_config.mysql import MysqlDB
from pwd_md.pass_config import hash_password

# Importante - Deben ser similar a los valores de la BD
ENABLE_STATUS = 1
ADMIN_ROL_ID = 1

class User():
  conn = None
  cursor = None

  def __init__(self,):
    self.conn = MysqlDB()
  
  def find_user(self, user):
    conn = self.conn.connect()
    cursor = conn.cursor(dictionary=True)
    try:
      query = """
          SELECT *
          FROM user 
          WHERE BINARY user.username=%s"""
      params = (user,)
      cursor.execute(query, params)
      result = cursor.fetchone()
      return result
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      cursor.close()
      conn.close()

  def load(self, per_page, current_page):
    conn = self.conn.connect()
    cursor = conn.cursor(dictionary=True)
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
      cursor.execute(query, params)
      result = cursor.fetchall()
      if not result:
        return (False, None)
      return (True, result)
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      cursor.close()
      conn.close()

  def get_status_types(self):
    conn = self.conn.connect()
    cursor = conn.cursor(dictionary=True)
    try:
      query = """
          SELECT 
            user_status_id AS id,
            status_name AS name
          FROM user_status
          """
      params = ()
      cursor.execute(query, params)
      result = cursor.fetchall()
      if not result:
        return (False, None)
      return (True, result)
    except mysql.connector.Exception as e:
      print("Error: {}".format(e))
    finally:
      cursor.close()
      conn.close()

  def get_total(self):
    conn = self.conn.connect()
    cursor = conn.cursor(dictionary=True)
    try:
      query = """
          SELECT COUNT(*) AS total FROM user;
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
      conn.close()

  def find_user_status(self, status_id):
    conn = self.conn.connect()
    cursor = conn.cursor(dictionary=True)
    try:
      query = """
          SELECT *
          FROM user_status 
          WHERE user_status_id=%s"""
      params = (status_id,)
      cursor.execute(query, params)
      return cursor.fetchone()
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      cursor.close()
      conn.close()

  def get_user_roles(self, user_id):
    conn = self.conn.connect()
    cursor = conn.cursor(dictionary=True)
    try:
      query = """
          SELECT *
          FROM user_rol 
          INNER JOIN rol
          ON rol.rol_id = user_rol.fk_rol_id
          WHERE fk_user_id=%s"""
      params = (user_id,)
      cursor.execute(query, params)
      return cursor.fetchall()
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      cursor.close()
      conn.close()
  
    # Métodos CRUD
  
  def update(self, _id, dni, name, surname, username, password, status, rol):
    conn = self.conn.connect()
    cursor = conn.cursor(dictionary=True)
    try:
      # Si intenta cambiar la cedula por una ya existente
      can_use_dni = self.can_use_DNI(dni, _id)
      if not can_use_dni:
        return (False, {'error': 'Ya existe un usuario con ese número de cédula'})
      
      # Si intenta cambiar el nombre de usuario por uno existente
      can_use_username = self.can_use_username(username,_id)
      if not can_use_username:
        return (False, {'error': 'Ya existe ese nombre de usuario'})
      
      if self.is_last_admin_enable(_id):
        if int(status) != ENABLE_STATUS:
            return (False, {'error':'No es posible deshabilitar este usuario, debido a que es el único administrador'})
        if int(rol) != ADMIN_ROL_ID:
            return (False, {'error':'No es posible cambiar el rol de este usuario, debido a que es el único administrador'})
        
        was_updated = self.update_last_admin(dni, name, surname, username, password, _id)
        if was_updated:
          return (True, {'message':'Usuario administrador actualizado correctamente'})
        
      # Actualiza a cualquier otro usuario
      if self.update_any_user(dni, name, surname, username, password, status, _id):
        if self.update_rol(rol, _id):
          return (True, {'message':'Usuario actualizado correctamente'})
        return (False, {'error':'Ha ocurrido un error al actualizar el rol de este usuario'})
      return (False, {'error':'Ha ocurrido un error al actualizar este registro'})
    except Exception as e:
      print("Error: {}".format(e))
      return (False, {'error':'Ha ocurrido un error al actualizar el registro'})
    finally:
      cursor.close()
      conn.close()

  def delete(self, _id):
    conn = self.conn.connect()
    cursor = conn.cursor(dictionary=True)
    try:
      canDelete = self.is_last_admin_enable(_id)
      if canDelete:
        return (False, {'error':'No es posible eliminar este registro, porque es el único administrador habilitado'})

      # mensaje satisfactorio
      result_ok = (True, {'message':'Usuario eliminado correctamente'})
      result_err = (False, {'message':'Ha ocurrido un error al eliminar el registro'})

       # Verificamos que no sea administrador y lo eliminamos
      query = """SELECT fk_rol_id AS rol_id FROM user_rol WHERE fk_user_id = %s"""
      params = (_id,)
      cursor.execute(query, params)
      result = cursor.fetchall()
      if len(result) > 0:
        if result[0]['rol_id'] != ADMIN_ROL_ID:
          query = """DELETE FROM user WHERE id = %s"""
          params = (_id,)
          cursor.execute(query, params)
          if cursor.rowcount > 0:
            conn.commit()
            return result_ok
          return result_err
        
      # Si es administrador verificamos que no sea el ultimo administrador
      query = """SELECT * FROM user_rol WHERE fk_rol_id = %s"""
      params = (ADMIN_ROL_ID,)
      cursor.execute(query, params)
      result = cursor.fetchall()
      if len(result) > 1 :
        query = """DELETE FROM user WHERE id = %s"""
        params = (_id,)
        cursor.execute(query, params)
        if cursor.rowcount > 0:
          conn.commit()
          return result_ok
        return result_err
      
      return (False, {'error': 'Este usuario es el único administrador y no se puede borrar'})
        
    except mysql.connector.Error as e:
      print("Error: {}".format(e))
      if e.errno == 1451:
        return (False, {'error':'No es posible eliminar el registro, tiene registros vinculados'})
      return (False, {'error':'Ha ocurrido un error al eliminar el registro'})
    finally:
      cursor.close()
      conn.close()
  
  # Métodos para filtrar en el datatables
  def filter(self, per_page, current_page, filter):
    conn = self.conn.connect()
    cursor = conn.cursor(dictionary=True)
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
      conn.close()

  # Obtiene el total de registro que trae el filtro
  def get_total_filtered(self, filter):
    conn = self.conn.connect()
    cursor = conn.cursor(dictionary=True)
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
      cursor.execute(query, params)
      result = cursor.fetchall()
      if not result:
        return (False, None)
      return (True, result)
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      cursor.close()
      conn.close()

  def add_new(self, dni, name, surname, username, password, status, rol_id):
    conn = self.conn.connect()
    cursor = conn.cursor(dictionary=True)
    try:
      # Si ya existe la cedula en la bse datos entonces retornamos error
      query = """SELECT * FROM user WHERE dni = %s"""
      params = (dni,)
      cursor.execute(query, params)
      result = cursor.fetchall()
      if len(result) > 0:
        return (False, {'error': 'Ya existe un usuario con ese número de cédula'})
      
       # Si ya existe el nombre de usuario en la bse datos entonces retornamos error
      query = """SELECT * FROM user WHERE BINARY username = %s"""
      params = (username,)
      cursor.execute(query, params)
      result = cursor.fetchall()
      if len(result) > 0:
        return (False, {'error': 'Ya existe ese nombre de usuario'})
      
      # Agregmos solo si la cedula y el nombre de usuario no existen en la BD
      query = """
            INSERT INTO user(dni, name, surname, username, password, fk_user_status_id)
            VALUES(%s, %s, %s, %s, %s, %s)
          """
      encryptedPass = hash_password(password)
      params = (dni, name, surname, username, encryptedPass, status)
      cursor.execute(query, params)
      if cursor.rowcount > 0:
        conn.commit()
        result = self.add_role(dni, rol_id)
        if result[0] == True:
          return (True, {'message':'Usuario agregado correctamente'})
        return (False, {'message':'Ha ocurrido un error al agregar el rol al usuario'})
      return (False, {'message':'Ha ocurrido un error al agregar el registro'})
    except Exception as e:
      print("Error: {}".format(e))
      return (False, {'message':'Ha ocurrido un error al agregar el registro'})
    finally:
      cursor.close()
      conn.close()  

  def add_role(self, dni, rol_id):
    conn = self.conn.connect()
    cursor = conn.cursor(dictionary=True)
    try:
      # Buscamos el usuario que se acaba de registrar con su dni
      query = """SELECT * FROM user WHERE dni = %s"""
      params = (dni,)
      cursor.execute(query, params)
      result = cursor.fetchall()
      if len(result) > 0: 
        user_id = result[0]["id"]
        query = """INSERT INTO user_rol(fk_rol_id,
          fk_user_id) VALUES(%s, %s)"""
        params = (rol_id, user_id)
        cursor.execute(query, params)
        result = cursor.fetchall()      
      if cursor.rowcount > 0:
        conn.commit()
        return (True, {'message':'Rol agregado correctamente al usuario'})
      return (False, {'message':'Ha ocurrido un error al agregar el registro'})
    except Exception as e:
      print("Error: {}".format(e))
      return (False, {'message':'Ha ocurrido un error al agregar el registro'})
    finally:
      cursor.close()
      conn.close()

  def get_roles(self):
    conn = self.conn.connect()
    cursor = conn.cursor(dictionary=True)
    try:
      # Buscamos el usuario que se acaba de registrar con su dni
      query = """SELECT rol_id AS id, rol_name AS name FROM rol"""
      params = ()
      cursor.execute(query, params)
      result = cursor.fetchall()
      if not result:
        return (False, None)
      return (True, result)
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      cursor.close()
      conn.close()

  def can_use_DNI(self, _dni, _id):
    conn = self.conn.connect()
    cursor = conn.cursor(dictionary=True)
    try:
      # Si ya existe la cedula en la base datos entonces retornamos error
      query = """SELECT * FROM user WHERE dni = %s"""
      params = (_dni,)
      cursor.execute(query, params)
      result = cursor.fetchall()
      can_use_it = False
      if len(result) > 0:
        for data in result:
          if data['id'] == _id:
            can_use_it = True
      return can_use_it     
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      cursor.close()
      conn.close()

  def can_use_username(self, username, _id):
    conn = self.conn.connect()
    cursor = conn.cursor(dictionary=True)
    try:
      query = """SELECT * FROM user WHERE username = %s"""
      params = (username,)
      cursor.execute(query, params)
      result = cursor.fetchall()
      can_use_it = False
      if len(result) > 0:
        for data in result:
          if data['id'] == _id:
            can_use_it = True
      return can_use_it  
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      cursor.close()
      conn.close()

  def is_last_admin_enable(self, _id):
    conn = self.conn.connect()
    cursor = conn.cursor(dictionary=True)
    try:
      # Verificamos que no sea el ultimo administrador habilitado
      query = """
        SELECT 
          fk_rol_id AS rol_id, 
          fk_user_status_id AS status_id,
          fk_user_id AS user_id
          FROM user_rol 
          INNER JOIN USER 
          ON user.id = user_rol.fk_user_id
          WHERE 
            fk_rol_id = %s 
          AND 
            user.fk_user_status_id = %s
        """
      params = (ADMIN_ROL_ID, ENABLE_STATUS)
      cursor.execute(query, params)
      result = cursor.fetchall()
      is_last = False
      if len(result) == 1:
        for data in result:
          if data['user_id'] == _id:
            is_last = True
      return is_last  
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      cursor.close()
      conn.close()
  
  def is_admin(self, _id):
    conn = self.conn.connect()
    cursor = conn.cursor(dictionary=True)
    try:
      # Verificamos que no sea el ultimo administrador habilitado
      query = """
        SELECT 
          fk_rol_id AS rol_id 
          FROM user_rol
          WHERE fk_user_id = %s;
        """
      params = (_id,)
      cursor.execute(query, params)
      result = cursor.fetchall()
      is_admin = False
      if len(result) > 0:
        for data in result:
          if data['rol_id'] == ADMIN_ROL_ID:
            is_admin = True
      return is_admin 
    except Exception as e:
      print("Error: {}".format(e))
    finally:
      cursor.close()
      conn.close()

  def update_last_admin(self, dni, name, surname, username, password, _id):
    conn = self.conn.connect()
    cursor = conn.cursor(dictionary=True)
    try:   
      # Si no envian la nueva password
      params = ()
      query = """"""
      if password == '':
        params = (dni, name, surname, username, _id)
        query = """
          UPDATE user
          SET 
            dni = %s, 
            name = %s, 
            surname = %s, 
            username = %s  
          WHERE id = %s
          """
      else:
        encrypted_pass = hash_password(password)
        params = (dni, name, surname, username, encrypted_pass, _id)
        query = """
          UPDATE user
          SET 
            dni = %s, 
            name = %s, 
            surname = %s, 
            username = %s, 
            password = %s 
          WHERE id = %s
          """
      cursor.execute(query, params)
      conn.commit()
      return True
    except Exception as e:
      print("Error: {}".format(e))
      return False
    finally:
      cursor.close()
      conn.close()

  def update_any_user(self, dni, name, surname, username, password, status, _id):
    conn = self.conn.connect()
    cursor = conn.cursor(dictionary=True)
    try:   
      # Si no envian la nueva password
      params = ()
      query = """"""
      if password == '':
        params = (dni, name, surname, username, status, _id)
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
      else:
        encrypted_pass = hash_password(password)
        params = (dni, name, surname, username, encrypted_pass, status,_id)
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
      cursor.execute(query, params)
      conn.commit()
      return True
    except Exception as e:
      print("Error: {}".format(e))
      return False
    finally:
      cursor.close()
      conn.close()

  def update_rol(self, rol, _id):
    conn = self.conn.connect()
    cursor = conn.cursor(dictionary=True)
    try:   
      params = (rol, _id)
      query = """
        UPDATE user_rol
        SET 
          fk_rol_id = %s 
        WHERE fk_user_id = %s
      """
      cursor.execute(query, params)
      conn.commit()
      return True
    except Exception as e:
      print("Error: {}".format(e))
      return False
    finally:
      cursor.close()
      conn.close()

UserSystem = User()