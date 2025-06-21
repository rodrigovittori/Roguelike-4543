#pgzero
"""
Pack Kodland: https://kenney.nl/assets/roguelike-caves-dungeons (NO VIENE PRECORTADO)
packs de assets: https://kenney.nl/assets/series:Tiny?sort=update (LO TIENEN QUE ESCALAR)

pack escalado (drive del profe): https://drive.google.com/drive/folders/19obh4TK0RIBWlXOsaOq9uJ287jUHuLTn?usp=drive_link

Link al repo de GitHub: https://github.com/rodrigovittori/Roguelike-4543/

> Página para redimensionar assets https://imageresizer.com/bulk-resize/
============================================================================================================================

Version actual: [M9.L2] - Actividades Nº 5 "Aparición de las bonificaciones"
Objetivo del ejercicio: Agregar mecánicas de bonus, su spawn, mostrarlas en pantalla

NOTA: Todavía SEGUIMOS sin game-over (somos inmortales :D)

NOTA 2: Las colisiones con los bonus se programan en la SIGUIENTE tarea

Pasos:

#1: Crear una nueva lista para los bonus
#2: Durante la creación de enemigos vamos a asignarles un valor de bonus que dropearán tras ser derrotados
#3: Agregar un bucle en draw para dibujar los bonus en pantalla
#4: Al derrotar a un enemigo, spawnearemos el bonus que se le asignó al crearlo
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

colision = -2 # ¿XQ -2 como valor inicial?: porque es un valor que NO nos puede devolver collidelist.
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
        nvo_enemigo.bonus = random.randint(0, 2)   # 0: NADA / 1: curacion / 2: espadas
        
        """ FINALMENTE, lo agregamos a la lista """
        lista_enemigos.append(nvo_enemigo)

################## BONUS ##################

lista_bonus = []

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

    for bonus in lista_bonus:
        bonus.draw()
    
    for enemigo in lista_enemigos:
        enemigo.draw()

    # Mostramos valores personaje:
    screen.draw.text(("❤️: " + str(personaje.salud)), midleft = (int(celda.width / 2), (HEIGHT - int(celda.height / 2))), color = 'black', fontsize = 36)
    screen.draw.text(("🗡️: " + str(personaje.ataque)), midright = ( (WIDTH - int(celda.width / 2)), (HEIGHT - int(celda.height / 2)) ), color = 'black', fontsize = 36)

def on_key_down(key):
  global colision

  pos_previa = personaje.pos # Posición previa a pulsar la tecla
    
  # Movimiento personaje
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

 ################## COLISIONES ##################

  colision = personaje.collidelist(lista_enemigos)

  if (colision != -1):
      # Si hubo colisión con un enemigo:

      # Paso 1: Volvemos al personaje a su posición anterior:
      personaje.pos = pos_previa
      
      # Paso 2: Calculamos daños
      enemigo_atacado = lista_enemigos[colision]
      enemigo_atacado.salud -= personaje.ataque
      personaje.salud -= enemigo_atacado.ataque
      # Nota: Podríamos agregar un sistema de puntos de daño flotantes en pantalla

      # Si el enemigo se quedó sin puntos de salud, 
      if (enemigo_atacado.salud <= 0):
          # ANTES DE DESTRUÍRLO/ELIMINARLO -> Spawneamos bonus:
          if (enemigo_atacado.bonus == 0):
              # NADA
              enemigo_atacado.bonus += 0 # TENGO que poner algo para que python NO devuelva error
              
          elif (enemigo_atacado.bonus == 1):
              # Spawneamos curación:
              nvo_bonus = Actor("heart", enemigo_atacado.pos)    # Spawneo un nuevo bonus en la posición del enemigo derrotado
              lista_bonus.append(nvo_bonus)                      # Lo agrego a la lista de bonus

          elif (enemigo_atacado.bonus == 2):
              # Spawneamos mejora ataque:
              nvo_bonus = Actor("sword", enemigo_atacado.pos)    # Spawneo un nuevo bonus en la posición del enemigo derrotado
              lista_bonus.append(nvo_bonus)                      # Lo agrego a la lista de bonus

          # Ya creado el bonus, bye bye~♥
          
          # Método Nº 1: pop() con índice según colision
          #lista_enemigos.pop(colision)

          # Método Nº 2: remove(enemigo_atacado)
          lista_enemigos.remove(enemigo_atacado)

          # To-do: modificar la casilla / spawnear una pila de huesitos donde muere el esqueleto