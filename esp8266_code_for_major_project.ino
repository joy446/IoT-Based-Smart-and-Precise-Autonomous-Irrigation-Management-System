#include <ESP8266WiFi.h>
#include <DHT.h>

#define DHTPIN D2        // Pin where the DHT11 is connected
#define DHTTYPE DHT11    // DHT11 sensor type
DHT dht(DHTPIN, DHTTYPE);

#define MOTOR_PIN D6     // Motor connected to D6
#define LED_PIN D5       // LED connected to D5
#define SOIL_PIN A0      // Soil moisture sensor connected to A0

const char* ssid = "joy@pi"; // Replace with your Wi-Fi SSID
const char* password = "12345678"; // Replace with your Wi-Fi password

WiFiServer server(80);

void setup() {
  Serial.begin(115200);
  dht.begin();
  
  // Set pin modes
  pinMode(MOTOR_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
  pinMode(SOIL_PIN, INPUT);

  digitalWrite(MOTOR_PIN, LOW);  // Initially motor is off
  digitalWrite(LED_PIN, LOW);    // Initially LED is off
  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  
  // Start the server
  server.begin();
  Serial.println("Server started");
}

void loop() {
  WiFiClient client = server.available();
  if (!client) {
    return;
  }

  // Wait until the client sends some data
  while (!client.available()) {
    delay(1);
  }

  String request = client.readStringUntil('\r');
  Serial.println(request);
  client.flush();

  // Handle HTTP request for motor control
  if (request.indexOf("/motor/on") != -1) {
    digitalWrite(MOTOR_PIN, HIGH);
    digitalWrite(LED_PIN, HIGH);
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println("");
    client.println("Motor is ON");
  } else if (request.indexOf("/motor/off") != -1) {
    digitalWrite(MOTOR_PIN, LOW);
    digitalWrite(LED_PIN, LOW);
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println("");
    client.println("Motor is OFF");
  }

  // Handle HTTP request for sensor data
  if (request.indexOf("/get-data") != -1) {
    int soil_moisture = analogRead(SOIL_PIN);
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();
    Serial.println(soil_moisture);
    Serial.println(humidity);
    Serial.println(temperature);
    

    // Send the sensor data back as a JSON response
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: application/json");
    client.println("");
    client.print("{\"soil_moisture\":");
    client.print(soil_moisture);
    client.print(", \"temperature\":");
    client.print(temperature);
    client.print(", \"humidity\":");
    client.print(humidity);
    client.println("}");
  }
}
