from abc import ABC, abstractmethod
import RPi.GPIO as GPIO


class Salida(ABC):
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)


class SalidaPWM(Salida):
    def __init__(self, pin, frecuencia):
        super().__init__(pin)
        self.frecuencia = frecuencia #frecuencia en Hz
        self.pwm = GPIO.PWM(self.pin, self.frecuencia)
        self.pwm.start(0)  # Establece un dc inicial. Comienza con brillo al 0%

    def modificar_salida(self, valor):
        """Controla brillo con duty cycle de 0 a 100"""
        self.pwm.ChangeDutyCycle(valor)

    def detener(self):
        self.pwm.stop()





class Entrada(ABC):
    def __init__(self, pin, pud=GPIO.PUD_OFF):
        self.pin = pin
        GPIO.setup(pin, GPIO.IN, pull_up_down=pud)

    def leer(self):
        return GPIO.input(self.pin)


class EntradaPudDown(Entrada):
    def __init__(self, pin):
        super().__init__(pin, pud=GPIO.PUD_DOWN)

    def esta_presionado(self):
        return self.leer() == GPIO.HIGH


class EntradaPudUp(Entrada):
    def __init__(self, pin):
        super().__init__(pin, pud=GPIO.PUD_UP)