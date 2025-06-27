#!/home/rcad/proyecto_borde_caex/venv/bin/python

from tkinter import *
from tkinter import messagebox, ttk
from glob import glob
import time
from PIL import ImageTk , Image
import serial
import subprocess as sp
import RPi.GPIO as GPIO
import sys

#importaciones propias
from data_utils import *

##############################################################
#VARIABLES GLOBALES 
contraseña=0
exit_programa=False
unidad_metros=0
unidad_centimetros=0
# unidad_final=100
unidad_final = leer_json()
x=None

################################################################
#DEFINICION DE PINES Y VELOCIDADES
ser = serial.Serial("/dev/ttyS0", 115200) 
#-----------------------------------------------------
GPIO.setmode(GPIO.BCM)


GPIO.setwarnings(False) 

GPIO.setup(2,GPIO.OUT) 
GPIO.setup(3,GPIO.OUT) 
GPIO.setup(9,GPIO.OUT)
GPIO.setup(12,GPIO.OUT) 

GPIO.output(2, GPIO.LOW) 
GPIO.output(3, GPIO.LOW)
GPIO.output(9, GPIO.LOW)
GPIO.output(12, GPIO.LOW) 



###############################################################
#DEFINICION DE FUNCIONES 

def delay(n):
    time.sleep(n)



#PANTALLAS DEL PROGRAMA 


def logo_screen(): #PANTALLA DE BIENVENIDA

  
    root = Tk()
    root.title('Detector de Obstáculos (Autoría: Andrés Núñez Donoso)')
    
    
    open_image = Image.open('/home/rcad/proyecto_borde_caex/images/logo_rcad_grande.png')
    resized = open_image.resize((root.winfo_screenwidth() - 2*100, root.winfo_screenheight() - 2*100), Image.LANCZOS)
    new_pic = ImageTk.PhotoImage(resized)

    
    miframe = Frame(root)
    miframe.pack(fill=BOTH, expand=True,pady=100,padx=100)

    
    label = Label(miframe, image=new_pic)
    label.image = new_pic
    label.pack(fill=BOTH, expand=True)

    
    icono = PhotoImage(file='/home/rcad/proyecto_borde_caex/images/logo_rcad.png')
    root.iconphoto(True, icono)

    
    root.attributes('-fullscreen', True)

    
    root.after(3000, root.destroy)

    root.mainloop()


def config_screen():
    def fin_config():
        global unidad_final
        
        
        unidad_final=0
        unidad_final=(unidad_metros*100)+unidad_centimetros

        if unidad_final==0:
            unidad_final=1500
        else:
            unidad_final=(unidad_metros*100)+unidad_centimetros
        
   

        valor_cargado.set(str(unidad_final/100)+' m')
        miframe.update()

        escribir_json(unidad_final)
        

        root.destroy()
    
        delay(0.01)
        params_screen()  

    def sumar():
        global unidad_metros, unidad_centimetros

        if x=='metros':
            unidad_metros+=1

            if unidad_metros>40:
                unidad_metros=0

            medida_pantalla_label.set(str(unidad_metros)+' Metros')
            estado_pantalla.set(str(unidad_metros)+'m con '+str(unidad_centimetros) +'cm')
            miframe.update()

        if x=='centimetros':
            unidad_centimetros+=1

            if unidad_centimetros>99:
                unidad_centimetros=0

            medida_pantalla_label.set(str(unidad_centimetros)+' Centímetros')
            estado_pantalla.set(str(unidad_metros)+'m con '+str(unidad_centimetros) +'cm')
            miframe.update()
    
    def restar():
        global unidad_metros, unidad_centimetros

        if x=='metros':
            unidad_metros-=1

            if  unidad_metros<0:
                unidad_metros=40

            medida_pantalla_label.set(str(unidad_metros)+' Metros')
            estado_pantalla.set(str(unidad_metros)+'m con '+str(unidad_centimetros) +'cm')
            miframe.update()

        if x=='centimetros':
            unidad_centimetros-=1

            if unidad_centimetros< 0:
                unidad_centimetros=99

            medida_pantalla_label.set(str(unidad_centimetros)+' Centímetros')
            estado_pantalla.set(str(unidad_metros)+'m con '+str(unidad_centimetros) +'cm')
            miframe.update()

    def medida(operacion):
        global x
        x=operacion

        if operacion=='metros':
            estado_pantalla.set('Metros')
            miframe.update()

        if operacion=='centimetros':
            estado_pantalla.set('Centímetros')
            miframe.update()

    def cargar_valor():
        global unidad_final

        unidad_final=0
        unidad_final=(unidad_metros*100)+unidad_centimetros

        if unidad_final==0:
            unidad_final=1500
        else:
            unidad_final=(unidad_metros*100)+unidad_centimetros
        

        valor_cargado.set(str(unidad_final/100)+' m')
        miframe.update()
        escribir_json(unidad_final)

        delay(0.01)


    ##############################################################
    #VARIABLES
    custom_font = ('Rockwell', 30, 'bold italic')
    custom_font2 = ('Rockwell', 18, 'bold italic')
    custom_font3 = ('Rockwell', 20, 'bold italic')

    ##############################################################
    root=Tk()
    root.title('Detector de Obstáculos (Autoria: Andrés Núñez Donoso)')

    icono = PhotoImage(file='/home/rcad/proyecto_borde_caex/images/logo_rcad.png')

    root.iconphoto(True, icono)


    ################################################################
    #ABRIR IMAGEN 
    open_image=Image.open('/home/rcad/proyecto_borde_caex/images/logo_rcad.png')

    
    resized=open_image.resize((100,100), Image.Resampling.LANCZOS)
    new_pic=ImageTk.PhotoImage(resized)

    ################################################################
    #CONFIGURACION DEL FRAME
   
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()

    root.attributes('-fullscreen', True)
    delay(0.5)
    root.attributes('-fullscreen', True)

    
    def set_fullscreen(window):
        window.attributes('-fullscreen', True)

  
    def on_focus_in(event):
        set_fullscreen(event.widget)


  
    set_fullscreen(root)

  
    root.bind('<FocusIn>', on_focus_in)
  

    
    root.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")
    

 
    miframe = Frame(root)
    miframe.pack(fill=BOTH, expand=True)

    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    miframe.config(width=screen_width, height=screen_height)

    ################################################################
    #INCLUCION DE TEXTO E IMAGENES

    titulo=Label(miframe, text='Detector de Obstáculos', fg='#317CF5',font=custom_font).grid(row=0,column=1,columnspan=3,sticky='w',rowspan=2)
    sub_titulo=Label(miframe, text='Configuración de parámetros', fg='#317CF5',font=custom_font3).grid(row=1,column=1,columnspan=3,sticky='n')
    foto=Label(miframe,image=new_pic).grid(row=0,column=0,padx=10,pady=1)

    foto=Label(miframe,image=new_pic).grid(row=0,column=0,padx=10,pady=10)     

    # ################################################################
    #ENTRIES LABEL
    Config_unidad=Label(miframe,text='Configurar \n Unidades:',font=('8514oem',15)).grid(row=2,column=0, padx=5, pady=5,sticky='e')
    Config_distancia=Label(miframe,text='Configurar \n Distancia:',font=('8514oem',15)).grid(row=3,column=0, padx=5, pady=5,sticky='e')


    #################################################################
    #PANTALLA
    estado_pantalla=StringVar()
    estado_pantalla.set('')
    pantalla=Entry(miframe,textvariable=estado_pantalla, font=custom_font2)
    # pantalla.place(height=30,width=200)
    pantalla.grid(row=5,column=1,padx=10,pady=10,sticky='w',columnspan=2)
    pantalla.config(background="black",fg='#03f943', justify='left',width='13')

    #LABEL DE PANTALLA PRINCIPAL
    sub_pantalla=Label(miframe,text='Distancia Actual: ', font=('8514oem',15))
    sub_pantalla.grid(row=5,column=0,padx=10,pady=10,sticky='e')
    
    max_pantalla=Label(miframe,text='Máximo 40m ', font=('8514oem',15))
    max_pantalla.grid(row=6,column=1,padx=10,pady=10,sticky='n')

    # ################################################################
    #INDICADORES DE MEDIDAS
    #____________________________________________________________________________________________________________________
   
    estado_pantalla_dis=StringVar()
    estado_pantalla_dis.set('0cm')

    valor_cargado=StringVar()
    valor_cargado.set(str(unidad_final/100)+' m')
    # valor_cargado.set(str(5)+' m')

    distancia_final_label=Label(miframe,text='Valor\nCargado:',font=('8514oem',15)).grid(row=5,column=2, padx=5, pady=5,sticky='e')

    distancia_final=Entry(miframe,textvariable=valor_cargado, font=custom_font2)
    distancia_final.grid(row=5,column=3,padx=10,pady=10,sticky='w')
    distancia_final.config(background="black",fg='#03f943', justify='left',width='9')


    #____________________________________________________________________________________________________________________    

    mas=Button(miframe, text='+',font=('8514oem',15),fg='#1F2733',command=lambda:sumar())
    mas.config(bg='#5A94F4',bd=3, relief='solid',width=8)
    mas.grid(row=3,column=1, padx=5, pady=5,sticky='w')

    menos=Button(miframe, text='-',font=('8514oem',15),fg='#1F2733',command=lambda:restar())
    menos.config(bg='#708BB5',bd=3, relief='solid',width=8)
    menos.grid(row=4,column=1, padx=5, pady=5,sticky='w')

    centimetros_boton=Button(miframe, text='Centimetros',font=('8514oem',15),fg='#1F2733',command=lambda:medida('centimetros'))
    centimetros_boton.config(bg='#7189AF',bd=3, relief='solid',width=8)
    centimetros_boton.grid(row=2,column=2, padx=5, pady=5,sticky='w')

    metros_boton=Button(miframe, text='Metros',font=('8514oem',15),fg='#1F2733',command=lambda:medida('metros'))
    metros_boton.config(bg='#707F98',bd=3, relief='solid',width=8)
    metros_boton.grid(row=2,column=1, padx=5, pady=5,sticky='w')

    vacio=Label(miframe,text='').grid(row=6,column=2, sticky='e')
    vacio=Label(miframe,text='').grid(row=7,column=2, sticky='e')
  

    cargar=Button(miframe, text='Finalizar Configuración',font=('8514oem',15),fg='#1F2733',command=lambda:fin_config())
    cargar.config(bg='#F5C25B',bd=8, relief='solid',width=20)
    cargar.grid(row=8,column=2, padx=5, pady=5,sticky='s',columnspan=2)


    cargar2=Button(miframe, text='Cargar',font=('8514oem',15),fg='#1F2733',command=lambda:cargar_valor())
    cargar2.config(bg='#F5C25B',bd=3, relief='solid',width=7)
    cargar2.grid(row=3,column=3, padx=5, pady=5,sticky='w',columnspan=3,rowspan=2)


    #____________________________________________________________________________________________________________________
    medida_pantalla_label=StringVar()
    medida_pantalla_label.set('')

    medida_pantalla=Entry(miframe,textvariable=medida_pantalla_label, font=custom_font2)
    medida_pantalla.grid(row=3,column=2,padx=10,sticky='sw',rowspan=2,pady=(5, 25), ipady=25)
    medida_pantalla.config(background="black",fg='#03f943', justify='left',width='12')



    root.mainloop()


def params_screen():
    ###############################################################
    #DEFINICION DE FUNCIONES 
    def delay(n):
        time.sleep(n)

    def read_data():

    
        while True:
        
            contador = ser.in_waiting  
            
            delay(0.1)
            


            if contador > 8: 
                
                bytes_serial = ser.read(9) 
                ser.reset_input_buffer()


                if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59:
                    
                    distancia_low=bytes_serial[2] 
                    distancia_high=bytes_serial[3] 

                    intensidad_low=bytes_serial[4] 
                    intensidad_high=bytes_serial[5]

                    temperatura_low=bytes_serial[6]
                    temperatura_high=bytes_serial[7]


                    #Valores Finales

                    distancia= distancia_low + distancia_high * 256
                    intensidad= intensidad_low + intensidad_high * 256
                    temperatura= temperatura_low + temperatura_high * 256
                    temperatura = (temperatura/8) - 256 

                    ser.reset_input_buffer()

                    return distancia, intensidad, temperatura
    
    def lectura(estado):
        global exit_programa, unidad_final
        contador=0
        contador2=0
        contador3=0
        contador4=0

        
        while not exit_programa:

            estado=estado
            
            if estado=='iniciar':
                exit_programa=False
                data=read_data()

                distancia=data[0]
        
                estado_pantalla_dis.set(str(distancia/100)+' m')
             
                if distancia>unidad_final:
                    contador+=1
                    GPIO.output(2, GPIO.LOW)
                    GPIO.output(3, GPIO.LOW)
                    GPIO.output(9, GPIO.LOW)
                    GPIO.output(12, GPIO.LOW)

                    if contador==1: #MENSAJES E IMAGENES
                        flecha_verde_label=Label(miframe,image=flecha_verde_pic).grid(row=7,column=2,padx=1,pady=1,sticky='sw',rowspan=2,columnspan=2)
                        advertencia_nada_label=Label(miframe,image=advertencia_nada_pic).grid(row=3,column=1,padx=1,pady=1,rowspan=2,sticky='w')
                        advertencia_nada_label=Label(miframe,image=advertencia_nada_pic).grid(row=3,column=3,padx=1,pady=1,rowspan=2,sticky='e')

                        pantalla=Label(miframe,text='MANTENGA DISTANCIA', font=custom_font2)
                        pantalla.grid(row=3,column=1,padx=20,pady=10,columnspan=3)
                        pantalla.config(fg='#03a015', justify='left',width=20)

                        contador2=0
                        contador3=0
                        contador4=0

                    
                
                if distancia<=unidad_final and distancia>(unidad_final*67)/100:
                    contador2+=1
                    
                    if contador2==1:
                        flecha_amarilla_label=Label(miframe,image=flecha_amarilla_pic).grid(row=7,column=2,padx=1,pady=1,sticky='sw',rowspan=2,columnspan=2)
                        advertencia_amarilla_label=Label(miframe,image=advertencia_amarilla_pic).grid(row=3,column=1,padx=1,pady=1,rowspan=2,sticky='w')
                        advertencia_nada_label=Label(miframe,image=advertencia_nada_pic).grid(row=3,column=3,padx=1,pady=1,rowspan=2,sticky='e')


                        pantalla=Label(miframe,text='ADVERTENCIA', font=custom_font2)
                        pantalla.grid(row=3,column=1,padx=20,pady=10,columnspan=3)
                        pantalla.config(fg='#ddb800', justify='left',width=20)

                        contador=0
                        contador3=0
                        contador4=0

                    GPIO.output(2, GPIO.HIGH)
                    GPIO.output(3, GPIO.LOW)
                    GPIO.output(9, GPIO.LOW)
                    GPIO.output(12, GPIO.HIGH)
                    delay(0.15)
                    GPIO.output(12, GPIO.LOW)
                    delay(0.15)
                
                if distancia<=(unidad_final*67)/100 and distancia>(unidad_final*34)/100 :
                    contador3+=1

                    if contador3==1:
                        flecha_amarilla_label=Label(miframe,image=flecha_amarilla_pic).grid(row=7,column=2,padx=1,pady=1,sticky='sw',rowspan=2,columnspan=2)
                        advertencia_amarilla_label=Label(miframe,image=advertencia_amarilla_pic).grid(row=3,column=1,padx=1,pady=1,rowspan=2,sticky='w')
                        advertencia_nada_label=Label(miframe,image=advertencia_nada_pic).grid(row=3,column=3,padx=1,pady=1,rowspan=2,sticky='e')

                        pantalla=Label(miframe,text='ADVERTENCIA', font=custom_font2)
                        pantalla.grid(row=3,column=1,padx=20,pady=10,columnspan=3)
                        pantalla.config(fg='#ddb800', justify='left',width=20)

                        contador=0
                        contador2=0
                        contador4=0
                    
                    GPIO.output(2, GPIO.HIGH)
                    GPIO.output(3, GPIO.HIGH)
                    GPIO.output(9, GPIO.LOW)
                    GPIO.output(12, GPIO.HIGH)
                    delay(0.05)
                    GPIO.output(12, GPIO.LOW)
                    delay(0.05)

                if distancia<=(unidad_final*34)/100 and distancia>0:
                    contador4+=1

                    if contador4==1:
                        flecha_roja_label=Label(miframe,image=flecha_roja_pic).grid(row=7,column=2,padx=1,pady=1,sticky='sw',rowspan=2,columnspan=2)
                        advertencia_roja_label=Label(miframe,image=advertencia_roja_pic).grid(row=3,column=1,padx=1,pady=1,rowspan=2,sticky='w')
                        avertencia_roja2_label=Label(miframe,image=advertencia_roja_pic).grid(row=3,column=3,padx=1,pady=1,rowspan=2,sticky='e')

                        pantalla=Label(miframe,text='¡PELIGRO DE COLISIÓN!', font=custom_font2)
                        pantalla.grid(row=3,column=1,padx=20,pady=10,columnspan=3)
                        pantalla.config(fg='#ED1C24', justify='left',width=20)

                        contador=0
                        contador3=0
                        contador2=0

                    GPIO.output(2, GPIO.HIGH)
                    GPIO.output(3, GPIO.HIGH)
                    GPIO.output(9, GPIO.HIGH)
                    GPIO.output(12, GPIO.HIGH)

                miframe.update()

            if estado=='salir':
                cerrar_programa()
                break

    def cerrar_programa():
        global exit_programa
        estado_pantalla_dis.set('0cm')
        
        root.destroy()
   
        miframe.update()
    

        delay(0.01)
        password_screen()  # Abrimos la última pantalla
    
  


    ##############################################################
    #VARIABLES
    custom_font = ('Rockwell', 30, 'bold italic')
    custom_font2 = ('Rockwell', 18, 'bold italic')
    custom_font3 = ('Rockwell', 20, 'bold italic')
    custom_font4 = ('Rockwell', 12, 'bold italic')

    ##############################################################
    root=Tk()
    root.title('Detector de Obstáculos (Autoria: Andrés Núñez Donoso)')

    # Cargar la imagen como un icono de ventana
    icono = PhotoImage(file='/home/rcad/proyecto_borde_caex/images/logo_rcad.png')

    root.iconphoto(True, icono)


    ################################################################
    #ABRIR IMAGEN 
    open_image=Image.open('/home/rcad/proyecto_borde_caex/images/logo_rcad.png')
    camion=Image.open('/home/rcad/proyecto_borde_caex/images/camion3.png')
    tierra=Image.open('/home/rcad/proyecto_borde_caex/images/tierra.png')
    flecha_verde=Image.open('/home/rcad/proyecto_borde_caex/images/flecha_verde.png')
    flecha_amarilla=Image.open('/home/rcad/proyecto_borde_caex/images/flecha_amarilla.png')
    flecha_roja=Image.open('/home/rcad/proyecto_borde_caex/images/flecha_roja.png')
    advertencia_roja=Image.open('/home/rcad/proyecto_borde_caex/images/advertencia_roja.png')
    advertencia_amarilla=Image.open('/home/rcad/proyecto_borde_caex/images/advertencia_amarilla.png')
    advertencia_nada=Image.open('/home/rcad/proyecto_borde_caex/images/advertencia_nada.png')


    #Dimensiones Imagen
    resized=open_image.resize((100,100), Image.Resampling.LANCZOS)
    new_pic=ImageTk.PhotoImage(resized)

    camion_resized=camion.resize((250,240), Image.Resampling.LANCZOS)
    camion_pic=ImageTk.PhotoImage(camion_resized)

    tierra_resized=tierra.resize((150,150), Image.Resampling.LANCZOS)
    tierra_pic=ImageTk.PhotoImage(tierra_resized)

    flecha_verde_resized=flecha_verde.resize((150,150), Image.Resampling.LANCZOS)
    flecha_verde_pic=ImageTk.PhotoImage(flecha_verde_resized)

    flecha_amarilla_resized=flecha_amarilla.resize((150,150), Image.Resampling.LANCZOS)
    flecha_amarilla_pic=ImageTk.PhotoImage(flecha_amarilla_resized)

    flecha_roja_resized=flecha_roja.resize((150,150), Image.Resampling.LANCZOS)
    flecha_roja_pic=ImageTk.PhotoImage(flecha_roja_resized)

    advertencia_roja_resized=advertencia_roja.resize((100,100), Image.Resampling.LANCZOS)
    advertencia_roja_pic=ImageTk.PhotoImage(advertencia_roja_resized)

    advertencia_amarilla_resized=advertencia_amarilla.resize((100,100), Image.Resampling.LANCZOS)
    advertencia_amarilla_pic=ImageTk.PhotoImage(advertencia_amarilla_resized)

    advertencia_nada_resized=advertencia_nada.resize((100,100), Image.Resampling.LANCZOS)
    advertencia_nada_pic=ImageTk.PhotoImage(advertencia_nada_resized)


    ################################################################
    #CONFIGURACION DEL FRAME
    # Obtener el tamaño de la pantalla
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()

    root.attributes('-fullscreen', True)
    delay(0.5)
    root.attributes('-fullscreen', True)

    def set_fullscreen(window):
        window.attributes('-fullscreen', True)

 
    def on_focus_in(event):
        set_fullscreen(event.widget)

    set_fullscreen(root)

    root.bind('<FocusIn>', on_focus_in)

    root.geometry(f"{ancho_pantalla}x{alto_pantalla}+0+0")
    
    miframe = Frame(root)
    miframe.pack(fill=BOTH, expand=True)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    miframe.config(width=screen_width, height=screen_height)

    ################################################################
    #INCLUCION DE TEXTO E IMAGENES

    titulo=Label(miframe, text='Detector de Obstáculos', fg='#317CF5',font=custom_font).grid(row=0,column=1,columnspan=3,sticky='w',rowspan=2)
    sub_titulo=Label(miframe, text='Monitoreo y Sensado', fg='#317CF5',font=custom_font3).grid(row=1,column=1,columnspan=3,sticky='n')
    foto=Label(miframe,image=new_pic).grid(row=0,column=0,padx=10,pady=1)

    camion_label=Label(miframe,image=camion_pic).grid(row=5,column=3,padx=10,pady=10,rowspan=4,columnspan=2)
    tierra_label=Label(miframe,image=tierra_pic).grid(row=7,column=1,padx=10,pady=10,rowspan=2,columnspan=2,sticky='nw')


    # ################################################################
    #FLECHAS DE ADVERTENCIA

    flecha_indicacion=flecha_verde_pic

    flecha_verde_label=Label(miframe,image=flecha_verde_pic).grid(row=7,column=2,padx=1,pady=1,sticky='sw',rowspan=2,columnspan=2)
    advertencia_nada_label=Label(miframe,image=advertencia_nada_pic).grid(row=3,column=1,padx=1,pady=1,rowspan=2,sticky='w')
    advertencia_nada_label=Label(miframe,image=advertencia_nada_pic).grid(row=3,column=3,padx=1,pady=1,rowspan=2,sticky='e')

    pantalla=Label(miframe,text='MANTENGA DISTANCIA', font=custom_font2)
    pantalla.grid(row=3,column=1,padx=20,pady=10,columnspan=3)
    pantalla.config(fg='#03a015', justify='left',width=20)



    # ################################################################
    #INDICADORES DE MEDIDAS
    #____________________________________________________________________________________________________________________
    estado_pantalla_dis=StringVar()
    estado_pantalla_dis.set('0cm')

    valor_cargado=StringVar()
    valor_cargado.set(str(unidad_final/100)+' m')

    distancia_label=Label(miframe,text='Distancia:',font=custom_font2).grid(row=4,column=2, padx=1, pady=1,sticky='w')
    
    distancia_pantalla=Entry(miframe,textvariable=estado_pantalla_dis, font=custom_font3)
    distancia_pantalla.grid(row=5,column=2,padx=10,pady=10,sticky='w')
    distancia_pantalla.config(background="black",fg='#03f943', justify='left',width='6')

    #____________________________________________________________________________________________________________________
    #VALOR CARGADO
    distancia_final_label=Label(miframe,text='Valor\nCargado',font=custom_font4).grid(row=9,column=0, padx=1, pady=1,sticky='e')

    distancia_final=Entry(miframe,textvariable=valor_cargado, font=custom_font2)
    distancia_final.grid(row=9,column=1,padx=10,pady=10,sticky='wn')
    distancia_final.config(background="black",fg='#03f943', justify='left',width='8')

    #____________________________________________________________________________________________________________________
   
    # ################################################################
    #BOTONES DEL INTERACCIONES DEL PROGRAMA

    def ejecutar_lectura():
        lectura(estado='iniciar')

    root.after(100, ejecutar_lectura)

    salir=Button(miframe, text='Cambiar\nConfig',font=custom_font4,fg='#1F2733',command=lambda:cerrar_programa())
    salir.config(bg='#F5C25B',bd=3, relief='solid', width=8)
    salir.grid(row=0,column=4, padx=5, pady=5,sticky='e')



    root.mainloop()


def password_screen(): 
    ################################################################
    #DEFINICION DE FUNCIONES
    def monitoreo():
        root.destroy()
        delay(0.01)
        params_screen()

    def insertar_numero(num):
        entry_contrasena.insert(END, num)

    def verificar_contrasena():
        contrasena_ingresada = entry_contrasena.get()
        if contrasena_ingresada == contrasena_correcta:
            etiqueta = Label(miframe, text="¡Contraseña correcta!", font=custom_font4)
            etiqueta.grid(column=4,row=1)
            
            root.destroy()
        
            config_screen()

        else:
            etiqueta2 = Label(miframe, text="¡Contraseña incorrecta!", font=custom_font4)
            etiqueta2.grid(column=1,row=1,columnspan=3)
            entry_contrasena.delete(0, END)

   
    ##############################################################
    root=Tk()
    root.title('Detector de Obstáculos (Autoria: Andrés Núñez Donoso)')

    # Cargar la imagen como un icono de ventana
    icono = PhotoImage(file='/home/rcad/proyecto_borde_caex/images/logo_rcad.png')

    root.iconphoto(True, icono)


    custom_font = ('Rockwell', 30, 'bold italic')
    custom_font2 = ('Rockwell', 18, 'bold italic')
    custom_font3 = ('Rockwell', 20, 'bold italic')
    custom_font4 = ('Rockwell', 12, 'bold italic')

    ################################################################
    #CONFIGURACION DEL FRAME
    ancho_pantalla = root.winfo_screenwidth()
    alto_pantalla = root.winfo_screenheight()

    root.attributes('-fullscreen', True)
    delay(0.5)
    root.attributes('-fullscreen', True)

 
    def set_fullscreen(window):
        window.attributes('-fullscreen', True)

    def on_focus_in(event):
        set_fullscreen(event.widget)

    set_fullscreen(root)

    root.bind('<FocusIn>', on_focus_in)
        

    # Configurar el Frame principal
    miframe = Frame(root)
    miframe.pack(fill=BOTH, expand=True)

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    miframe.config(width=screen_width, height=screen_height)

    ################################################################
    #INCLUCION DE TEXTO E IMAGENES

    titulo=Label(miframe, text='CONTRASEÑA', fg='#317CF5',font=custom_font)
    titulo.grid(row=0,column=1,columnspan=3,padx=10,pady=10)
   
    
    ################################################################
    #CONTRASEÑA

    contrasena_correcta = "1234"  

    frame_teclado = Frame(miframe)  
    frame_teclado.grid(row=2, column=1, columnspan=3)  

    numeros = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    r = 0
    c = 0
    for num in numeros:
        btn = Button(frame_teclado, text=num, width=5, height=2, font=custom_font3,command=lambda n=num: insertar_numero(n))
        btn.grid(row=r, column=c, padx=5, pady=5)
        c += 1
        if c == 3:
            c = 0
            r += 1

    entry_contrasena = Entry(miframe, show="*", font=custom_font3)  
    entry_contrasena.grid(row=3, column=2, padx=10, pady=10,sticky='e')  

    btn_ingresar = Button(miframe, text="Ingresar",font=custom_font3, command=verificar_contrasena)  
    btn_ingresar.grid(row=4, column=2, padx=10, pady=10,sticky='e')  

    visualizar=Button(miframe, text='Volver',font=('8514oem',15),fg='#1F2733',command=lambda:monitoreo())
    visualizar.config(bg='#F5C25B',bd=3, relief='solid',width=15)
    visualizar.grid(row=4,column=3, padx=5, pady=5,sticky='w',columnspan=3)



if __name__ == "__main__":
    logo_screen()
    params_screen()
    