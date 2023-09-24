import bcrypt

encode = 'utf-8'

def hash_password(password) :
  passEncoded = password.encode(encode)
  return bcrypt.hashpw(passEncoded, bcrypt.gensalt())

def verify_password(password, hashed_pwd):
  passEncoded = "{}".format(password).encode(encode)
  return bcrypt.checkpw(passEncoded, hashed_pwd.encode(encode))