import re
class Plate:
  def is_plate(self, txt):
      # Eliminar caracteres que no sean letras mayúsculas o números al principio y al final
      clean_text = re.sub(r'^[^A-Z0-9]+|[^A-Z0-9]+$', '', txt)
      
      # Definir una expresión regular para el patrón "XXX-XXXX" donde XXX son mayúsculas y XXXX son números
      patron = r'^[A-Z]{3}-\d{3,4}$'
      
      # Usar re.match() para verificar si la cadena coincide con el patrón
      if re.match(patron, clean_text):
          return (True, clean_text)
      else:
          return (False, txt)
