#   Programa para controlar LEDs mediante un Arduino, segun la entrada del usuario
#   Version: 1.0 | Release
#   Autor: Federico Moradillo
#
#   Encabezado del Programa
#   Importo las librerias necesarias
import msvcrt   #   Para usar el getch en Windows
import os       #   Para llamar las System Calls de Windows (clearScreen)
import random   #   Para usar la funcion random
import vlc      #   Para crear el reproductor de musica
import time     #   Para manejar tiempos en el programa
import serial   #   Para comunicarme por serial con el Arduino

from colorama import init, Fore, Back, Style   #   Estilo de la consola con Colorama
init()


#   ----------------------------------------------------------------------------------------
#   ----    VLC    ----
#   Creo una instancia de vlc con la configuracion para repetir el audio
instance = vlc.Instance('--input-repeat=-1')

#Con la instancia anterior, creo el reproductor
player = instance.media_player_new()

#   Defino la musica, para reproducir es variable.play(), para detener variable.stop()
standby = instance.media_new("assets/sounds/standby.wav")
incorrecto = instance.media_new("assets/sounds/incorrecto.wav")
correcto = instance.media_new("assets/sounds/correcto.wav")
esperandoInput = instance.media_new("assets/sounds/esperandoInput.wav")

#   ----------------------------------------------------------------------------------------
#   ----    RANDOM    ----
#   Defino la funcion que valida que el valor random no es el que eligio antes
def generate_random(lista, valorAnterior):
    posible = random.choice(lista)
    while (posible == valorAnterior):
        posible = random.choice(lista)
    return posible

#   Defino mi array de botones
botones = ['q', 'z', 'e', 'c']

#   ----------------------------------------------------------------------------------------
#   ----    OS  ----
#   Defino clearScreen para limpiar pantalla
def cls():
    os.system('cls' if os.name=='nt' else 'clear')

#   ----------------------------------------------------------------------------------------
#   ----    SERIAL  ----
print('ATENCION: Para cambiar el puerto COM, debera reiniciar la aplicacion')
numCOM = input('Ingrese puerto COM (USB) donde esta el arduino (1, 2, 3, etc): ')
#   Creo el puerto COM segun lo que ingresa el usuario, y abro conexion por ese canal en 9600 baud
COM = 'COM' + numCOM
ser = serial.Serial(COM,9600)
cls()
print('El COM ingresado es el ', COM, '. Si no es correcto, reinicie la aplicacion')
print('Presione una tecla para continuar...')
msvcrt.getch()
cls()

#   Valores a enviar por el ser.write():
#   's'    -> StandBy, el estado inicial. Los 4 LEDs "respiran" (fade in/fade out)
#   'q' / 'z' / 'e' / 'c' -> Indica el led a encender, es decir, el que debe presionar el usuario
#   'o'    -> Indica que presiono el led correcto
#   'n'    -> Indica que presiono el led incorrecto

#   ----------------------------------------------------------------------------------------
#   Comienza el programa

#   Ciclo infinito, el juego no tiene fin
while True:
    ser.write(bytes(b's'))                  #   Envio el valor StandBy, para la musica de fondo y LEDs respirando
    #   En la primer ejecucion, puede que el StandBy no llegue al arduino. Usar '0' para reiniciar el juego lo soluciona

    valorAnterior = 'pp'                    #   Lo inicializo en un valor imposible
    target = generate_random(botones, valorAnterior)    #   Obtengo un valor random
    player.set_media(standby)               #   Cargo el sonido a reproducir
    player.play()                           #   Reproduzco el sonido
    cls()
    print ('JUEGO EN STANDBY\nToque una tecla para iniciar el juego\n')
    valor_entrada = msvcrt.getwch()         #   Leo dato del usuario
    cls()

    #   Aca elimino los estados StandBy, y con la obtencion del siguiente valor comienza el juego
    player.stop()                           #   Detengo el sonido
    player.set_media(esperandoInput)        #   Cambio el sonido
    player.play()                           #   Reproduzco el nuevo sonido
    ser.write(str.encode(target))           #   Envio el Target, para que ilumine ese led
    print ('Inicia el juego, el primer valor es: ', target)
    valor_entrada = msvcrt.getwch()
    cls()

    #   Comienza juego, con 0 vuelve a estado StandBy
    while valor_entrada != '0': 
        player.stop()                       #   Detengo el sonido de esperar input
        cls()

        #   Rama VERDADERA, el usuario presiono el boton indicado
        if (valor_entrada.lower() == target):
            ser.write(bytes(b'o'))          #   Envio "OK" al Arduino, secuencia de LEDs de CORRECTO
            player.set_media(correcto)      #   Reproduzco el sonido de correcto
            player.play()
            cls()
            for i in range(5,0,-1):         #   FOR unicamente para variar el "i" en el mensaje, no tiene funcionalidad
                print(Back.GREEN + 'Correcto, eligiendo nuevo valor en ', i, '...')
                time.sleep(1)
                print(Style.RESET_ALL)
                cls()
            valorAnterior = target          #   Almaceno el target actual para la siguiente iteracion
            target = generate_random(botones, valorAnterior)    #   Genero nuevo target

        #   Rama FALSA, el usuario no presiono el boton indicado
        else:
            valorAnterior = valor_entrada   #   Para que entre al WHILE al final
            ser.write(bytes(b'n'))          #   Envio "NO-OK" al Arduino, secuencia de LEDs de INCORRECTO
            player.set_media(incorrecto)    #   Reproduzco el sonido de incorrecto
            player.play()
            cls()
            for i in range(5,0,-1):         #   FOR unicamente para variar el i en el mensaje, no tiene funcionalidad
                print(Back.RED + 'ERROR - Valor incorrecto. Volviendo en ', i, '...')
                time.sleep(1)
                print(Style.RESET_ALL)
                cls()
        player.stop()                       #   Detengo el sonido de correcto/incorrecto
        player.set_media(esperandoInput)    #   Cargo el tema de input nuevamente
        player.play()
        print(Style.RESET_ALL)
        cls()
        ser.write(str.encode(target))
        print ('Debe presionar ', target, '\n')
        valor_entrada = msvcrt.getwch()
        while valor_entrada == valorAnterior:   #   Con este loop, no tengo en cuenta si presiona la misma tecla otra vez,
            cls()                               #   por si se queda parado en la plataforma, lo cual daria error siempre
            print ('Debe presionar ', target, '\n')
            valor_entrada = msvcrt.getwch()
    cls()