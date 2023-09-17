import cv2
import pytesseract
import imutils
import numpy as np
from plate_validator import Plate
from find_in_db import findPlateInDB

# Configuración de la ubicación de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Hp\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
config = '--psm 1'
cap = cv2.VideoCapture(0) 
plate = Plate()

def read_plate():
    text = ""
    while True:
        ret, img = cap.read()

        if ret == False:
            break

        # Leemos la imagen y la convertimos a escala de grises
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Aplicamos filtro y detectamos los bordes para localizar placa
        bfilter = cv2.bilateralFilter(gray, 11, 17, 17) #Reducimos ruido
        edged = cv2.Canny(bfilter, 30, 200) #Detectamos bordes

        # Encontramos los contornos y aplicamos una mascara
        keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(keypoints)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

        location = None
        for contour in contours:
            approx = cv2.approxPolyDP(contour, 10, True)
            if len(approx) == 4:
                location = approx
                break
            
        mask = np.zeros(gray.shape, np.uint8)
        if location is not None:
            # La máscara es válida, puedes realizar operaciones en ella
            cv2.drawContours(mask, [location], 0, 255, -1)
            cv2.bitwise_and(img, img, mask=mask)

        (x, y) = np.where(mask == 255)
        # Inicializa las coordenadas en cero
        (x1, y1, x2, y2) = (0, 0, 0, 0)  

        if len(x) > 0 and len(y) > 0:
            (x1, y1) = (np.min(x), np.min(y))
            (x2, y2) = (np.max(x), np.max(y))

       # Verificamos si la imagen recortada tiene dimensiones mínimas para realizar el recorte
        if x2 - x1 > 0 and y2 - y1 > 0:
            cropped_image = gray[x1:x2+1, y1:y2+1]

            # Verificamos si la imagen recortada tiene un tamaño mínimo para procesar con Tesseract
            if cropped_image.size > 0:
                # Extraemos el texto de la placa
                text = pytesseract.image_to_string(cropped_image, config=config)
                font = cv2.FONT_HERSHEY_SIMPLEX

                # Limpiamos y validamos el texto
                is_valid, clean_text = plate.is_plate(text)
                if is_valid == True :
                    cv2.putText(img, text=clean_text, org=(y1, x2 + 30), fontFace=font, fontScale=1, color=(255, 255, 0), thickness=2, lineType=cv2.LINE_AA)

                    # Buscamos la placa en la base de datos
                    was_found, data = findPlateInDB(clean_text)
                    if was_found == True:
                        cv2.putText(img, text="Encontrada", org=(y1, x2 + 50), 
                        fontFace=font, fontScale=1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
                        print(data)
                    else:
                        cv2.putText(img, text="Desconocida", org=(y1, x2 + 50), 
                        fontFace=font, fontScale=1, color=(0, 0, 255), thickness=2, lineType=cv2.LINE_AA)
                        print(data)
                cv2.rectangle(img, (y1, x1), (y2, x2), (255, 255, 0), 3)
            else:
                # Si la imagen recortada es demasiado pequeña o vacía, mantén el texto en blanco
                text = ""
        else:
            # Si la imagen recortada es demasiado pequeña, limpiamos el texto
            text = ""
        
       
        _, buffer = cv2.imencode('.jpg', img)
        img = buffer.tobytes()

        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + img + b'\r\n')
            
                

