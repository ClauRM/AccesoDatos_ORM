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
        self.energia = 100
        self.descanso = 100
        self.entidadenergia = ""
        self.entidaddescanso = ""
    #metodo dibujar personas
    def dibuja(self):
        #dibujar a la persona como un circulo
        self.entidad = lienzo.create_oval(
            self.posx-self.radio/2,
            self.posy-self.radio/2,
            self.posx+self.radio/2,
            self.posy+self.radio/2,
            fill=self.color)
        #dibujar su barra de energia como un rectangulo
        self.entidadenergia = lienzo.create_rectangle(
            self.posx-self.radio/2,
            self.posy-self.radio/2-10,
            self.posx+self.radio/2,
            self.posy-self.radio/2-7,
            fill="green")
        #dibujar su barra de descanso como un rectangulo
        self.entidaddescanso = lienzo.create_rectangle(
            self.posx-self.radio/2,
            self.posy-self.radio/2-17,
            self.posx+self.radio/2,
            self.posy-self.radio/2-14,
            fill="green")
    #metodo mover personas
    def mueve(self):
        #restar energia y descanso en cada movimiento
        if self.energia >0:
            self.energia -= 0.1
        if self.descanso >0:
            self.descanso -= 0.1
        #con cada movimiento verificar si esta en la pared para chocar
        self.colisiona()
        #mover la entidad de posicion(entidad, posicion en x, posicion en y)
        lienzo.move(self.entidad,
                    math.cos(self.direccion),
                    math.sin(self.direccion))
        #mover la barra de energia e ir disminuyendo
        anchuraenergia = (self.energia/100)*self.radio
        lienzo.coords(self.entidadenergia,
                    self.posx-self.radio/2,
                    self.posy-self.radio/2-10,
                    self.posx-self.radio/2+anchuraenergia,
                    self.posy-self.radio/2-7)
        #mover la barra de descanso
        anchuradescanso = (self.energia/100)*self.radio
        lienzo.coords(self.entidaddescanso,
                    self.posx-self.radio/2,
                    self.posy-self.radio/2-17,
                    self.posx-self.radio/2+anchuradescanso,
                    self.posy-self.radio/2-14)
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
    cursor.execute('SELECT * FROM jugadores')
    ##    cursor.execute('SELECT * FROM jugadores WHERE posx <100') #utilizando condiciones
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
