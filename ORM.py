import tkinter as tk
import random

#Lista y numero de personas
personas = []
numeropersonas = 20

#Clase persona y metodos
class Persona:
    def __init__(self):
        self.posx = random.randint(0,700) #posicion entre 0 y 700
        self.posy = random.randint(0,700)
        self.radio = 20
        self.direccion = 0
        self.color = "blue"
        self.entidad = ""
    def dibuja(self):
        self.entidad = lienzo.create_oval(
            self.posx-self.radio/2,
            self.posy-self.radio/2,
            self.posx+self.radio/2,
            self.posy+self.radio/2,
            fill=self.color)
            #para centrar el ovalo en el lienzo
    def mueve(self):
        #mover la entidad de la posición 10 a 0
        lienzo.move(self.entidad,5,0) #5 es el numero de pixeles que se mueven

#Ventana
ventana = tk.Tk()

#Agregar lienzo a la ventana
lienzo = tk.Canvas(width=700,height=700)
lienzo.pack()

#Instanciar persona y agragarla a la lista
for i in range (0, numeropersonas):
    personas.append(Persona())

#Recorrer lista y dibujar personas
for persona in personas:
    persona.dibuja()

#Definir metodo bucle para mover a las personas
def bucle():
    for persona in personas:
        persona.mueve()
    ventana.after(1000,bucle) #en 1seg ejecutar de nuevo el bucle mover a las personas

#Ejecutar bucle
bucle()

ventana.mainloop() #Empaquetar 
