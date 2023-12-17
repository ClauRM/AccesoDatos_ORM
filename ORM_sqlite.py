import tkinter as tk
import random
import math
import json
import sqlite3

#Declaracion de variables globales
personas = []
numeropersonas = 5

#Clase persona y metodos
class Persona:
    #constructor
    def __init__(self):
        self.posx = random.randint(0,700) #posicion entre 0 y ancho de ventana
        self.posy = random.randint(0,700)
        self.radio = 20
        self.direccion = random.randint(0,360)#angulo en radianes
        self.color = "#{:06x}".format(random.randint(0,0xFFFFFF))
        self.entidad = ""
    #metodo dibujar personas
    def dibuja(self):
        self.entidad = lienzo.create_oval(
            self.posx-self.radio/2,
            self.posy-self.radio/2,
            self.posx+self.radio/2,
            self.posy+self.radio/2,
            fill=self.color)
            #para centrar el ovalo en el lienzo
    #metodo mover personas
    def mueve(self):
        self.colisiona()#llama al metodo para que tenga en cuenta las paredes
        #mover la entidad de posicion(entidad, posicion en x, posicion en y)
        lienzo.move(self.entidad,
                    math.cos(self.direccion),
                    math.sin(self.direccion))
        #actualiza las posiciones
        self.posx += math.cos(self.direccion)
        self.posy += math.sin(self.direccion)
    #metodo colisionar cuando toquen las paredes
    def colisiona(self):
        if self.posx < 0 or self.posx > 700 or self.posy < 0 or self.posy > 700:
            self.direccion+=180 #si alguna posicion toca la pared cambia de sentido 180grados
#====================================

def guardarPersonas():
    print("Los datos se guardan en la bd jugadores.sqlite3")
    #guardar las personas en sql
    conexion = sqlite3.connect("jugadores.sqlite3") 
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM jugadores')
    conexion.commit()
    for persona in personas:
        cursor.execute('INSERT INTO jugadores VALUES (NULL,'+str(persona.posx)+','+str(persona.posy)+','+str(persona.radio)+','+str(persona.direccion)+',"'+str(persona.color)+'","'+str(persona.entidad)+'")')
    conexion.commit()
    conexion.close()

#Ventana
ventana = tk.Tk()

#Agregar lienzo a la ventana
lienzo = tk.Canvas(width=700,height=700)
lienzo.pack()

#Boton GUARDAR
botonGuardar = tk.Button(ventana, text="Guardar", command = guardarPersonas)
botonGuardar.pack()

#Cargar personas desde sql
try:
    conexion = sqlite3.connect("jugadores.sqlite3") 
    cursor = conexion.cursor()
    ##    cursor.execute('SELECT * FROM jugadores')
    cursor.execute('SELECT * FROM jugadores WHERE posx <100') #utilizando condiciones
    while True: #recorrer el resultado
        fila = cursor.fetchone()
        if fila is None:
            break
        #por cada fila, crear persona , tomar los valores del resultado y sumarlo al listado 
        persona = Persona()
        persona.posx = fila[1]
        persona.posy = fila[2]
        persona.radio = fila[3]
        persona.direccion = fila[4]
        persona.color = fila[5]
        persona.entidad = fila[6]
        personas.append(persona)
    conexion.close()
except:
    print("Error al leer la base de datos")

#Recorrer lista y crear personas
if len(personas) == 0: #si la lista esta vacia, crea personas
    numeropersonas = 5
    for i in range (0,numeropersonas):
        personas.append(Persona())

#Dibujar en el lienzo a cada persona de la lista personas
for persona in personas:
    persona.dibuja()

#Definir metodo bucle para mover a las personas
def bucle():
    for persona in personas:
        persona.mueve()
    ventana.after(5,bucle) #en 1seg=1000 ejecutar de nuevo el bucle mover a las personas

#Ejecutar bucle
bucle()

ventana.mainloop() #Empaquetar 
