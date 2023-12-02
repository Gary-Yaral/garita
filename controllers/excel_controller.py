
from flask import request
import flask
import xlsxwriter
import tempfile
from datetime import datetime

# Obtener la fecha y hora actual
def generate_excel():
  req = request.json
  data = req.get('data')
  file_name = req.get('file_name').lower()
  is_filtered = req.get('is_filtered')
  if is_filtered: 
      file_name = file_name + "_filtrados"
  file_name = f"{file_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
  # Crear un archivo temporal
  with tempfile.NamedTemporaryFile(suffix='.xlsx', prefix=file_name, delete=False) as tmp_file:
      tmp_file_path = tmp_file.name
      
      # Escribir en el archivo Excel
      workbook = xlsxwriter.Workbook(tmp_file_path)
      worksheet = workbook.add_worksheet('Nombre')

      # Formato para centrado vertical y horizontal en la primera fila
      bold_center_format = workbook.add_format({'bold': True, 'align': 'center', 'valign': 'vcenter'})

      # Establecemos el ancho de todas las columnas
      worksheet.set_column(0, len(data[0]) - 1, 20)
      # Formato para centrado vertical y horizontal en la primera celda de cada fila
      center_format = workbook.add_format({'align': 'center', 'valign': 'vcenter'})

      # Escribir los datos y aplicar formato a las celdas
      for i, row in enumerate(data):
          for j, cell_data in enumerate(row):
              if i == 0 or j == 0:  # Aplicar negrita y centrado a la primera fila y la primera celda de cada fila
                  worksheet.write(i, j, cell_data, bold_center_format)
              else: 
                  worksheet.write(i, j, cell_data, center_format)

      workbook.close()

  # Leer el archivo y enviarlo como respuesta de descarga
  with open(tmp_file_path, 'rb') as f:
      output = flask.make_response(f.read())
      output.headers["Content-Disposition"] = f"filename={file_name}"
      output.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

  return output