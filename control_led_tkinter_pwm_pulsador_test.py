import RPi.GPIO as GPIO
import time


from components import EntradaPudDown, SalidaPWM  # O el nombre de tu archivo si lo separaste
from gui import App

GPIO.setmode(GPIO.BCM)

boton = EntradaPudDown(19)
brillo = SalidaPWM(26, 100)
nivel_brillo_on = 100 #nivel de brillo definido en la configuracion
nivel_brillo_off = 0 #nivel de brillo definido para el retroceso

print("Test de activacion/apagado de brillo con pulsador (marcha atrás)")



app = App(ancho=400, alto=280, fullscreen=False)
app.mainloop()



try:
    while True:
        if boton.esta_presionado():
            print("¡Botón presionado!")
            brillo.modificar_salida(nivel_brillo_on)
        else:
            print("Botón suelto")
            brillo.modificar_salida(nivel_brillo_off)
        time.sleep(0.2)
except KeyboardInterrupt:
    print("\nTest finalizado.")
finally:
    GPIO.cleanup()
