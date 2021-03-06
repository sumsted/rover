#include <Arduino.h>
#include <Servo.h>
#include "SimpleTimer.h"

#define DIR_PIN_RF 6
#define PWM_PIN_RF 7
#define DIR_PIN_LF 3
#define PWM_PIN_LF 4
#define LED_PIN 13

#define MOTOR_ORIENTATION_LEFT -1
#define MOTOR_ORIENTATION_RIGHT 1

// should be duty range for cytron mdd10a
#define PWM_FULL_FORWARD 0
#define PWM_STOP 127
#define PWM_FULL_BACKWARD 255
#define PWM_DELTA 127
#define PWM_TUNE_PERCENTAGE .75  // use to limit duty signal .5 = 50%

#define SAFETY_CADENCE_MS 1000  // millisecs
#define MAX_BUFFER_SIZE 50

SimpleTimer timer;
bool commandProcessed = false; // check used by safety timer to tell if command issued
byte ledVal = HIGH; // safety timer flips the led on and off

int lastLeftPulse = PWM_STOP;
int lastRightPulse = PWM_STOP;

void safetyCheck() {
    if(!commandProcessed){
        analogWrite(DIR_PIN_LF, PWM_STOP);
        analogWrite(DIR_PIN_RF, PWM_STOP);
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

void writeData(){

}

void motionControl(int motorPin, int initialPulse, int targetPulse){
    int currentPulse = initialPulse;
    analogWrite(motorPin, targetPulse);
    // while(currentPulse != targetPulse){
    //     analogWrite(motorPin, currentPulse);
    //     currentPulse = currentPulse + (currentPulse < targetPulse ? 1 : -1);
    //     // delay(1);
    // }
}

// TODO eventually add each individual motor, once we have encoders on all wheels and
// are able to offer corrections
char *runMotor(int leftSpeed, int rightSpeed){
    int leftPulse = PWM_STOP;
    int rightPulse = PWM_STOP;

    if(leftSpeed > 100 || leftSpeed < -100 || rightSpeed > 100 || rightSpeed < -100){
        motionControl(DIR_PIN_LF, lastLeftPulse, leftPulse);
        motionControl(DIR_PIN_RF, lastRightPulse, rightPulse);
    } else {
        // ok
        leftPulse = PWM_STOP + ( PWM_DELTA * (leftSpeed * PWM_TUNE_PERCENTAGE)/100 * MOTOR_ORIENTATION_LEFT);
        motionControl(DIR_PIN_LF, lastLeftPulse, leftPulse);
        
        // ok
        rightPulse = PWM_STOP + (PWM_DELTA * (rightSpeed * PWM_TUNE_PERCENTAGE)/100 * MOTOR_ORIENTATION_RIGHT);
        motionControl(DIR_PIN_RF, lastRightPulse, rightPulse);
        commandProcessed = true;
    }

    lastLeftPulse = leftPulse;
    lastRightPulse = rightPulse;

    char result[100];
    sprintf(result, "{\"leftSpeed\":%d,\"rightSpeed\":%d,\"leftPulse\":%d,\"rightPulse\":%d}", 
            leftSpeed, rightSpeed, leftPulse, rightPulse);
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
    // timer.setInterval(SAFETY_CADENCE_MS, safetyCheck);
    pinMode(LED_PIN, OUTPUT);

    // setting up for locked antiphase for cytron mdd10a
    // in this way it works like a frc pwm, one pwm signal
    // to control forward and reverse
    // the pulse is sent along the DIR channels while the PWM channel is always high
    pinMode(DIR_PIN_LF, OUTPUT);
    pinMode(PWM_PIN_LF, OUTPUT);
    pinMode(DIR_PIN_RF, OUTPUT);
    pinMode(PWM_PIN_RF, OUTPUT);

    digitalWrite(PWM_PIN_LF, HIGH);
    digitalWrite(PWM_PIN_RF, HIGH);
    analogWrite(DIR_PIN_LF, PWM_STOP);
    analogWrite(DIR_PIN_RF, PWM_STOP);
}

void testPwm(){
    int pwm_value = 0;
    int opposite_i;
    int pulse;
    digitalWrite(PWM_PIN_LF, HIGH);
    digitalWrite(PWM_PIN_RF, HIGH);
    for(pulse=0;pulse<=255;pulse++){
        analogWrite(DIR_PIN_LF, pulse);
        analogWrite(DIR_PIN_RF, pulse);
        delay(50);
        Serial.println(pulse);        
    }    
    for(pulse=255;pulse>=0;pulse--){
        analogWrite(DIR_PIN_LF, pulse);
        analogWrite(DIR_PIN_RF, pulse);
        delay(50);
        Serial.println(pulse);        
    }    
}

void loop() {
    // testPwm();
    digitalWrite(PWM_PIN_LF, HIGH);
    digitalWrite(PWM_PIN_RF, HIGH);

    serialHandler();
    // timer.run();
}
