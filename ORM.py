import tkinter as tk
import random

personas = []
numeropersonas = 20

class Persona:
    def __init__(self):
        self.posx = random.randint(0,700) #posicion entre 0 y 700
        self.posy = random.randint(0,700)
        self.radio = 20
    def dibuja(self):
        lienzo.create_oval(
            self.posx-self.radio/2,
            self.posy-self.radio/2,
            self.posx+self.radio/2,
            self.posy+self.radio/2,
            fill="red")
            #para centrar el ovalo en el lienzo

ventana = tk.Tk()

lienzo = tk.Canvas(width=700,height=700)
lienzo.pack()

for i in range (0, numeropersonas):
    personas.append(Persona())

for persona in personas:
    persona.dibuja()

ventana.mainloop()
