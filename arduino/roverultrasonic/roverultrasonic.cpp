#include <Arduino.h>
#include <Servo.h>

#define LED_PIN 13

#define US_FRONT_TRIG_PIN 11
#define US_FRONT_ECHO_PIN 12
#define US_LEFT_TRIG_PIN 3
#define US_LEFT_ECHO_PIN 4
#define US_LOW_TRIG_PIN 5
#define US_LOW_ECHO_PIN 6

#define US_REAR_TRIG_PIN 7
#define US_REAR_ECHO_PIN 8
#define US_RIGHT_TRIG_PIN 9
#define US_RIGHT_ECHO_PIN 10

#define ENC_LEFT_FRONT 2

#define MAX_BUFFER_SIZE 50


bool commandProcessed = false; // check used by safety timer to tell if command issued
byte ledVal = HIGH; // safety timer flips the led on and off

long left_distance=0;
long low_distance=0;
long front_distance=0;
long right_distance=0;
long rear_distance=0;
long left_front_encoder=0;

void doStep(byte step){
    // for debugging
    // Serial.println("step: "+String(step));
    // delay(1000);
}

void writeSensorData(){
    char result[100];
   sprintf(result,"{\"left\":%ld,\"low\":%ld,\"front\":%ld,\"right\":%ld,\"rear\":%ld}",
       left_distance, low_distance, front_distance, right_distance, rear_distance);
    Serial.println(result);
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
                Serial.write("{\"id\":\"encoder\"}");
                break;
            default:
                writeSensorData();
                break;
        }
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
    Serial.write("{\"id\":\"encoder\"}");
    pinMode(LED_PIN, OUTPUT);
    pinMode(US_FRONT_TRIG_PIN, OUTPUT);
    pinMode(US_FRONT_ECHO_PIN, INPUT);
    pinMode(US_LEFT_TRIG_PIN, OUTPUT);
    pinMode(US_LEFT_ECHO_PIN, INPUT);
    pinMode(US_LOW_TRIG_PIN, OUTPUT);
    pinMode(US_LOW_ECHO_PIN, INPUT);
    pinMode(US_RIGHT_TRIG_PIN, OUTPUT);
    pinMode(US_RIGHT_ECHO_PIN, INPUT);
    pinMode(US_REAR_TRIG_PIN, OUTPUT);
    pinMode(US_REAR_ECHO_PIN, INPUT);

//    pinMode(ENC_LEFT_FRONT, INPUT);
//    digitalWrite(ENC_LEFT_FRONT, HIGH);
//    attachInterrupt(0, encoderCb, CHANGE);
}

int getDistance(int trigPin, int echoPin){
    long duration = 0;

    digitalWrite(trigPin, LOW);
    delayMicroseconds(5);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    pinMode(echoPin, INPUT);
    duration = pulseIn(echoPin, HIGH);
    // duration = pulseIn(echoPin, HIGH,10000);
    // Serial.println("duration: "+String(duration));
    if(duration < 0){
        return 0;
    } else if(duration >= 10500){
        return 180;
    } else {
        return (duration/2) / 29.1;
    }
}


void loop() {
    serialHandler();
    front_distance = getDistance(US_FRONT_TRIG_PIN, US_FRONT_ECHO_PIN);
    low_distance = getDistance(US_LOW_TRIG_PIN, US_LOW_ECHO_PIN);
    left_distance = getDistance(US_LEFT_TRIG_PIN, US_LEFT_ECHO_PIN);
    right_distance = getDistance(US_RIGHT_TRIG_PIN, US_RIGHT_ECHO_PIN);
    rear_distance = getDistance(US_REAR_TRIG_PIN, US_REAR_ECHO_PIN);
    // writeSensorData();
    // delay(500);
}
