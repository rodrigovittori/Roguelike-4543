#pgzero
"""
Pack Kodland: https://kenney.nl/assets/roguelike-caves-dungeons (NO VIENE PRECORTADO)
packs de assets: https://kenney.nl/assets/series:Tiny?sort=update (LO TIENEN QUE ESCALAR)

pack escalado (drive del profe): https://drive.google.com/drive/folders/19obh4TK0RIBWlXOsaOq9uJ287jUHuLTn?usp=drive_link

Link al repo de GitHub: https://github.com/rodrigovittori/Roguelike-4543/

> Página para redimensionar assets https://imageresizer.com/bulk-resize/
============================================================================================================================

Version actual: [M9.L2] - Actividades Nº 2 "Generando Enemigos"
Objetivo: Crear nuestro primer enemigo y generar variaciones del mismo con componentes random/aleatorios

NOTA: La actividad Nº 1 "Revisando nuestro mapa de sueños" NO involucra nuestro juego.

Pasos:
#1: Importar random
#2: Creamos una constante que determine la cantidad de enemigos a spawnear (5)
#3: Creamos un bucle FOR donde calculamos la posición, la validamos,
    creamos los actores enemigos y les asignamos su salud y ataque con valores randomizados
#4: Agregamos un bucle FOR en nuestro draw() para mostrar los enemigos en pantalla

Nota: Pronto calcularemos las colisiones contra ellos
"""
import random

# Ventana de juego hecha de celdas
celda = Actor('border') # Celda que voy a utilizar como referencia para mi mapa

""" ******************************************************************* """
# Paleta de terrenos:
pared =  Actor("border") # 0: Pared de bloques
piso =   Actor("floor")  # 1: Suelo liso (sin decoración)
crack =  Actor("crack")  # 2: Suelo resquebrajado/quebradizo
huesos = Actor("bones")  # 3: Suelo con una pilita de huesos
""" ******************************************************************* """
cant_celdas_ancho = 9 # Ancho del mapa (en celdas)
cant_celdas_alto = 10 # Altura del mapa (en celdas)

WIDTH  = celda.width  * cant_celdas_ancho # Ancho de la ventana (en píxeles)
HEIGHT = celda.height * cant_celdas_alto  # Alto de la ventana (en píxeles)

TITLE = "Rogue-like: Mazmorra Maldita" # Título de la ventana de juego
FPS = 60 # Número de fotogramas por segundo

# Personaje:
personaje = Actor("stand")

# Nota: si quieren llevar control de la vida, pueden crear dos atributos: "salud_max" y "salud_actual"
personaje.salud = 100

# Nota: si quieren hacer más interesante el combate pueden agregar atributos para el valor mínimo de ataque y el máximo
# (también pueden implementar un sistema de miss y critical hits) Por ejemplo ataque de 2-5 de daño y crítico 2xMAX = 10
personaje.ataque = 5

################# ENEMIGOS ################

CANT_ENEMIGOS_A_SPAWNEAR = 5
lista_enemigos = []

############ GENERAR ENEMIGOS #############

# To-Do: migrar a función
while (len(lista_enemigos) < CANT_ENEMIGOS_A_SPAWNEAR):
    """ PASO 1: Generar coordenadas random """
    
    x = (random.randint(1, cant_celdas_ancho - 2) * celda.width)
    y = (random.randint(1, cant_celdas_alto - 3)  * celda.height)
    # To-Do: Agregar variable para determinar tipo de enemigo a spawnear
    
    nvo_enemigo = Actor("enemy", topleft = (x, y))

    """ PASO 2: Validar posición / evitar enemigos superpuestos """
    # Validamos que los enemigos no spawneen uno sobre el otro
    posicion_duplicada = False
    
    for enemigo in lista_enemigos:
        if (nvo_enemigo.pos == enemigo.pos): # Si la posición de nvo_enemigo es IGUAL a la de CUALQUIER enemigo en la lista,
            posicion_duplicada = True        # Actualizamos la flag que indica que la posicion está duplicada
            
    if (posicion_duplicada):
        continue
        
    else:
        """ PASO 3: Generar atributos random """
        # Si NO hay conflicto: randomizamos salud, ataque y lo agregamos a lista_enemigos
        nvo_enemigo.salud = random.randint(10, 20)
        nvo_enemigo.ataque = random.randint(5, 10)
        
        """ FINALMENTE, lo agregamos a la lista """
        lista_enemigos.append(nvo_enemigo)

################## MAPAS ##################

mapa = [ [0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 1, 2, 1, 3, 1, 1, 0],
         [0, 1, 1, 1, 2, 1, 1, 1, 0],
         [0, 1, 3, 2, 1, 1, 3, 1, 0],
         [0, 1, 1, 1, 1, 3, 1, 1, 0],
         [0, 1, 1, 3, 1, 1, 2, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0] ]

##########################################

mapa_actual = mapa # mapa a dibujar // cambiar valor si cambiamos de habitación

"""   #####################
     # FUNCIONES PROPIAS #
    #####################   """

def dibujar_mapa(mapa, mostrar_texto):

  for fila in range(len(mapa)):
    for columna in range(len(mapa[fila])):

      """
      Lista códigos terrenos
      
      0: pared
      1: piso (sin nada)
      2: piso (roto/resquebrajado)
      3: piso (c/ huesitos)
      """

      if (mapa[fila][columna] == 0): # pared
        pared.left = pared.width * columna
        pared.top = pared.height * fila
        pared.draw()

      elif (mapa[fila][columna] == 1): # piso (sin nada)
        piso.left = piso.width * columna
        piso.top = piso.height * fila
        piso.draw()

      elif (mapa[fila][columna] == 2): # piso (roto/resquebrajado)
        crack.left = crack.width * columna
        crack.top = crack.height * fila
        crack.draw()

      elif (mapa[fila][columna] == 3): # piso (c/ huesitos)
        huesos.left = huesos.width * columna
        huesos.top = huesos.height * fila
        huesos.draw()

      if (mostrar_texto):
          screen.draw.text( str(mapa_actual[fila][columna]),
                            center=( ( (celda.width * columna) + int(celda.width/2) ), ( (celda.height * fila) + int(celda.height/2)) ),
                            color="black", fontsize=32 )

"""   #####################
     # FUNCIONES PG-ZERO #
    #####################   """

def draw():
    screen.fill((200,200,200))
    dibujar_mapa(mapa = mapa_actual, mostrar_texto = False)
    personaje.draw()

    for enemigo in lista_enemigos:
        enemigo.draw()

    # Mostramos valores personaje:
    screen.draw.text(("❤️: " + str(personaje.salud)), midleft = (int(celda.width / 2), (HEIGHT - int(celda.height / 2))), color = 'black', fontsize = 36)
    screen.draw.text(("🗡️: " + str(personaje.ataque)), midright = ( (WIDTH - int(celda.width / 2)), (HEIGHT - int(celda.height / 2)) ), color = 'black', fontsize = 36)

def on_key_down(key):
  
  if ((keyboard.right or keyboard.d) and (personaje.x < (WIDTH - celda.width * 2))):
    # ¿Xq 2?: Una (a la que me voy a desplazar) y otra (por la pared, que NO puedo atravesar)
    personaje.x += celda.width
    personaje.image = "stand" # xq stand mira a la dcha
        
  elif ((keyboard.left or keyboard.a) and (personaje.x > (celda.width * 2))):
    personaje.x -= celda.width
    personaje.image = "left" # xq mira a la izq
        
  elif ((keyboard.down or keyboard.s) and (personaje.y < HEIGHT - celda.height * 3)):
    # ¿Xq 3?: Una (a la que me voy a desplazar), otra (por la pared, que NO puedo atravesar) Y UNA TERCERA (para mostrar el texto)
    personaje.y += celda.height
    
  elif ((keyboard.up or keyboard.w) and (personaje.y > (celda.height * 2))):
        personaje.y -= celda.height