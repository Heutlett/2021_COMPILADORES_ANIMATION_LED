
#define ROW_1 2
#define ROW_2 3
#define ROW_3 4
#define ROW_4 5
#define ROW_5 6
#define ROW_6 7
#define ROW_7 8
#define ROW_8 9

#define COL_1 10
#define COL_2 11
#define COL_3 12
#define COL_4 13
#define COL_5 A0
#define COL_6 A1
#define COL_7 A2
#define COL_8 A3

//==============================================================================================================================
//***************************************************VARIABLES GLOBALES*********************************************************
//==============================================================================================================================

//Arreglos para manejo de matriz de leds
const byte rows[] = {
    ROW_1, ROW_2, ROW_3, ROW_4, ROW_5, ROW_6, ROW_7, ROW_8
};
const byte col[] = {
  COL_1,COL_2, COL_3, COL_4, COL_5, COL_6, COL_7, COL_8
};

//Manejo de conversiones Hexadecimal - Binario
String h = "0123456789ABCDEF";
String b[16] = {"0000","0001","0010","0011","0100","0101","0110","0111","1000","1001","1010","1011","1100","1101","1110","1111"};


//Almacena instrucciones
String mtrxS[20];
                   
//Buffer, almacena mensaje Serial
String inBytes;

//------------Variables del controlador-----------------
int p = 0; //

int rsize=0; //Tamaño-cantidad de instrucciones a leer

bool runcron=false; //Cronometro empieza a correr

int cron=0; //Cronometro

int frame = 0; //Instrucción que se está revisando

int dlay = 0; //Cuantos delays se han encontrado después del último frame

String current; //Frame que se debe imprimir

int wait=0; //Tiempo que se debe esperar antes de pasar a la siguiente instrucción
//------------------------------------------------------

void setup() 
{
    // Se abre el puerto Serial
    Serial.begin(9600);
    
    // Set establece todos los pines usados en OUTPUT
    // Muy importante, pues si están en INPUT la luz
    // de la matriz será muy tenue
    for (byte i = 2; i <= 13; i++)
        pinMode(i, OUTPUT);
    pinMode(A0, OUTPUT);
    pinMode(A1, OUTPUT);
    pinMode(A2, OUTPUT);
    pinMode(A3, OUTPUT);
}

void loop() {

// Si se recibe una entrada Serial, se imprime un mensaje
// y seguidamente se acomodan las reglas en mtrxS
if(Serial.available()>0){
      inBytes = Serial.readStringUntil('\n');
      Serial.println("Se recibe entrada");
      buildRules(inBytes);
      //printMatriz();
      runcron=true;   
}

// No será hasta que se reciba una entrada Serial que
// el cronometro empiece a andar
if (runcron){
  cron++;
  current = mtrxS[frame-dlay];
  drawScreen3(current);
}

// Ciclo del cronometro ajustable
if ((cron%1)==0){
  if (frame == p){
    Serial.println("AGAIN");// Inicia nuevamente el ciclo de animación
    frame=0;
    }
  else{
    if (wait<=0){
      Serial.println("FRAME++"); // Se pasa al siguiente "frame"
      frame++;
      if (mtrxS[frame][0]=='2'){
        managgeDelay(mtrxS[frame]);
        dlay+=1;
      }
      else{
        dlay=0;
      }
    }else{
      Serial.print("WAIT--"); // Se disminuye una unidad en el "wait"
      Serial.println(wait);
      wait--;
    }
  }
}
}


/**
 * managgeDelay
 * @param String msg
 * Maneja el delay, analiza la instrucción y distribuye
 * la cantidad d epuntos a esperar.
 */
 void managgeDelay(String msg){
    if(msg[1]=='1'){
      wait+=getNum(msg);
    }
    if(msg[1]=='2'){
      wait+=getNum(msg)*100;
    }
    if(msg[1]=='3'){
      wait+=getNum(msg)*100*60;
    }   
 }

/**
 * getNum
 * @param String msg
 * @return int numero
 * Obtiene la cantidad que se debe esperar para 
 * un determinado delay.
 */
 int getNum(String msg){
    String str = "";
    char c_arr[5];
    bool founded=false;
    for (int i=0;i<4;i++){
      str += msg[2+i];
    }
    strcpy(c_arr, str.c_str());
    Serial.print("WAIT: ");
    Serial.println(atoi(c_arr));
    return atoi(c_arr); 
 }

/**
 * drawScreen3
 * @param String matrix
 * Recibe la matriz en forma de string de 64 bits
 * y lo interpreta para encender los leds respectivos
 */
 void  drawScreen3(String matrix)
 { 
   // Enciende cada fila
    for (int i = 0; i < 8; i++)        // cuenta a la siguiente fila
     {
        digitalWrite(rows[i], HIGH);    //enciende una fila completa
        for (int a = 0; a < 8; a++)    // cuenta a la siguiente columna
        {
          if (matrix[(8*a)+i]=='1'){
            digitalWrite(col[a], 0);  
          }
          if (matrix[(8*a)+i]=='0'){
            digitalWrite(col[a], 1);  
          }
          
          digitalWrite(col[a], 1);      // apaga una columna
        }
        digitalWrite(rows[i], LOW);     // apaga una fila
    }
}


/**
 * printMatriz
 * Se utilza para realizar pruebas, realiza la
 * impresión en consola de las instrucciones dentro
 * del arreglo.
 */
void printMatriz(){
  Serial.println (rsize);
  for (int i = 0; i<rsize; i++){
    //for (int j = 0; j<8; j++){
      //for (int k = 0; k<8; k++){
      Serial.print(mtrxS[i]);  
      Serial.println(";");
      //}
    Serial.println("============");
    }
  }

/**
 * buildRules
 * @param String msg
 * Realiza la lectura del String proveniente del Serial
 * mediante otras funciones envía intervalos extraidos
 * del String para ser integrados en el arreglo de 
 * instrucciones.
 */
void buildRules(String msg){
  int c = 0;
  int i = 0;
  while(msg[i] != ')'){
    Serial.println(msg[i]);
    if(msg[i] == 'P'){
      buildMtrx(msg,i+1,c,1);
      c++;
      }
    if(msg[i] == 'T'){
      buildMtrx(msg,i+1,c,2);
      c++;
      }
    i++;
    }
    rsize=c;
  }

/**
 * getNum
 * @param String msg, int i, int c, int op
 * Mediante la instrucción y una operación dada,
 * llena el arreglo de instrucciones.
 */
void buildMtrx(String msg, int i, int c, int op){
  if (op==1){
    mtrxS[p]= hextobin(msg,i);
    }
  if (op==2){
    mtrxS[p]= delayer(msg,i);
    }
  printMatriz();
  p++;
  }

/**
 * delayer
 * @param String msg, int i
 * @return String instruccion
 * Convierte instruccion delay del Serial
 * a instruccion entendible para el controlador.
 */
String delayer(String msg, int i){
  String rslt = "2";
  String time_u= "";

  if(msg[i] == 'N'){
    rslt+="1";
  }
  if(msg[i] == 'S'){
    rslt+="2";
  }
  if(msg[i] == 'M'){
    rslt+="3";
  }
  
  for(int j=1;j<5;j++){
      time_u+=msg[j+i];
  }
  rslt+=time_u;   
  return rslt;
}
  
/**
 * hextobin
 * @param String msg, int i
 * @return String binary
 * A partir de una cadena de hexadecimales,
 * convierte el número a binario.
 */
String hextobin(String msg, int i){
  String reslt = "";
  for(int j = 0; j<16; j++){
    for(int k = 0; k<16; k++){
      //Serial.print(h[k]);
      //Serial.print("-----");
      //Serial.print(msg[i+j]);
      if(h[k]==msg[i+j]){
        reslt += b[k];
        break;
        }
      //Serial.println("");
      }
    }
    return reslt;
  }
