#include <Arduino.h>
#include <Servo.h>
#include "SimpleTimer.h"

#define MOTOR_PIN_LF 3
#define MOTOR_PIN_LR 5
#define MOTOR_PIN_RF 6
#define MOTOR_PIN_RR 9

#define LED_PIN 13

#define US_LEFT_PIN 3
#define US_LOW_PIN 5
#define US_FRONT_PIN 6
#define US_RIGHT_PIN 9
#define US_REAR_PIN 7
#define ENC_LEFT_FRONT 2

#define SAFETY_CADENCE_MS 500  // millisecs

#define MAX_BUFFER_SIZE 50


SimpleTimer timer;

bool commandProcessed = false; // check used by safety timer to tell if command issued
byte ledVal = HIGH; // safety timer flips the led on and off

int left_distance=0;
int low_distance=0;
int front_distance=0;
int right_distance=0;
int rear_distance=0;
int left_front_encoder=0;


void safetyCheck() {
    if(false){
    } else {
    }
    ledVal = (ledVal == HIGH)?LOW:HIGH;
    digitalWrite(LED_PIN, ledVal);
}


void doStep(byte step){
    // for debugging
    // Serial.println("step: "+String(step));
    // delay(1000);
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
        char result[100];
        sprintf(result,"{\"left\":%d,\"low\":%d,\"front\":%d,\"right\":%d,\"rear\":%d,\"encoder\":%d}",
                left_distance, low_distance, front_distance, right_distance, rear_distance, left_front_encoder);
        Serial.write(result);
    }
}

void encoderCb(){
    left_front_encoder++;
}

void readUltrasonic(){

}

void setup() {
    Serial.begin(9600);
    while(!Serial){}
    Serial.println("begin");
    timer.setInterval(SAFETY_CADENCE_MS, safetyCheck);
    pinMode(LED_PIN, OUTPUT);
    pinMode(US_LEFT_PIN, INPUT);
    pinMode(US_LOW_PIN, INPUT);
    pinMode(US_FRONT_PIN, INPUT);
    pinMode(US_RIGHT_PIN, INPUT);
    pinMode(US_REAR_PIN, INPUT);

    pinMode(ENC_LEFT_FRONT, INPUT);
    digitalWrite(ENC_LEFT_FRONT, HIGH);
    attachInterrupt(0, encoderCb, CHANGE);
}

void loop() {
    serialHandler();
    timer.run();
}
