#include <Arduino.h>
#include <Servo.h>

#define LED_PIN 13

#define LEFT_FRONT_ENCODER 3
#define RIGHT_FRONT_ENCODER 2

#define MAX_BUFFER_SIZE 50

byte ledVal = HIGH; 

long leftFrontEncoder=0;
long leftLastMillis=0;
long leftLastRotations=0;

long rightFrontEncoder=0;
long rightLastMillis=0;
long rightLastRotations=0;

// Test code
#define LEFT_SERVO_PIN 9
#define RIGHT_SERVO_PIN 7
Servo leftServo;
Servo rightServo;
// #define LEFT_LED_PIN 11
// #define RIGHT_LED_PIN 12
// #define LEFT_US_TRIG_PIN 6
// #define LEFT_US_ECHO_PIN 4

// long counter = 0;

int pos = 0;

void doStep(byte step){
    // for debugging
    // Serial.println("step: "+String(step));
    // delay(1000);
}

void writeSensorData(){
    char result[100];
    sprintf(result,"{\"id\":\"encoder\",\"left\":%ld,\"right\":%ld}",
       leftFrontEncoder, rightFrontEncoder);
    Serial.println(result);
}

void writeId(){
    Serial.println("{\"id\":\"encoder\"}");
}

void serialHandler(){
    char readBuffer[MAX_BUFFER_SIZE] = "";
    String readString;
    doStep(1);

    while(Serial.available() > 0){
        doStep(2);
        readString = Serial.readStringUntil('!');
    }

    doStep(3);
    if(readString.length() > 0){
        doStep(4);
        readString.toCharArray(readBuffer, MAX_BUFFER_SIZE);

        char command = readBuffer[0];
        switch(command){
            case 'I':
                writeSensorData();
                break;
            case 'E':
                writeSensorData();
                break;
            default:
                writeId();
                break;
        }
    }
}

void leftEncoderCb(){
    leftFrontEncoder++;
}

void rightEncoderCb(){
    rightFrontEncoder++;
}

long writeRpm(char label, long ticks, long *prevMillis, long *prevRotations){
    long currentMillis = millis();
    long currentRotations = ticks/2;
    char buffer[200];
    float rotations = (float)currentRotations - (float)(*prevRotations);
    float minutes = (((float)currentMillis - (float)(*prevMillis))/1000.0/60.0);
    // float rpm = ((float)currentRotations - (float)lastRotations) / (((float)currentMillis - (float)lastMillis)/1000.0/60.0);
    float rpm = rotations / minutes;
    sprintf(buffer, " = (%ld - %ld) / (%ld - %ld)/1000.0/60.0\n", currentRotations, *prevRotations, currentMillis,*prevMillis);
    // sprintf(buffer, "%f = %f / %f", rpm, rotations, minutes);
    *prevMillis = currentMillis;
    *prevRotations = currentRotations;
    Serial.println(String(label)+": "+String(rpm)+buffer);
    return rpm;
}

void setup() {
    Serial.begin(9600);
    while(!Serial){}
    writeSensorData();
    pinMode(LED_PIN, OUTPUT);

    pinMode(LEFT_FRONT_ENCODER, INPUT);
    digitalWrite(LEFT_FRONT_ENCODER, HIGH);
    
    pinMode(RIGHT_FRONT_ENCODER, INPUT);
    digitalWrite(RIGHT_FRONT_ENCODER, HIGH);

    attachInterrupt(digitalPinToInterrupt(LEFT_FRONT_ENCODER), leftEncoderCb, RISING);
    attachInterrupt(digitalPinToInterrupt(RIGHT_FRONT_ENCODER), rightEncoderCb, RISING);

    // more test code
    leftServo.attach(LEFT_SERVO_PIN);
    rightServo.attach(RIGHT_SERVO_PIN);
    leftServo.write(110);
    rightServo.write(120);
    // pinMode(LEFT_US_TRIG_PIN, OUTPUT);
    // pinMode(LEFT_US_ECHO_PIN, INPUT);
    // pinMode(LEFT_LED_PIN, OUTPUT);
    // pinMode(RIGHT_LED_PIN, OUTPUT);
}



void loop() {
    serialHandler();
    ledVal = (ledVal==HIGH) ? LOW : HIGH;
    digitalWrite(LED_PIN, ledVal);
}

// test code using ultrasonic sensor and two servos
// int getDistance(int trigPin, int echoPin){
//     long duration = 0;

//     digitalWrite(trigPin, LOW);
//     delayMicroseconds(5);
//     digitalWrite(trigPin, HIGH);
//     delayMicroseconds(10);
//     digitalWrite(trigPin, LOW);

//     pinMode(echoPin, INPUT);
//     // duration = pulseIn(echoPin, HIGH, 8730);
//     duration = pulseIn(echoPin, HIGH);
//     // Serial.println("duration: "+String(duration));
//     delay(100);
//     if(duration < 0){
//         return 0;
//     } else if(duration >= 8730 || duration == 0){
//         return 150;
//     } else {
//         return (duration/2) / 29.1;
//     }
// }
// void testEncoders(){
//     if(leftDistance < 50){
//         leftServo.write(110);
//         rightServo.write(120);
//     } else {
//         leftServo.write(90);
//         rightServo.write(90);
//     }

//     ledVal = (ledVal==HIGH) ? LOW : HIGH;
//     digitalWrite(LED_PIN, ledVal);

//     counter++;
//     if(!(counter%100)){
//         writeRpm('L', leftFrontEncoder, &leftLastMillis, &leftLastRotations);
//         writeRpm('R', rightFrontEncoder, &rightLastMillis, &rightLastRotations);
//     }
//     Serial.println("L: "+String(leftFrontEncoder)+", "+String((float)leftFrontEncoder/2.0));
//     Serial.println("R: "+String(rightFrontEncoder)+", "+String((float)rightFrontEncoder/2.0));

//     int leftLight = (!((leftFrontEncoder) % 2)) ? HIGH : LOW;
//     digitalWrite(LEFT_LED_PIN, leftLight);

//     int rightLight = (!((rightFrontEncoder) % 2)) ? HIGH : LOW;
//     digitalWrite(RIGHT_LED_PIN, rightLight);

// }
