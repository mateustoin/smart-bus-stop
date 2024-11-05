#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <UniversalTelegramBot.h>

// Wifi network station credentials
#define WIFI_SSID ""
#define WIFI_PASSWORD ""

// Telegram BOT Token (Get from Botfather)
#define BOT_TOKEN ""

// Identificator responsible 
#define CHAT_ID ""

// WiFi and Bot objects
WiFiClientSecure secured_client;
UniversalTelegramBot bot(BOT_TOKEN, secured_client);

// GPIO used
const int buttonPin = 37;  // the number of the pushbutton pin
const int ledPin = 19;    // the number of the LED pin

// variables will change:
int buttonState = 0;  // variable for reading the pushbutton status

void setup() {
  Serial.begin(115200);
  Serial.println("Starting configs and init WiFi");
  Serial.println();

  // attempt to connect to Wifi network:
  Serial.print("Connecting to Wifi SSID ");
  Serial.print(WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  secured_client.setCACert(TELEGRAM_CERTIFICATE_ROOT); // Add root certificate for api.telegram.org
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(500);
  }
  Serial.print("\nWiFi connected. IP address: ");
  Serial.println(WiFi.localIP());

  Serial.print("Retrieving time: ");
  configTime(0, 0, "pool.ntp.org"); // get UTC time via NTP
  time_t now = time(nullptr);
  while (now < 24 * 3600)
  {
    Serial.print(".");
    delay(100);
    now = time(nullptr);
  }
  Serial.println(now);

  // initialize the LED pin as an output:
  pinMode(ledPin, OUTPUT);
  // initialize the pushbutton pin as an input:
  pinMode(buttonPin, INPUT);
}

void loop() {
  buttonState = digitalRead(buttonPin);

  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  if (buttonState == LOW) {
    digitalWrite(ledPin, HIGH); // Turn LED on

    // Send message and location to Telegram Channel
    bot.sendMessage(CHAT_ID, "[ESP32] Houve uma ocorrência reportada pelo panic button! Localização:");
    bot.sendLocation(CHAT_ID, -22.813407, -47.0643614);
    delay(100);

  } else {
    digitalWrite(ledPin, LOW); // Turn LED off
  }
}
