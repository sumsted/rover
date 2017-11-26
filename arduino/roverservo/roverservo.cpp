#include <Arduino.h>
#include <Servo.h>
#include "SimpleTimer.h"

#define PWM_PIN_LF 9
#define PWM_PIN_RF 7

#define LED_PIN 13

#define MOTOR_ORIENTATION_LEFT_FRONT 1
#define MOTOR_ORIENTATION_RIGHT_FRONT 1

// should be duty range for cytron mdd10a
#define PWM_FULL_FORWARD 180
#define PWM_STOP 90
#define PWM_FULL_BACKWARD 0
#define PWM_TUNE_PERCENTAGE 1

#define SAFETY_CADENCE_MS 1000  // millisecs

#define MAX_BUFFER_SIZE 50

Servo leftServo;
Servo rightServo;

SimpleTimer timer;

bool commandProcessed = false; // check used by safety timer to tell if command issued
byte ledVal = HIGH; // safety timer flips the led on and off


void safetyCheck() {
    if(!commandProcessed){
        leftServo.write(PWM_STOP);
        rightServo.write(PWM_STOP);
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
    int leftFrontPulse = PWM_STOP;
    int rightFrontPulse = PWM_STOP;
    int leftRearPulse = PWM_STOP;
    int rightRearPulse = PWM_STOP;
    if(leftSpeed > 100 || leftSpeed < -100 || rightSpeed > 100 || rightSpeed < -100){
        leftServo.write(leftFrontPulse);
        rightServo.write(rightFrontPulse);
    } else {
        // ok
        leftFrontPulse = PWM_STOP + ( PWM_STOP * (leftSpeed*PWM_TUNE_PERCENTAGE)/100 * MOTOR_ORIENTATION_LEFT_FRONT);
        leftServo.write(leftFrontPulse);

        // ok
        rightFrontPulse = PWM_STOP + (PWM_STOP * (rightSpeed*PWM_TUNE_PERCENTAGE)/100 * MOTOR_ORIENTATION_RIGHT_FRONT);
        rightServo.write(rightFrontPulse);

        commandProcessed = true;
    }
    char result[100];
    sprintf(result, "{\"leftSpeed\":%d,\"rightSpeed\":%d,\"leftFrontPulse\":%d,\"rightFrontPulse\":%d,\"leftRearPulse\":%d,\"rightRearPulse\":%d}", 
            leftSpeed, rightSpeed, leftFrontPulse, rightFrontPulse, leftRearPulse, rightRearPulse);
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
        switch(command){
            case 'I':
                Serial.write("{\"id\":\"motor\"}");    
                break;
            default:
                char leftSpeedBuffer[5];
                memcpy(leftSpeedBuffer, readBuffer+1, 4);
                leftSpeedBuffer[4] = '\0';
                int leftSpeed = atoi(leftSpeedBuffer);

                char rightSpeedBuffer[5];
                memcpy(rightSpeedBuffer, readBuffer+5, 4);
                rightSpeedBuffer[4] = '\0';
                int rightSpeed = atoi(rightSpeedBuffer);
                Serial.write(runMotor(leftSpeed, rightSpeed));
        }

    }
}

void setup() {
    Serial.begin(9600);
    while(!Serial){}
    Serial.write("{\"id\":\"motor\"}");
    timer.setInterval(SAFETY_CADENCE_MS, safetyCheck);
    pinMode(LED_PIN, OUTPUT);

    leftServo.attach(PWM_PIN_LF);
    rightServo.attach(PWM_PIN_RF);
    leftServo.write(PWM_STOP);
    rightServo.write(PWM_STOP);
}

void testPwm(){
    int pwm_value = 0;
    int opposite_i;
    int pulse;
    for(pulse=0;pulse<=180;pulse++){
        leftServo.write(pulse);
        rightServo.write(pulse);
        delay(50);
        Serial.println(pulse);        
    }    
    for(pulse=180;pulse>=0;pulse--){
        leftServo.write(pulse);
        rightServo.write(pulse);
        delay(50);
        Serial.println(pulse);        
    }    
}

void loop() {
    // testPwm();
    serialHandler();
    timer.run();
}
