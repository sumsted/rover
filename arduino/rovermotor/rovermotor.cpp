#include <Arduino.h>
#include <Servo.h>
#include "SimpleTimer.h"

#define PWM_PIN_LF 3
#define PWM_PIN_RF 5
#define PWM_PIN_LR 6
#define PWM_PIN_RR 9

#define DIR_PIN_LF 2
#define DIR_PIN_RF 4
#define DIR_PIN_LR 7
#define DIR_PIN_RR 8

#define LED_PIN 13

#define MOTOR_ORIENTATION_LEFT 1
#define MOTOR_ORIENTATION_RIGHT 1

// should be duty range for cytron mdd10a
#define PWM_FULL_FORWARD 0
#define PWM_STOP 127
#define PWM_FULL_BACKWARD 255
#define PWM_TUNE_PERCENTAGE .5

#define SAFETY_CADENCE_MS 250  // millisecs

#define MAX_BUFFER_SIZE 50


SimpleTimer timer;

bool commandProcessed = false; // check used by safety timer to tell if command issued
byte ledVal = HIGH; // safety timer flips the led on and off


void safetyCheck() {
    if(!commandProcessed){
        analogWrite(PWM_PIN_LF, PWM_STOP);
        analogWrite(PWM_PIN_RF, PWM_STOP);
        analogWrite(PWM_PIN_LR, PWM_STOP);
        analogWrite(PWM_PIN_RR, PWM_STOP);
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
        analogWrite(PWM_PIN_LF, leftPulse);
        analogWrite(PWM_PIN_LR, leftPulse);

        analogWrite(PWM_PIN_RF, rightPulse);
        analogWrite(PWM_PIN_RR, rightPulse);
    } else {
        leftPulse = PWM_STOP + ((PWM_FULL_FORWARD - PWM_STOP) * (leftSpeed*PWM_TUNE_PERCENTAGE)/100 * MOTOR_ORIENTATION_LEFT);
        analogWrite(PWM_PIN_LF, leftPulse);
        analogWrite(PWM_PIN_LR, leftPulse);

        rightPulse = PWM_STOP + ((PWM_FULL_FORWARD - PWM_STOP) * (rightSpeed*PWM_TUNE_PERCENTAGE)/100 * MOTOR_ORIENTATION_RIGHT);
        analogWrite(PWM_PIN_RF, rightPulse);
        analogWrite(PWM_PIN_RR, rightPulse);

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

    // setting up for locked antiphase for cytron mdd10a
    // in this way it works like a frc pwm, one pwm signal
    // to control forward and reverse
    // the pwm from nano should be wired to dir pin on controller
    // and the dir pin should be wired to pwm on controller
    pinMode(DIR_PIN_LF, OUTPUT);
    pinMode(PWM_PIN_LF, OUTPUT);

    pinMode(DIR_PIN_LR, OUTPUT);
    pinMode(PWM_PIN_LR, OUTPUT);

    pinMode(DIR_PIN_RF, OUTPUT);
    pinMode(PWM_PIN_RF, OUTPUT);
    
    pinMode(DIR_PIN_RR, OUTPUT);
    pinMode(PWM_PIN_RR, OUTPUT);
}

void testPwm(){
    digitalWrite(DIR_PIN_LF, HIGH);
    digitalWrite(DIR_PIN_RF, HIGH);
    digitalWrite(DIR_PIN_LR, HIGH);
    digitalWrite(DIR_PIN_RR, HIGH);

    int pwm_value = 0;
    int opposite_i;
    int pulse;
    digitalWrite(DIR_PIN_LF, HIGH);
    for(pulse=0;pulse<=255;pulse++){
        analogWrite(PWM_PIN_LF, pulse);
        analogWrite(PWM_PIN_RF, pulse);
        analogWrite(PWM_PIN_LR, pulse);
        analogWrite(PWM_PIN_RR, pulse);
        delay(50);
        Serial.println(pulse);        
    }    
    for(pulse=255;pulse>=0;pulse--){
        analogWrite(PWM_PIN_LF, pulse);
        analogWrite(PWM_PIN_RF, pulse);
        analogWrite(PWM_PIN_LR, pulse);
        analogWrite(PWM_PIN_RR, pulse);
        delay(50);
        Serial.println(pulse);        
    }    
}

void loop() {
    // testPwm();
    digitalWrite(DIR_PIN_LF, HIGH);
    digitalWrite(DIR_PIN_RF, HIGH);
    digitalWrite(DIR_PIN_LR, HIGH);
    digitalWrite(DIR_PIN_RR, HIGH);

    serialHandler();
    timer.run();
}
