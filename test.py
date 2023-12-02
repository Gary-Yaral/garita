
from flask import Blueprint, request, send_file
import io, os
import pandas as pd
 
""" def generate_excel():
     # Crear un DataFrame de ejemplo
   


    # Guardar el DataFrame como un archivo Excel en BytesIO """

data = {
    'Nombre': ['Juan', 'María', 'Pedro'],
    'Edad': [25, 30, 28],
    'Email': ['juan@example.com', 'maria@example.com', 'pedro@example.com']
  }
df = pd.DataFrame(data)

df.to_excel('ejemplo.xlsx', index=True)
