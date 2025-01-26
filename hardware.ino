#include <PubSubClient.h>
#include <WiFi.h>
#include "DHT.h"

#define DHTTYPE DHT11

// WiFi credentials
const char* WIFI_SSID = "cslab";
const char* WIFI_PASSWORD = "aksesg31";

// MQTT settings
const char* MQTT_SERVER = "35.198.230.42";
const char* MQTT_TOPIC_TEMPERATURE = "iot/temp";
const char* MQTT_TOPIC_PIR = "iot/pir";
const int MQTT_PORT = 1883;

// Pins
const int dht11Pin = 42; // DHT11 sensor pin
const int pirPin = 4;   // PIR sensor pin

// Variables
char buffer[128] = ""; // Text buffer
DHT dht(dht11Pin, DHTTYPE);
WiFiClient espClient;
PubSubClient client(espClient);
int pirState = LOW; // PIR sensor state

// Function to connect to WiFi
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WIFI_SSID);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

// Reconnect to MQTT broker
void reconnect() {
  while (!client.connected()) {
    Serial.println("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("Connected to MQTT server");
    } else {
      Serial.print("Failed, rc=");
      Serial.print(client.state());
      Serial.println(" Retrying in 5 seconds...");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200); // Initiate serial communication
  dht.begin();          // Initialize DHT sensor
  pinMode(pirPin, INPUT); // Set PIR pin as input
  setup_wifi();          // Connect to WiFi network
  client.setServer(MQTT_SERVER, MQTT_PORT); // Set MQTT server
}
