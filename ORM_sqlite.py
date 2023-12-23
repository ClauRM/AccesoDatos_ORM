import tkinter as tk
import random
import math
import json
import sqlite3
#Declaracion de variables globales
personas = []
numeropersonas = 5
roles = ["TRIPULANTE","IMPOSTOR","DETECTIVE"]

#Case entidad
# class Entidad:
#     def __init__(self):#constructor
#         self.posx = random.randint(0,700) #posicion entre 0 y ancho de ventana
#         self.posy = random.randint(0,700)
#         self.color = "#{:06x}".format(random.randint(0,0xFFFFFF))

#Case recogible
class Recogible(): #Recogible extends Entidad
    def __init__(self):
        self.posx = random.randint(0,700) #posicion entre 0 y ancho de ventana
        self.posy = random.randint(0,700)
        self.color = "#{:06x}".format(random.randint(0,0xFFFFFF))
    #metodo para crear objetos dentro de objetos (json)
    def serializar(self): 
        recogible_serializado ={
            "posx":self.posx,
            "posy":self.posy,
            "color":self.color
            }
        return recogible_serializado

#Clase persona y metodos
class Persona(): #Persona extends Entidad
    def __init__(self):
        self.posx = random.randint(0,700) #posicion entre 0 y ancho de ventana
        self.posy = random.randint(0,700)
        self.color = "#{:06x}".format(random.randint(0,0xFFFFFF))
        self.radio = 20
        self.direccion = random.randint(0,360)#angulo en radianes
        self.entidad = ""
        self.energia = 100
        self.descanso = 100
        self.entidadenergia = ""
        self.entidaddescanso = ""
        self.rol = random.choice(roles)
        self.etiquetarol = ""
        self.inventario = []
        self.inventario.append(Recogible()) #new Recogible
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
            self.posx+self.radio,
            self.posy-self.radio-7,
            fill="green")
        #dibujar su barra de descanso como un rectangulo
        self.entidaddescanso = lienzo.create_rectangle(
            self.posx-self.radio/2,
            self.posy-self.radio/2-17,
            self.posx+self.radio/2,
            self.posy-self.radio/2-14,
            fill="blue")
        #dibujar el rol
        self.etiquetarol = lienzo.create_text(
            (self.posx, self.posy),
            text=self.rol,
            fill="blue",
            font='tkDefaeultFont 8'
            )
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
        anchuradescanso = (self.descanso/100)*self.radio
        lienzo.coords(self.entidaddescanso,
                    self.posx-self.radio/2,
                    self.posy-self.radio/2-17,
                    self.posx-self.radio/2+anchuradescanso,
                    self.posy-self.radio/2-14)
        #mover el rotulo del rol
        lienzo.coords(self.etiquetarol,
                      self.posx,
                      self.posy+30)
        #actualiza las posiciones
        self.posx += math.cos(self.direccion)
        self.posy += math.sin(self.direccion)
    #metodo colisionar cuando toquen las paredes
    def colisiona(self):
        if self.posx < 0 or self.posx > 700 or self.posy < 0 or self.posy > 700:
            self.direccion+=180 #si alguna posicion toca la pared cambia de sentido 180grados
    #metodo para crear objetos dentro de objetos (json)
    def serializar(self):
        persona_serializada ={
            "posx":self.posx,
            "posy":self.posy,
            "radio":self.radio,
            "direccion":self.direccion,
            "color":self.color,
            "energia":self.energia,
            "descanso":self.descanso,
            "rol":self.rol,
            "inventario":[item.serializar() for item in self.inventario]
            }
        return persona_serializada
#====================================
def guardarPersonas():
    #guardar con fines demostrativos
    personas_serializadas = [persona.serializar() for persona in personas]
    print("Datos a guardar en json:")
    # cadena = json.dumps(personas_serializadas) #crear la cadena persona para cada persona
    # print(cadena)
    # archivo = open("jugadores.json",'w')#abrir archivo
    # archivo.write(cadena)#guardar cadena en archivo
    with open("jugadores.json","w") as archivo: #abrir archivo
        json.dump(personas_serializadas,archivo,indent=4)#almacenar personas serializadas en archivo

    print("Los datos se guardan en la bd jugadores.sqlite3")
    #guardar las personas en sql
    conexion = sqlite3.connect("jugadores.sqlite3") 
    cursor = conexion.cursor()
    cursor.execute('DELETE FROM jugadores')
    conexion.commit()
    for persona in personas:
        cursor.execute('INSERT INTO jugadores VALUES (NULL,'+str(persona.posx)+','+str(persona.posy)+','+str(persona.radio)+','+str(persona.direccion)+',"'+str(persona.color)+'","'+str(persona.entidad)+'",'+str(persona.energia)+','+str(persona.descanso)+',"'+str(persona.entidadenergia)+'","'+str(persona.entidaddescanso)+'","'+str(persona.rol)+'","'+str(persona.inventario)+'")')
    conexion.commit()
    conexion.close()

def nuevoJuego():
    #Limpiar canvas
    lienzo.delete("all")
    #Vaciar la lista y crear nuevas personas
    personas.clear() 
    numeropersonas = 5
    for i in range (0,numeropersonas):
        personas.append(Persona())

    #Dibujar en el lienzo a cada persona de la lista personas
    for persona in personas:
        persona.dibuja()

def salirJuego():
    ventana.destroy()

#Ventana
ventana = tk.Tk()

#Agregar lienzo a la ventana
lienzo = tk.Canvas(width=700,height=700)
lienzo.pack()
#Boton GUARDAR
botonGuardar = tk.Button(ventana, text="Guardar", command = guardarPersonas)
botonGuardar.pack()

#Boton NUEVO
botonGuardar = tk.Button(ventana, text="Nuevo", command = nuevoJuego)
botonGuardar.pack()

#Boton SALIR
botonGuardar = tk.Button(ventana, text="Salir", command = salirJuego)
botonGuardar.pack()

#Cargar personas desde sql
try:
    conexion = sqlite3.connect("jugadores.sqlite3") 
    cursor = conexion.cursor()
    cursor.execute('SELECT * FROM jugadores')
    ##    cursor.execute('SELECT * FROM jugadores WHERE posx <100') #utilizando condiciones
    ##    cursor.execute('SELECT * FROM jugadores WHERE rol="IMPOSTOR"') #utilizando condiciones
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
        persona.energia = fila[7]
        persona.descanso = fila[8]
        persona.entidadenergia = fila[9]
        persona.entidaddescanso = fila[10]
        persona.rol = fila[11]
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