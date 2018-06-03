#include <DRV8825.h>
#include <HX711.h>

HX711 scale;

#define CAL_VAL 385     // Set the calibration value
#define DOUT A1         // DOUT -> pin A1 on arduino
#define SCK A0          // SCK  -> pin A0 on arduino

#define STEP_SIZE 0.004f// Set the step size in milimeter
#define MOTOR_STEPS 200 // Specify how many steps there are
                        // in one rotation

// The following variables relate the pins from the arduino
// to the pins on the DRV8825.
#define DIR 9
#define STEP 8
#define M0 3
#define M1 4
#define M2 5
#define ROT_SPEED 500   // Rotation speed of the motor
#define ENABLE -1       // We will not be using the enable
                        // pin on the DRV8825

DRV8825 stepper(MOTOR_STEPS, DIR, STEP, ENABLE, M0, M1, M2);

int count = 0;          // This value will count how many
// times the loop has ran

boolean run = false;
int steps_per_turn = 1;
float distance = 0;

void PrintWeight () {
  distance = count * STEP_SIZE * steps_per_turn;
  
  Serial.print(count);
  Serial.print(",");
  Serial.print(distance);
  Serial.print(",");

  // Take a measurement of the scale
  Serial.println(scale.get_units(5), 4);
}

void setup() {
  Serial.begin(38400);

  Serial.println("Beginning HX711 setup");
  Serial.println("\tSetting up pins");
  scale.begin(DOUT, SCK);

  Serial.println("\tSetting calibration value");
  scale.set_scale(CAL_VAL); // Calibrate the scale

  Serial.println("\tTaring");
  scale.tare();

  Serial.println("HX711 setup succesful");

  Serial.println("Beginning DRV8825 setup");
  Serial.println("\tStarting motors");
  stepper.begin(ROT_SPEED, 1);
}


// The serial input will determine when the program
// will be run. By sending the letter 'g', (without
// quoutes) the code will start running. To stop the
// code simply send 's'.
int dir = 1;
void loop() {
  if (Serial.available() > 0) {
    char inChar = Serial.read();
    Serial.print("Got: ");
    Serial.println(inChar);
    switch (inChar) {
      case 'g': // Go
        run = true;
        count = 0;
        scale.tare();
        Serial.println("---------------------");
        Serial.println("count,distance,weight");
        break;
      case 's': // Stop
        run = false;
        break;
      case '1':
        steps_per_turn = 1;
        break;
      case '2':
        steps_per_turn = 5;
          break;
      case '3':
        steps_per_turn = 10;
        break;
      case '4':
        steps_per_turn = 50;
        break;
      case '5':
        steps_per_turn = 100;
        break;
      case '6':
        steps_per_turn = 500;
        break;
      case '7':
        steps_per_turn = 1000;
        break;
      case '8':
        steps_per_turn = 5000;
        break;
      case '9':
        steps_per_turn = 10000;
        break;
      case 'd':
        stepper.move(steps_per_turn*dir);
        break;
      case 'r':
        dir = -dir;
        break;
      case 't':
        scale.tare();
        break;
      case 'o':
        stepper.rotate(180);
    }
  }
  if (run) {
    // Turn the stepper motor
    stepper.move(steps_per_turn*dir);

    PrintWeight();

    count++;
  }
}
