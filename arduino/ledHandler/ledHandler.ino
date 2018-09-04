//Las salidas PWM para cada plataforma (tira de LED)
int ledQ = 5;   //La señal para la Q
int ledZ = 6;   //La señal para la Z
int ledE = 9;   //La señal para la E
int ledC = 11;  //La señal para la C

//Para controlar el fadeIn y fadeOut de las tiras
int fadeValue;

//La variable que recibe dato del Serial, y la segunda variable que lo almacena para que persista
char ledOrder, order;

//Variable para controlar los ciclos WHILE
bool stopWhile = false;

void setup(){
  //Establezco conexion en 9600 baud
  Serial.begin(9600);
  //Por defecto, apago todas las tiras de LED
  analogWrite(ledC, 0);
  analogWrite(ledE, 0);
  analogWrite(ledQ, 0);
  analogWrite(ledZ, 0);
}

void loop(){
  
//  El serial se pisa y borra el dato, por lo que es imposible loopear en base al dato que leo, entonces:

//  1) Leo el serial en una variable, y guardo en OTRA variable lo que recibio
  if (Serial.available() > 0){  //Si hay comunicacion serial
    order = Serial.read();      //Leo el dato
  }

//Case para decidir que caracter fue enviado en el paso anterior, para almacenarlo y que persista
  switch (order) {
    case 'o':
      ledOrder = 'o';
      break;
    case 'n':
      ledOrder = 'n';
      break;
    case 'q':
      ledOrder = 'q';
      break;
    case 'z':
      ledOrder = 'z';
      break;
    break;
    case 'e':
      ledOrder = 'e';
      break;
    break;
    case 'c':
      ledOrder = 'c';
      break;
    break;
    case 's':
      ledOrder = 's';
      break;
  }

//  2) Uso la SEGUNDA variable (que guarde en el primer case) para poder loopear

//  Para modificar todos los LEDs en una sola sentencia, tengo definida la funcion "leds(intensidad)" al final
  switch (ledOrder) {
  //Caso correcto, se encienden los LEDs en maxima intensidad, y se apagan con fadeOut
  case 'o':
    fadeValue = 255;
    stopWhile = false;
    //Mientras los LEDs no esten apagados, o el usuario no presione una tecla, itero
    while (fadeValue >= 0 && stopWhile == false) {
      leds(fadeValue);  //LEDs con la intensidad que tiene fadeValue
      delay(100);       //Espero 0,1 segundos, para que se vea el efecto fade
      fadeValue -= 5;   //Decremento fadeValue
      if (Serial.available() > 0){  //Para poder detener el while y arrancar el juego si se presiona una tecla
        stopWhile = true;
      }
    }
    break;
  //Caso incorrecto, hago destellar a todos los LEDs en forma violenta
  case 'n':
    leds(0);     //Apago LEDs
    delay(100);  //Espero  
    leds(255);   //Enciendo LEDs
    delay(100);  //Espero    
    leds(0);     //Apago LEDs
    break;
  //Hago destellar la Q
  case 'q':
      //Apago los 4 LEDs
      leds(0);  
      delay(500);
      //Enciendo Q
      analogWrite(ledQ, 255);
      delay(500);
      break;
  //Hago destellar la Z
  case 'z':
    //Apago los 4 LEDs
    leds(0);  
    delay(500);
    //Enciendo Z
    analogWrite(ledZ, 255);
    delay(500);
    break;
  //Hago destellar la E
  case 'e':
    //Apago los 4 LEDs
    leds(0);  
    delay(500);
    //Enciendo E
    analogWrite(ledE, 255);
    delay(500);
    break;
  //Hago destellar la C
  case 'c':
    //Apago los 4 LEDs
    leds(0);  
    delay(500);
    //Enciendo C
    analogWrite(ledC, 255);
    delay(500);
    break;
  //Estado StandBy, enciendo LEDs con fadeIn y los apago con fadeOut, simulando "respirar"
  case 's':
    //Enciendo LEDs con fadeIn
    stopWhile = false;
    fadeValue = 0;
    while (fadeValue <= 255 && stopWhile == false) {
      leds(fadeValue);
      delay(100);
      fadeValue += 10;
      if (Serial.available() > 0){  //Para poder detener el while y arrancar el juego si se presiona una tecla
        stopWhile = true;
      }
    }
    //Apago LEDs con fadeOut
    fadeValue = 255;
    while (fadeValue >= 0 && stopWhile == false ) {
      leds(fadeValue);
      delay(100);
      fadeValue -= 10;
      if (Serial.available() > 0){  //Para poder detener el while y arrancar el juego si se presiona una tecla
        stopWhile = true;
      }
    }
    break;
  }
}

//Este procedimiento recibe un valor entero y lo escribe como salida PWM a los 4 LEDs, para simplificar codigo
void leds(int valor){
  analogWrite(ledC, valor);
  analogWrite(ledE, valor);
  analogWrite(ledQ, valor);
  analogWrite(ledZ, valor); 
}
