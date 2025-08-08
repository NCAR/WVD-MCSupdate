// Written By: Kina Smith
// Modified by: Robert Stillwell
// This is the source code that is compiled and run on the MPD switch for MPD. 

#include <SPI.h>
#include <Ethernet.h>
#include <EEPROM.h>
#define BUF_SIZE 8

// Global Variables 
const int ServerNum = 3;
unsigned int Count = 0;

// Ethernet settings for the Arduino device
byte mac[6] = { 0xBA, 0xBE, 0x00, 0x01, 0x02, 0x03}; // Mac address of device
IPAddress ip(192, 168, 0, 140);                      // IP Address of device 

// Defining the TCP connections
int            Ports[ServerNum]     = {1616, 1617, 1618};
EthernetServer Servers[ServerNum]   = {EthernetServer(Ports[0]), EthernetServer(Ports[1]), EthernetServer(Ports[2])};
boolean        Connected[ServerNum] = {false,false,false};

// Global Variables 
int status_led_pin = 13;

// This function is called at started before the loop() function is called continuously 
void setup() {
  // Generating MAC Address string
  char macstr[18];
  snprintf(macstr, 18, "%02x:%02x:%02x:%02x:%02x:%02x", mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);

  // Intialize output pins
  for (int i = 2; i <= 9; i++) { 
		pinMode(i, OUTPUT);
	}
  pinMode(status_led_pin, OUTPUT);
  
  // Initialized Ethernet Shield
  Ethernet.init(10); 
  Ethernet.begin(mac, ip); 
  // Start serial port communications for debugging (if desired)
  Serial.begin(9600); 

  // If the Shield is missing, blink LED forever
  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
    while (true) {
      digitalWrite(status_led_pin, !digitalRead(status_led_pin));
      delay(100);
    }
  }
  // If Ethernet Cable is disconnected, light LED until it's not (not sure this)
	if (Ethernet.linkStatus() == LinkOFF){
		digitalWrite(status_led_pin, HIGH);
	} else digitalWrite(status_led_pin, LOW);

  // Starting the TCP servers
  Serial.print("IP address: ");
	Serial.print(Ethernet.localIP());
  for (int i = 0; i < ServerNum; i++){
    Servers[i].begin();
    Serial.print(", Port "); Serial.print(i + 1);  Serial.print(": ");
    Serial.print(Ports[i]);
  }
  //debug print IP Address, Port, and MAC
  Serial.print(", Mac Address: ");	
	Serial.println(macstr);
}

// This function is called continuously right after startup
void loop() {
    // Determining which port to check this time through the loop 
    int CurrentServerNum = Count % ServerNum;
    // Checking to see if a TCP connection has been requested
    EthernetClient clientSwitch = Servers[CurrentServerNum].available(); //TCP Client
    if (clientSwitch) {
      Connected[CurrentServerNum] = respondToTCPConnection(&clientSwitch, Connected[CurrentServerNum]);
    }
    //Wait to make sure the loop doesn't race
    delay(1);
    //Updating the counter
    Count += 1;
}

// Used to check a generic TCP  connection and respond
boolean respondToTCPConnection(EthernetClient* client, boolean alreadyConnected){
  long int t1 = millis();
  // Checking if the connection has ever been established
  if (!alreadyConnected) {
    client->flush();
    Serial.println("client connected");
    alreadyConnected = true;
  }
  // Reading and executing the TCP request
  Serial.print("------Reading-----: ");
  String request = readRequest(client); //listen and read TCP messages
  Serial.println(request);              //prints recieved characters
  Serial.print("---Executinging---: ");
  executeRequest(client, &request); //execute commands
  long int t2 = millis();
  Serial.print("Communication time: ");
  Serial.print(t2-t1); 
  Serial.println(" milliseconds");
  // Returning if the connection has been made
  return alreadyConnected;
}

//Executes requests based on the incoming messages
void executeRequest(EthernetClient* client, String* request){
  // Check what type of user command is requested
  char command = parseUserCommand(request);
  // 'w********': Writes the output pins of device, 
  // 'l********': Does the same but only allows writting to pin 7/8/9
  if('l' == command || 'w' == command) {
    String writeVals = request->substring(1,9);
    for(int i = 0; i < BUF_SIZE; i++) {
      int pinState = writeVals.charAt(i);
      int pinNum = (BUF_SIZE-i)+1;
      if (pinNum > 6 || 'w' == command){
        setDigital(pinState, pinNum);
      }
    }
    sendResponse(client, "k");
  }
  // 'h*': Sets pin 6 of the device (intended to be wired to the hygrostat)
  else if('h' == command) {
    String writeVals = request->substring(1,2);
    int pinState = writeVals.charAt(0);
    int pinNum = 6;
    setDigital(pinState, pinNum);
    sendResponse(client, "k");
  }
  // 'r': Polls the state of pins 2-9 and outputs those values as a String formated Binary Value
  else if('r' == command) {
    String pinState;
    for (int i = 9; i >= 2; i--){
      pinState += digitalRead(i);
    }
    sendResponse(client, pinState);
  } else{
    Serial.println("Comamnd not recognized");
  }
}

//
void setDigital(int pinState, int pinNum){
  if(pinState == '1'){
    digitalWrite(pinNum, HIGH);
  } else if(pinState == '0'){ 
    digitalWrite(pinNum, LOW);
  }
}

// Listens to TCP port and formats incoming messages (all messages must end with a New Line Character)
String readRequest(EthernetClient* client){
	String request = "";    // Defining a string to hold the request
  while (client->available()){
    char c = client->read();
    if ('\n' == c){
      return request;
    }
    request += c;
  }
	return request;
}

//Seperates the command from the incoming message
char parseUserCommand(String* request){
	String commandString = request->substring(0, 1);
	return commandString.charAt(0);
}

//sends a TCP response
void sendResponse(EthernetClient* client, String response){
	client->println(response);
  // Printing to the serial port if desired for debugging
	Serial.print("sendResponse: ");
	Serial.println(response);
}

