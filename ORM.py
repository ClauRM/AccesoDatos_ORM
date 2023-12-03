import tkinter as tk
import random

class Persona:
    def __init__(self):
        self.posx = random.randint(0,350) #posicion 350 es la mitad del lienzo
        self.posy = random.randint(0,350)
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

persona = Persona()
persona.dibuja()

ventana.mainloop()
