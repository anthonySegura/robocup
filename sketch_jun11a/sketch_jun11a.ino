#include <SoftwareSerial.h>
#include <RobotCustomLib.h>
SoftwareSerial hc06(0,1);

RobotCustomLib Robot;

int speed = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("Enter commands: ");
  hc06.begin(9600);
  
  Robot.begin();
  Robot.setSpeed(250);

}

void loop() {
  if (hc06.available()){
    char x = hc06.read(); 
    Serial.println((char)x);
    if ((char)x == 'F') {
      Robot.setSpeed(200);
      Robot.forward();
    }
    else if ((char)x == 'B') {
      Robot.setSpeed(200);
      Robot.backward();
    }
    else if ((char)x == 'L') {
      Robot.setSpeed(210);
      Robot.left(250);
    }
    else if ((char)x == 'R') {
      Robot.setSpeed(210);
      Robot.right(250);
    }
    else {
      Robot.stop();
    }
    
  }
}
