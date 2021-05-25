
#include<LiquidCrystal.h>
#include<Servo.h>
#include <SPI.h>
#include <Ethernet.h>
#include <PubSubClient.h>

// Update these with values suitable for your network.
byte mac[]    = {  0xDE, 0xED, 0xBA, 0xFE, 0xFE, 0xED };
IPAddress ip(192, 168, 1, 5);
IPAddress server(192,168,1,27);
EthernetClient ethClient;
PubSubClient client(ethClient);
LiquidCrystal lcd(2, 3, 4, 5, 6, 7);
Servo servo;
int pot = A1;
int sensor = A0; 
int bomba = A3;
String bombaModo = "auto";
bool bombaStatus = false;
bool bombaAtivada = false; 
unsigned long ultimaLeitura;
char hum[50];
unsigned long ultimoStatus;

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("arduinoClient")) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("outTopic","hello world");
      // ... and resubscribe
      client.subscribe("bomba/modo");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

int lerSensor(){
 int soma = 0; 
 for (int i = 0; i < 10; i++)
 {
  int tensao = analogRead(sensor);
  soma += tensao; 
 }
 Serial.print("soma ");
 Serial.println(soma);
 return constrain(soma, 3500, 10230); 
} 

void atualizarLcd(float humidade){
 lcd.clear();
 lcd.setCursor(0,0);
 lcd.print("humidade:");
 lcd.setCursor(0,1);
 lcd.print(humidade);
 lcd.print("%");
  
} 

void callback(char* topic, byte* payload, unsigned int length) {
  // handle message arrived
  Serial.println("mensagem");
  if(strcmp(topic, "bomba/modo")==0 ){
    bombaModo = String((char*)payload);
    Serial.println(String((char*)payload));
 }
}
void setup()
{
 client.setCallback(callback);
 ultimaLeitura = millis();
 ultimoStatus = millis();  
 lcd.begin (16, 2);
 servo.attach(9); 
 pinMode(pot,INPUT);
 pinMode(sensor,INPUT);
 pinMode(bomba, OUTPUT);
 Serial.begin(9600); 
 client.setServer(server, 1883);

  Ethernet.begin(mac, ip);
  delay(1500);
  
}


 
void loop()
{
  static int pct = 0; 
  if (!client.connected()) {
    reconnect();
  } else{
    if (millis()- ultimaLeitura > 2000){
      // leitura sensor valor 2500 a 10230 > mais seco
      
     int leituraSensor =  lerSensor();
     pct = map(leituraSensor, 3500, 10230, 100, 0);
     int angulo = map(pct ,0, 100, 0, 180);
     atualizarLcd(pct);
     servo.write(angulo);
     String humidade = String(pct);
     humidade.toCharArray(hum,humidade.length()+ 1);
     client.publish("humidade",hum, true);
     ultimaLeitura = millis();   
    }
    if (millis()- ultimoStatus > 500){
     if(bombaModo == "auto"){
      if(!bombaAtivada && pct < 45){
        bombaAtivada = true;
       
      }else if (bombaAtivada && pct > 65){
        bombaAtivada = false;
      }
      bombaStatus = bombaAtivada;
      
      
     }else if(bombaModo == "on"){
        bombaStatus = true; 
     }else{
        bombaStatus = false; 
     }
     digitalWrite(bomba, !bombaStatus);
     String statusStr = bombaStatus ? "on" : "off";
     char statusCh[5]; 
     statusStr.toCharArray(statusCh, statusStr.length()+ 1);
     client.publish("bomba/status", statusCh, true);
     ultimoStatus = millis();   
    }
    
    
   
  }
  client.loop();
 

}
      
