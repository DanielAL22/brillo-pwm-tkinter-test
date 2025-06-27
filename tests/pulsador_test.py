import RPi.GPIO as GPIO
import time

from components import EntradaPudDown  # O el nombre de tu archivo si lo separaste

GPIO.setmode(GPIO.BCM)

boton = EntradaPudDown(pin=19)

print("Test de EntradaPudDown en GPIO 19. Presiona el botón...")

try:
    while True:
        if boton.esta_presionado():
            print("¡Botón presionado!")
        else:
            print("Botón suelto")
        time.sleep(0.2)
except KeyboardInterrupt:
    print("\nTest finalizado.")
finally:
    GPIO.cleanup()
