#define R_EN_R 2
#define L_EN_R 3
#define RPWM_R 4
#define LPWM_R 5

#define R_EN_L 8
#define L_EN_L 9
#define RPWM_L 10
#define LPWM_L 11


int command = 0;
int speed = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  //Motor1
  pinMode (R_EN_R, OUTPUT);
  pinMode (L_EN_R, OUTPUT);
  pinMode (RPWM_R, OUTPUT);
  pinMode (LPWM_R, OUTPUT);
  //Motor2
  pinMode (R_EN_L, OUTPUT);
  pinMode (L_EN_L, OUTPUT);
  pinMode (RPWM_L, OUTPUT);
  pinMode (LPWM_L, OUTPUT);
}

void loop() {
  if (Serial.available() > 0){

    String toParse = Serial.readStringUntil("\n");
    toParse.trim();

    int colonIndex = toParse.indexOf(":");
    if (colonIndex != -1) {
      command = toParse.substring(0, colonIndex).toInt();
      speed = toParse.substring(colonIndex+1).toInt();

      Serial.print("Command: ");
      Serial.print(command);
      Serial.print("|");
      Serial.print("Speed: ");
      Serial.println(speed);
    }

    if (command == 1){ //Forward
      digitalWrite (R_EN_R, HIGH);
      digitalWrite (L_EN_R, HIGH);
      analogWrite (RPWM_R, speed); //speed 0-255
      analogWrite (LPWM_R, 0); //speed 0-255

      digitalWrite (R_EN_L, HIGH);
      digitalWrite (L_EN_L, HIGH);
      analogWrite (RPWM_L, speed); //speed 0-255
      analogWrite (LPWM_L, 0); //speed 0-255

    } else if (command == 2){ //Right
      digitalWrite (R_EN_R, HIGH);
      digitalWrite (L_EN_R, HIGH);
      analogWrite (RPWM_R, speed); //speed 0-255
      analogWrite (LPWM_R, 0); //speed 0-255

      digitalWrite (R_EN_L, HIGH);
      digitalWrite (L_EN_L, HIGH);
      analogWrite (RPWM_L, 0); //speed 0-255
      analogWrite (LPWM_L, speed); //speed 0-255

    } else if (command == 3){ //Left
      digitalWrite (R_EN_R, HIGH);
      digitalWrite (L_EN_R, HIGH);
      analogWrite (RPWM_R, 0); //speed 0-255
      analogWrite (LPWM_R, speed); //speed 0-255

      digitalWrite (R_EN_L, HIGH);
      digitalWrite (L_EN_L, HIGH);
      analogWrite (RPWM_L, speed); //speed 0-255
      analogWrite (LPWM_L, 0); //speed 0-255

    } else if (command == 4){ //Backward
      digitalWrite (R_EN_R, HIGH);
      digitalWrite (L_EN_R, HIGH);
      analogWrite (RPWM_R, 0); //speed 0-255
      analogWrite (LPWM_R, speed); //speed 0-255

      digitalWrite (R_EN_L, HIGH);
      digitalWrite (L_EN_L, HIGH);
      analogWrite (RPWM_L, 0); //speed 0-255
      analogWrite (LPWM_L, speed); //speed 0-255

    } else {
      digitalWrite (R_EN_R, HIGH);
      digitalWrite (L_EN_R, HIGH);
      analogWrite (RPWM_R, 0); //speed 0-255
      analogWrite (LPWM_R, 0); //speed 0-255

      digitalWrite (R_EN_L, HIGH);
      digitalWrite (L_EN_L, HIGH);
      analogWrite (RPWM_L, 0); //speed 0-255
      analogWrite (LPWM_L, 0); //speed 0-255
    }
    
    delay(1000);
    Serial.print("Reset");

    digitalWrite (R_EN_R, HIGH);
    digitalWrite (L_EN_R, HIGH);
    analogWrite (RPWM_R, 0); //speed 0-255
    analogWrite (LPWM_R, 0); //speed 0-255

    digitalWrite (R_EN_L, HIGH);
    digitalWrite (L_EN_L, HIGH);
    analogWrite (RPWM_L, 0); //speed 0-255
    analogWrite (LPWM_L, 0); //speed 0-255
  } 
}