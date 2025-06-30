from abc import ABC, abstractmethod
import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk
from components import EntradaPudDown, SalidaPWM

ruta_imagen = Path(__file__).parent / "img" / "logo_rcad.png"



class PanelBase(tk.Frame, ABC):
    def __init__(self, master, cambiar_panel, titulo:str, font:tuple, button_title:str, panel_redirect_name:str):
        super().__init__(master)
        self.pack(fill="both", expand=True) #Coloca este widget (por ejemplo, un Frame) y haz que se expanda y ocupe todo el espacio disponible, tanto en ancho como en alto."
        self.titulo = titulo
        self.font = font
        self.panel_redirect_name = panel_redirect_name

        if titulo and font:
            tk.Label(self, text=self.titulo, font=self.font).pack(pady=20)

        self.crear_widgets_extra()

        if button_title and panel_redirect_name:
            tk.Button(self, text=button_title, command=lambda: cambiar_panel(self.panel_redirect_name)).pack()


    @abstractmethod
    def crear_widgets_extra(self):
        """Método que las subclases deben implementar para añadir contenido propio"""
        pass



class PanelBienvenida(PanelBase):
    def __init__(self, master, cambiar_panel):
        super().__init__(
            master,
            cambiar_panel,
            titulo=None,
            font=None,
            button_title=None,
            panel_redirect_name=None
        )
        self.after(3000, lambda: cambiar_panel("principal"))

    def crear_widgets_extra(self):
        ancho = self.winfo_screenwidth()
        alto = self.winfo_screenheight()

        imagen_original = Image.open(ruta_imagen)
        imagen_redimensionada = imagen_original.resize((ancho, alto))
        self.imagen = ImageTk.PhotoImage(imagen_redimensionada)

        tk.Label(self, image=self.imagen).pack(fill="both", expand=True)




class PanelPrincipal(PanelBase):
    def __init__(self, master, cambiar_panel):
        super().__init__(
            master,
            cambiar_panel,
            titulo="Panel Principal",
            font=("Arial", 16),
            button_title="Ir a Panel de Brillo",
            panel_redirect_name="brillo"
        )


    def crear_widgets_extra(self):
        self.slider = tk.Scale(
            self, 
            from_=10, 
            to=100, 
            orient="horizontal", 
            label="Nivel de brillo",
            command = self.on_slider_change
        )
        self.slider.set(self.master.nivel_brillo_on)  # carga valor actual
        self.slider.pack()

    def on_slider_change(self, valor):
        brillo_valor = int(valor)
        self.master.brillo.modificar_salida(brillo_valor)
        self.master.set_nivel_brillo(brillo_valor, self.master.nivel_brillo_off)  # actualiza y guarda


class PanelBrillo(PanelBase):
    def __init__(self, master, cambiar_panel):
        super().__init__(
            master,
            cambiar_panel,
            titulo="Control de Brillo",
            font=("Arial", 16),
            button_title="Volver",
            panel_redirect_name="principal"
            )
    
    def crear_widgets_extra(self):
        self.slider = tk.Scale(self, from_=0, to=100, orient="horizontal")
        self.slider.pack()






class BaseApp(tk.Tk):
    """
    App hereda de tk.Tk y es la ventana principal
    """
    def __init__(self, ancho=None, alto=None, fullscreen=True):
        super().__init__()  # Crea la ventana principal

        self.ancho = ancho or self.winfo_screenwidth()
        self.alto = alto or self.winfo_screenheight()
        self.fullscreen = fullscreen

        # Configuración de ventana
        self.geometry(f"{self.ancho}x{self.alto}+0+0")
        self.attributes('-fullscreen', self.fullscreen)
        self.bind("<FocusIn>", lambda e: self.attributes("-fullscreen", self.fullscreen))


        self.paneles = {}
        self.configurar_paneles()
        self.panel_actual = None
        self.mostrar_panel("principal")  # default

    def configurar_paneles(self):
        raise NotImplementedError("Debes implementar configurar_paneles en la subclase.")

    def mostrar_panel(self, nombre):
        if self.panel_actual == nombre:
            return  # No hagas nada si ya estás en el mismo panel

        for panel in self.paneles.values():
            panel.pack_forget()

        self.paneles[nombre].pack(fill="both", expand=True)
        self.panel_actual = nombre  # Actualiza el panel actual



class DeteccionObstaculosApp(BaseApp):
    def __init__(self, nivel_brillo_off=5, *args, **kwargs):
        GPIO.setmode(GPIO.BCM)
        self.boton = EntradaPudDown(19)
        self.brillo = SalidaPWM(26, 100)

        config = leer_json()
        self.nivel_brillo_on = config
        self.nivel_brillo_off = nivel_brillo_off
        super().__init__(*args, **kwargs)
        self.after(200, self.monitor_gpio)

    def configurar_paneles(self):
        self.paneles = {
            "principal": PanelPrincipal(self, self.mostrar_panel),
            "brillo": PanelBrillo(self, self.mostrar_panel),
            "bienvenida": PanelBienvenida(self, self.mostrar_panel),
        }

    def monitor_gpio(self):
        
        if self.boton.esta_presionado():
            # self.mostrar_panel("brillo")
            self.brillo.modificar_salida(self.nivel_brillo_on)
        else:
            # self.mostrar_panel("bienvenida")
            self.brillo.modificar_salida(self.nivel_brillo_off)
        
        

        self.after(200, self.monitor_gpio)

        

    def set_nivel_brillo(self, on, off):
        self.nivel_brillo_on = on
        self.nivel_brillo_off = off
        escribir_json(on)





if __name__ == "__main__":
    import RPi.GPIO as GPIO
    from json_utils import *
    app = DeteccionObstaculosApp(ancho=800, alto=480, fullscreen=False)
    app.mainloop()
