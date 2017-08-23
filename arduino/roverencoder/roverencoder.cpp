#include <Arduino.h>
#include <Servo.h>

#define LED_PIN 13

#define US_LEFT_TRIG_PIN 3
#define US_LEFT_ECHO_PIN 4

#define ENC_LEFT_FRONT 2

#define SERVO_PIN 9

#define MAX_BUFFER_SIZE 50

byte ledVal = HIGH; // safety timer flips the led on and off

long left_distance=0;

long left_front_encoder=0;

Servo theServo;
int pos = 0;

void doStep(byte step){
    // for debugging
    // Serial.println("step: "+String(step));
    // delay(1000);
}

void writeSensorData(){
    char result[100];
    sprintf(result,"{\"left\":%ld}",
       left_distance);
    Serial.println(result);
}

void writeId(){
    Serial.println("{\"id\":\"ultrasonic\"}");
}

void moveServo(int posIn){
    theServo.write(posIn);
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
                writeId();
                break;
            case 'U':
                writeSensorData();
                break;
            case 'M':
                char pulseBuffer[5];
                int posIn;
                memcpy(pulseBuffer, readBuffer+1, 4);
                pulseBuffer['\0'];
                posIn = atoi(pulseBuffer);
                moveServo(posIn);
            default:
                writeId();
                break;
        }
    }
}

void encoderCb(){
    left_front_encoder++;
}

int getDistance(int trigPin, int echoPin){
    long duration = 0;

    digitalWrite(trigPin, LOW);
    delayMicroseconds(5);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    pinMode(echoPin, INPUT);
    duration = pulseIn(echoPin, HIGH, 8730);
    // Serial.println("duration: "+String(duration));
    if(duration < 0){
        return 0;
    } else if(duration >= 8730 || duration == 0){
        return 150;
    } else {
        return (duration/2) / 29.1;
    }
}

void setup() {
    Serial.begin(9600);
    while(!Serial){}
    writeId();
    pinMode(LED_PIN, OUTPUT);
    pinMode(US_LEFT_TRIG_PIN, OUTPUT);
    pinMode(US_LEFT_ECHO_PIN, INPUT);

    theServo.attach(SERVO_PIN);
//    pinMode(ENC_LEFT_FRONT, INPUT);
//    digitalWrite(ENC_LEFT_FRONT, HIGH);
//    attachInterrupt(0, encoderCb, CHANGE);
}

void loop() {
    serialHandler();
    left_distance = getDistance(US_LEFT_TRIG_PIN, US_LEFT_ECHO_PIN);

    if(left_distance < 50){
        moveServo(100);
    } else {
        moveServo(90);
    }

    delay(100);
    ledVal = (ledVal==HIGH) ? LOW : HIGH;
    digitalWrite(LED_PIN, ledVal);

    // writeSensorData();
    // delay(200);

    // for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
    //     // in steps of 1 degree
    //     theServo.write(pos);              // tell servo to go to position in variable 'pos'
    //     delay(15);                       // waits 15ms for the servo to reach the position
    // }
    // for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    //     theServo.write(pos);              // tell servo to go to position in variable 'pos'
    //     delay(15);                       // waits 15ms for the servo to reach the position
    // }
}
