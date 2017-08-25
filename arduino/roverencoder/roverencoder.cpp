#include <Arduino.h>
#include <Servo.h>

#define LED_PIN 13
#define LEFT_LED_PIN 11
#define RIGHT_LED_PIN 12

#define US_LEFT_TRIG_PIN 3
#define US_LEFT_ECHO_PIN 4

#define ENC_LEFT_FRONT 2
#define ENC_RIGHT_FRONT 6

#define LEFT_SERVO_PIN 9
#define RIGHT_SERVO_PIN 7

#define MAX_BUFFER_SIZE 50

byte ledVal = HIGH; // safety timer flips the led on and off

long leftDistance=0;
long leftFrontEncoder=0;

long rightDistance=0;
long rightFrontEncoder=0;

Servo leftServo;
Servo rightServo;

int pos = 0;

void doStep(byte step){
    // for debugging
    // Serial.println("step: "+String(step));
    // delay(1000);
}

void writeSensorData(){
    char result[100];
    sprintf(result,"{\"left\":%ld,\"rightt\":%ld}",
       leftDistance, rightDistance);
    Serial.println(result);
}

void writeId(){
    Serial.println("{\"id\":\"ultrasonic\"}");
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
                leftServo.write(posIn);
            default:
                writeId();
                break;
        }
    }
}

void encoderCb(){
    leftFrontEncoder++;
    rightFrontEncoder++;
}

int getDistance(int trigPin, int echoPin){
    long duration = 0;

    digitalWrite(trigPin, LOW);
    delayMicroseconds(5);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);

    pinMode(echoPin, INPUT);
    // duration = pulseIn(echoPin, HIGH, 8730);
    duration = pulseIn(echoPin, HIGH);
    // Serial.println("duration: "+String(duration));
    delay(100);
    if(duration < 0){
        return 0;
    } else if(duration >= 8730 || duration == 0){
        return 150;
    } else {
        return (duration/2) / 29.1;
    }
}

long writeRpm(long ticks, long *prevMillis, long *prevRotations){
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
    Serial.println(String(rpm)+buffer);
    return rpm;
}

void setup() {
    Serial.begin(9600);
    while(!Serial){}
    writeId();
    pinMode(LED_PIN, OUTPUT);

    
    pinMode(US_LEFT_TRIG_PIN, OUTPUT);
    pinMode(US_LEFT_ECHO_PIN, INPUT);

    leftServo.attach(LEFT_SERVO_PIN);
    pinMode(LEFT_LED_PIN, OUTPUT);
    pinMode(ENC_LEFT_FRONT, INPUT);
    digitalWrite(ENC_LEFT_FRONT, HIGH);
    
    rightServo.attach(RIGHT_SERVO_PIN);
    pinMode(RIGHT_LED_PIN, OUTPUT);
    pinMode(ENC_RIGHT_FRONT, INPUT);
    digitalWrite(ENC_RIGHT_FRONT, HIGH);

    attachInterrupt(0, encoderCb, RISING);
}

long counter = 0;
long leftLastMillis=0;
long leftLastRotations=0;

void loop() {
    serialHandler();
    leftDistance = getDistance(US_LEFT_TRIG_PIN, US_LEFT_ECHO_PIN);

    if(leftDistance < 50){
        // float ratio = (50.0 - (float)leftDistance) / 50.0;
        // int pos = ratio * 40 + 110;
        // moveServo(pos);
        leftServo.write(90);
        rightServo.write(120);
    } else {
        leftServo.write(90);
        rightServo.write(90);
    }

    ledVal = (ledVal==HIGH) ? LOW : HIGH;
    digitalWrite(LED_PIN, ledVal);

    counter++;
    // if(!(counter%20)){
    //     writeRpm(leftFrontEncoder, leftLastMillis, leftLastRotations);
    //     writeRpm(rightFrontEncoder, rightLastMillis, rightLastRotations);
    // }
    Serial.println("L: "+String(leftFrontEncoder)+", "+String((float)leftFrontEncoder/2.0));
    Serial.println("R: "+String(rightFrontEncoder)+", "+String((float)rightFrontEncoder/2.0));

    int leftLight = (!((leftFrontEncoder) % 2)) ? HIGH : LOW;
    digitalWrite(LEFT_LED_PIN, leftLight);

    int rightLight = (!((rightFrontEncoder) % 2)) ? HIGH : LOW;
    digitalWrite(RIGHT_LED_PIN, rightLight);
    // writeSensorData();
    // delay(200);

    // for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
    //     // in steps of 1 degree
    //     leftServo.write(pos);              // tell servo to go to position in variable 'pos'
    //     delay(15);                       // waits 15ms for the servo to reach the position
    // }
    // for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
    //     leftServo.write(pos);              // tell servo to go to position in variable 'pos'
    //     delay(15);                       // waits 15ms for the servo to reach the position
    // }
}
