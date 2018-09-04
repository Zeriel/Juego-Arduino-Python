# Juego
El juego consiste en 4 plataformas con tiras de LEDs en el suelo, las cuales, al ser presionadas, pueden devolver uno de los siguientes valores, dependiendo de cuál fue elegida:
  - C
  - Z
  - E
  - Q

Se le indicará al usuario, mediante los LEDs, cual debe presionar. Dependiendo de su elección, el Sistema responderá con un comportamiento de música y de LEDs para cada caso.

Las distintas fases del juego son:
  - StandBy:      El estado inicial. El juego espera un input cualquiera. Musica tranquila.
  - esperarInput: Se designa una plataforma objetivo para el jugador. Se espera uno de los cuatro inputs definidos, o '0' para volver a StandBy. Música rápida.
  - correcto :    El jugador eligió la plataforma designada. Dura 5 segundos, luego vuelve a esperarInput. Música alegre.
  - incorrecto:   El jugador eligió otra plataforma. Dura 5 segundos, luego vuelve a esperarInput. Música agresiva.

# Python
Python es el lenguaje principal, encargado de administrar el juego, sus fases, las entradas que recibe de las plataformas, y la salida que le da al usuario, tanto la directa (reproduciendo música), como la indirecta (indicando el comportamiento de los LEDs al Arduino).

# Arduino
Arduino es el encargado de recibir un dato por Serial desde Python, evaluarlo, y decidir el comportamiento que tendrán los LEDs. Dichos comportamientos incluyen:
  - StandBy:      Las 4 tiras de LEDs "respiran", haciendo fadeIn y fadeOut. Activado con el valor 's'.
  - ok:           Valor correcto, se encienden las 4 tiras de LEDs, apagándose con un fadeOut tranquilo. Activado con el valor 'o'.
  - no-ok:        Valor incorrecto, las 4 tiras de LEDs destellan en forma agresiva, castigando al usuario. Activado con el valor 'n'.
  - indicarInput: Hace pestañar la tira de LEDs correspondiente a la plataforma que debe elegir el usuario. Activado con el valor correspondiente a la plataforma ('q' / 'e' / 'z' / 'c').
  
# Derechos de autor
La música usada en el juego por Python, son originalmente pistas de audio pertenecientes al soundtrack oficial del videojuego Portal 2, que fueron modificadas ligeramente para adecuarlas al mismo. De tal forma, no afirmo ser autor ni dueño de dichas pistas de audio.
