def closeConnection(obj) :
  try:
    obj.cursor.close()
    obj.conn.close()
  except Exception as e:
    print("Error: {}".format(e))
  finally:
    print("Connection was closed")

def openConnection(obj, DB):
  db = DB()
  obj.conn = db.connect()
  obj.cursor = obj.conn.cursor(dictionary=True)