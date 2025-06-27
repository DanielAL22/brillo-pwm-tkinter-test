import RPi.GPIO as GPIO
from components import SalidaPWM



GPIO.setmode(GPIO.BCM)


brillo = SalidaPWM(26, 100)




while True:
    dato = input("Digite el nuevo DC: ")
    if dato == "z":
        print("fin del programa")
        break
    else:
        brillo.modificar_salida(dato)

brillo.stop() #finaliza el pwm


GPIO.cleanup() #limpiamos canales GPIO


print("Fin de programa")