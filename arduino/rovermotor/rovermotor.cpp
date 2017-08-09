#include <Arduino.h>
#include <Servo.h>
#include "SimpleTimer.h"

#define MOTOR_PIN_LF 3
#define MOTOR_PIN_LR 5
#define MOTOR_PIN_RF 6
#define MOTOR_PIN_RR 9

#define LED_PIN 13

#define MOTOR_ORIENTATION_LEFT 1
#define MOTOR_ORIENTATION_RIGHT -1

#define PWM_FULL_FORWARD 2000
#define PWM_STOP 1500
#define PWM_FULL_BACKWARD 1000
#define PWM_TUNE_PERCENTAGE .5

#define SAFETY_CADENCE_MS 500  // millisecs

#define MAX_BUFFER_SIZE 50

Servo motorLeftFront;
Servo motorLeftRear;
Servo motorRightFront;
Servo motorRightRear;

SimpleTimer timer;

bool commandProcessed = false; // check used by safety timer to tell if command issued
byte ledVal = HIGH; // safety timer flips the led on and off


void safetyCheck() {
    if(!commandProcessed){
        motorLeftFront.write(PWM_STOP);
        motorLeftRear.write(PWM_STOP);
        motorRightFront.write(PWM_STOP);
        motorRightRear.write(PWM_STOP);
    } else {
    }
    commandProcessed = false;
    ledVal = (ledVal == HIGH)?LOW:HIGH;
    digitalWrite(LED_PIN, ledVal);
}

void doStep(byte step){
    // for debugging
    // Serial.println("step: "+String(step));
    // delay(1000);
}


// TODO eventually add each individual motor, once we have encoders on all wheels and
// are able to offer corrections
char *runMotor(int leftSpeed, int rightSpeed){
    int rightPulse = PWM_STOP;
    int leftPulse = PWM_STOP;
    if(leftSpeed > 100 || leftSpeed < -100 || rightSpeed > 100 || rightSpeed < -100){
        motorLeftFront.write(leftPulse);
        motorLeftRear.write(leftPulse);

        motorRightFront.write(rightPulse);
        motorRightRear.write(rightPulse);
    } else {
        leftPulse = PWM_STOP + ((PWM_FULL_FORWARD - PWM_STOP) * (leftSpeed*PWM_TUNE_PERCENTAGE)/100 * MOTOR_ORIENTATION_LEFT);
        motorLeftFront.write(leftPulse);
        motorLeftRear.write(leftPulse);

        rightPulse = PWM_STOP + ((PWM_FULL_FORWARD - PWM_STOP) * (rightSpeed*PWM_TUNE_PERCENTAGE)/100 * MOTOR_ORIENTATION_RIGHT);
        motorRightFront.write(rightPulse);
        motorRightRear.write(rightPulse);

        commandProcessed = true;
    }
    char result[100];
    sprintf(result, "{\"leftPulse\":%d,\"rightPulse\":%d}", leftPulse, rightPulse);
    return result;
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

        char leftSpeedBuffer[5];
        memcpy(leftSpeedBuffer, readBuffer+1, 4);
        leftSpeedBuffer[4] = '\0';
        int leftSpeed = atoi(leftSpeedBuffer);

        char rightSpeedBuffer[5];
        memcpy(rightSpeedBuffer, readBuffer+5, 4);
        rightSpeedBuffer[4] = '\0';
        int rightSpeed = atoi(rightSpeedBuffer);
        // Serial.println("command: "+String(command)+", left: "+String(leftSpeed)+", right: "+String(rightSpeed));

        Serial.write(runMotor(leftSpeed, rightSpeed));
    }
}

void setup() {
    Serial.begin(9600);
    while(!Serial){}
    Serial.println("begin");
    timer.setInterval(SAFETY_CADENCE_MS, safetyCheck);
    pinMode(LED_PIN, OUTPUT);
    motorLeftFront.attach(MOTOR_PIN_LF);
    motorLeftRear.attach(MOTOR_PIN_LR);
    motorRightFront.attach(MOTOR_PIN_RF);
    motorRightRear.attach(MOTOR_PIN_RR);
}

void loop() {
    serialHandler();
    timer.run();
}
