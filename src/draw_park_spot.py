import cv2
import json
import numpy as np

# Variabili globali per gestire il disegno dei rettangoli
drawing = False
start_point = None
rectangles = []  # Lista dei rettangoli

# Funzione di callback per il mouse
def draw_rectangle(event, x, y, flags, param):
    global drawing, start_point, rectangles
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_point = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing and start_point:
            img_copy = frame.copy()
            cv2.rectangle(img_copy, start_point, (x, y), (255, 0, 0), 2)
            cv2.imshow('Draw Parking Boxes', img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        end_point = (x, y)
        rectangles.append((start_point, end_point))  # Aggiungi il rettangolo alla lista
        cv2.rectangle(frame, start_point, end_point, (255, 0, 0), 2)

# Leggi l'immagine
image_path = '../media/test_park.jpg'  # Sostituisci con il percorso della tua immagine
frame = cv2.imread(image_path)

# Crea una finestra e imposta la funzione di callback del mouse
cv2.namedWindow('Draw Parking Boxes')
cv2.setMouseCallback('Draw Parking Boxes', draw_rectangle)

# Mostra l'immagine e aspetta l'input
while True:
    cv2.imshow('Draw Parking Boxes', frame)
    if cv2.waitKey(1) & 0xFF == 27:  # Esci premendo 'Esc'
        break

# Salva i rettangoli in un file JSON
with open('rectangles.json', 'w') as json_file:
    json.dump(rectangles, json_file)

print(f"Rectangles saved to rectangles.json: {rectangles}")

cv2.destroyAllWindows()
