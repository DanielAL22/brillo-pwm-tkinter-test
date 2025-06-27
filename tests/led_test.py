import RPi.GPIO as GPIO
import time

# Configurar el número del pin como BCM
LED_PIN = 26

# Configuración inicial
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    print("Iniciando test de LED. El LED parpadeará 5 veces.")
    for i in range(5):
        GPIO.output(LED_PIN, GPIO.HIGH)
        print(f"Encendido {i+1}")
        time.sleep(0.5)
        GPIO.output(LED_PIN, GPIO.LOW)
        print(f"Apagado {i+1}")
        time.sleep(0.5)
    print("Test finalizado.")
finally:
    GPIO.cleanup()
