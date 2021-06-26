
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

const byte rows[] = {
    ROW_1, ROW_2, ROW_3, ROW_4, ROW_5, ROW_6, ROW_7, ROW_8
};
const byte col[] = {
  COL_1,COL_2, COL_3, COL_4, COL_5, COL_6, COL_7, COL_8
};


String h = "0123456789ABCDEF";
String b[16] = {"0000","0001","0010","0011","0100","0101","0110","0111","1000","1001","1010","1011","1100","1101","1110","1111"};



String mtrxS[20];
                   


float timeCount = 0;


String inBytes;

int p = 0;

int s = 0;

int t = 1;

int rsize=2;

bool runcron=false;

int cron=0;

int frame = 0;

int dlay = 0;

int dlay_c = 0;

String current;

int wait=0;

void setup() 
{
    // Open serial port
    Serial.begin(9600);
    
    // Set all used pins to OUTPUT
    // This is very important! If the pins are set to input
    // the display will be very dim.
    for (byte i = 2; i <= 13; i++)
        pinMode(i, OUTPUT);
    pinMode(A0, OUTPUT);
    pinMode(A1, OUTPUT);
    pinMode(A2, OUTPUT);
    pinMode(A3, OUTPUT);
}

void loop() {

if(Serial.available()>0){
      inBytes = Serial.readStringUntil('\n');
      Serial.println("LLEGAA");
      buildRules(inBytes);
      Serial.println("SE LOGRA");
      printMatriz();
      runcron=true;
      //Serial.print(inBytes);      
}


if (runcron){
  cron++;
  current = mtrxS[frame-dlay];
  drawScreen3(current);
}

if ((cron%1)==0){
  if (frame == p){
    Serial.println("AGAIN");
    frame=0;
    }
  else{
    if (wait<=0){
      Serial.println("FRAME++");
      frame++;
      if (mtrxS[frame][0]=='2'){
        managgeDelay(mtrxS[frame]);
        dlay+=1;
      }
      else{
        dlay=0;
      }
    }else{
      Serial.print("WAIT--");
      Serial.println(wait);
      wait--;
    }
  }
}
}



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
 
 void  drawScreen(byte buffer2[])
 { 
   // Turn on each row in series
    for (int i = 0; i < 8; i++)        // count next row
     {
        digitalWrite(rows[i], HIGH);    //initiate whole row
        for (int a = 0; a < 8; a++)    // count next row
        {
          // if You set (~buffer2[i] >> a) then You will have positive
          digitalWrite(col[a], (~buffer2[a] >> i) & 0x01); // initiate whole column
          
          delayMicroseconds(100);       // uncoment deley for diferent speed of display
          //delayMicroseconds(1000);
          //delay(10);
          //delay(100);
          
          digitalWrite(col[a], 1);      // reset whole column
        }
        digitalWrite(rows[i], LOW);     // reset whole row
        // otherwise last row will intersect with next row
    }
}
 void  drawScreen2(int matrix[8][8])
 { 
   // Turn on each row in series
    for (int i = 0; i < 8; i++)        // count next row
     {
        digitalWrite(rows[i], HIGH);    //initiate whole row
        for (int a = 0; a < 8; a++)    // count next row
        {
          // if You set (~buffer2[i] >> a) then You will have positive
          digitalWrite(col[a], (~matrix[a][i])& 0x01); // initiate whole column
          
          //delayMicroseconds(10);       // uncoment deley for diferent speed of display
          //delayMicroseconds(1000);
          //delay(10);
          //delay(100);
          
          digitalWrite(col[a], 1);      // reset whole column
        }
        digitalWrite(rows[i], LOW);     // reset whole row
        // otherwise last row will intersect with next row
    }
}

 void  drawScreen3(String matrix)
 { 
   // Turn on each row in series
    for (int i = 0; i < 8; i++)        // count next row
     {
        digitalWrite(rows[i], HIGH);    //initiate whole row
        for (int a = 0; a < 8; a++)    // count next row
        {
          // if You set (~buffer2[i] >> a) then You will have positive
          //digitalWrite(col[a], (~charToInt(matrix[a][i]))& 0x01); // initiate whole column
          //Serial.println(matrix)
          if (matrix[(8*a)+i]=='1'){
            digitalWrite(col[a], 0);  
          }
          if (matrix[(8*a)+i]=='0'){
            digitalWrite(col[a], 1);  
          }
          
          //delayMicroseconds(10);       // uncoment deley for diferent speed of display
          //delayMicroseconds(1000);
          //delay(10);
          //delay(100);
          
          digitalWrite(col[a], 1);      // reset whole column
        }
        digitalWrite(rows[i], LOW);     // reset whole row
        // otherwise last row will intersect with next row
    }
}

int charToInt(char c){
  int num = 0;

  //Substract '0' from entered char to get
  //corresponding digit
  num = c - '0';

  return num;
}

 void  drawDot(int r, int c, int s)
 { 
   // Turn on each row in series
    for (int i = 0; i < 8; i++)        // count next row
     {
        digitalWrite(rows[i], HIGH);    //initiate whole row
        for (int a = 0; a < 8; a++)    // count next row
        {
          // if You set (~buffer2[i] >> a) then You will have positive
          if(r==i and c==a and s ==1){
            digitalWrite(col[a], LOW); // initiate whole column
          }else{
            digitalWrite(col[a], HIGH);
          }
          delayMicroseconds(10);       // uncoment deley for diferent speed of display    
          digitalWrite(col[a], 1);      // reset whole column
        }
        digitalWrite(rows[i], LOW);     // reset whole row
        // otherwise last row will intersect with next row
    }
}

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
  
  
String hextobin(String msg, int i){
  String reslt = "";
  for(int j = 0; j<16; j++){
    for(int k = 0; k<16; k++){
      //Serial.print(h[k]);
      //Serial.print("-----");
      //Serial.print(msg[i+j]);
      if(h[k]==msg[i+j]){
        //Serial.println(" OK");
        reslt += b[k];
        break;
        }
      //Serial.println("");
      }
    }
    return reslt;
  }
// 
  /* this is siplest resemplation how for loop is working with each row.
    digitalWrite(COL_1, (~1);b >> 0) & 0x01); // Get the 1st bit: 10000000
    digitalWrite(COL_2, (~b >> 1) & 0x0 // Get the 2nd bit: 01000000
    digitalWrite(COL_3, (~b >> 2) & 0x01); // Get the 3rd bit: 00100000
    digitalWrite(COL_4, (~b >> 3) & 0x01); // Get the 4th bit: 00010000
    digitalWrite(COL_5, (~b >> 4) & 0x01); // Get the 5th bit: 00001000
    digitalWrite(COL_6, (~b >> 5) & 0x01); // Get the 6th bit: 00000100
    digitalWrite(COL_7, (~b >> 6) & 0x01); // Get the 7th bit: 00000010
    digitalWrite(COL_8, (~b >> 7) & 0x01); // Get the 8th bit: 00000001
}*/
