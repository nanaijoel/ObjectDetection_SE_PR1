import cv2
#  import numpy as np


def start_webcam():
    # Webcam starten (0 steht für die Standardkamera)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Fehler: Kamera konnte nicht geöffnet werden")
        return

    while True:
        # Frame von der Kamera lesen
        ret, frame = cap.read()

        if not ret:
            print("Fehler: Frame konnte nicht gelesen werden")
            break

        # Frame im Fenster anzeigen
        cv2.imshow('Webcam', frame)

        # Mit 'q' das Programm beenden
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Kamera freigeben und Fenster schließen
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    start_webcam()
