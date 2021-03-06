int ledPins[]={11,10,9,6,5,3};      // the pins that the LEDs are attached to
char nbuffer[3];
int received=0;
int brightness;
void setup()
{
  // initialize the serial communication:
  Serial.begin(115200);

  // initialize the ledPin as an output:
  for(int i=0;i<6;i++)
    pinMode(ledPins[i], OUTPUT);
  received = 0;
  nbuffer[received] = '\0';
}

void loop() {
  if (Serial.available()) {
       nbuffer[received]=Serial.read();
       received+=1;
  }
  if(received>2){
    brightness = atoi(nbuffer);
    //Serial.println(brightness);
    received=0;
  }
  for(int i=0;i<6;i++)
    analogWrite(ledPins[i], brightness);
}

