#include <SPI.h>
#include <Ethernet.h>
#include <EEPROM.h>

#define BUF_SIZE 8

// Global Variables 
byte mac[6] = { 0xFF, 0xFF, 0xFF, 0x00, 0x01, 0x02};
IPAddress ip(192, 168, 0, 140); //IP Address of device

int port = 1616;

EthernetServer server(port); //TCP Port for device
boolean alreadyConnected = false;

//status led
int status_led_pin = 13;
bool status_led_state = false;



void setup() {
  //intialize output pins
  for (int i = 2; i <= 9; i++) { 
		pinMode(i, OUTPUT);
  }
  pinMode(status_led_pin, OUTPUT);

  //initialized Ethernet Shield
  Ethernet.init(10); 
  Ethernet.begin(mac, ip); 
  
  //If the Shield is missing, blink LED forever
  if (Ethernet.hardwareStatus() == EthernetNoHardware) {
    while (true) {
      digitalWrite(status_led_pin, HIGH);
      delay(100);
      digitalWrite(status_led_pin, LOW);
      delay(100);
    }
  }

  //if Ethernet Cable is disconnected, light LED until it's not (not sure this works) 
	if (Ethernet.linkStatus() == LinkOFF){
	  digitalWrite(status_led_pin, HIGH);
	} else digitalWrite(status_led_pin, LOW);

  //start TCP Server
  server.begin(); 
}

void loop() {
    String request = "";                        //recieved TCP messages (might be unneeded) 
    EthernetClient client = server.available(); //TCP Client

    // If the client is already connected, don't reconnect. 
    if (client) {
        if (!alreadyConnected) {
            client.flush();
            alreadyConnected = true;
        }
        String request = readRequest(&client); //listen and read TCP messages
        executeRequest(&client, &request);     //execute commands
    }
}

// Listens to TCP port and formats incoming messages (all messages must end with a New Line Character)
String readRequest(EthernetClient* client){
	String request = "";
    while (client->available()){
        char c = client->read();
        if ('\n' == c){
            return request;
        }
        request += c;
    }
	return request;
}

// Executes requests based on the incoming messages
void executeRequest(EthernetClient* client, String* request){
    char command = parseUserCommand(request);
    // 'w*******': Writes the output pins of device 
    // 'r': Polls the state of pins 2-9 and outputs values as a String formated Binary Value
    if('w' == command) {
      String writeVals = request->substring(1,9);
      Serial.println(writeVals);
    	for(int i = 0; i < BUF_SIZE; i++) {
        int pinState = writeVals.charAt(i);
        int pinNum = (BUF_SIZE-i)+1;
        if(pinState == '1'){
          digitalWrite(pinNum, HIGH);
        } else if(pinState == '0'){
          digitalWrite(pinNum, LOW);
        } 
      }
      sendResponse(client, "k");
    } else if('r' == command) {
        String pinState;
        for (int i = 9; i >= 2; i--)
            pinState += digitalRead(i);
        sendResponse(client, pinState);
    }
}

// Seperates the command from the incoming message
char parseUserCommand(String* request){
	String commandString = request->substring(0, 1);
	return commandString.charAt(0);
}

// Sends a TCP response
void sendResponse(EthernetClient* client, String response){
	client->println(response);
}
