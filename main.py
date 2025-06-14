#pgzero

"""
Pack Kodland: https://kenney.nl/assets/roguelike-caves-dungeons (NO VIENE PRECORTADO)
packs de assets: https://kenney.nl/assets/series:Tiny?sort=update (LO TIENEN QUE ESCALAR)

pack escalado (drive del profe): https://drive.google.com/drive/folders/19obh4TK0RIBWlXOsaOq9uJ287jUHuLTn?usp=drive_link

> Página para redimensionar assets https://imageresizer.com/bulk-resize/
============================================================================================================================

Version actual: [M9.L1] - Actividad #5: "Atributos"
Objetivo: Familiarizarnos con los atributos agregando salud y ataque a nuestro personaje
          > Creamos nuestro personaje como un objeto Actor() con sus respectivos atributos y los mostramos por pantalla

NOTA: La actividad #4 fue resuelta con el código de la actividad #3

PASOS:

1º) Creamos Actor() personaje
2º) Le damos sus atributos (salud, ataque)
3º) Eliminamos update(dt) y modificamos nuestra función draw() (rem: apagar texto)

NOTA: En el próximo ejercicio implementaremos el despalzamiento entre celdas por turnos con on_key_down(key)
"""

# Ventana de juego hecha de celdas
celda = Actor('border') # Celda que voy a utilizar como referencia para mi mapa

""" ******************************************************************* """
# Paleta de terrenos:
pared =  Actor("border") # 0: Pared de bloques
piso =   Actor("floor")  # 1: Suelo liso (sin decoración)
crack =  Actor("crack")  # 2: Suelo resquebrajado/quebradizo
huesos = Actor("bones")  # 3: Suelo con una pilita de huesos
""" ******************************************************************* """
cant_celdas_ancho = 7 # Ancho del mapa (en celdas)
cant_celdas_alto =  7 # Altura del mapa (en celdas)

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

################## MAPAS ##################

mapa = [ [0, 0, 0, 0, 0, 0, 0],
         [0, 1, 2, 1, 3, 1, 0],
         [0, 1, 1, 2, 1, 1, 0],
         [0, 3, 2, 1, 1, 3, 0],
         [0, 1, 1, 1, 3, 1, 0],
         [0, 1, 3, 1, 1, 2, 0],
         [0, 0, 0, 0, 0, 0, 0] ]

mapa_2 = [ [0, 0, 0, 0, 0, 0, 0],
           [0, 1, 1, 1, 1, 1, 0],
           [0, 1, 3, 1, 3, 1, 0],
           [0, 1, 1, 1, 1, 1, 0],
           [0, 3, 1, 1, 1, 3, 0],
           [0, 1, 3, 3, 3, 1, 0],
           [0, 0, 0, 0, 0, 0, 0] ]

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

    # Mostramos valores personaje:
    screen.draw.text(("❤️: " + str(personaje.salud)), midright=((WIDTH - 15), 14), color = 'white', fontsize = 16)
    screen.draw.text(("🗡️: " + str(personaje.ataque)), midright=((WIDTH - 15), 36), color = 'white', fontsize = 16)

def update(dt):
    global mapa_actual
    
    if keyboard.space:
        if mapa_actual == mapa:
            mapa_actual = mapa_2
        else:
            mapa_actual = mapa