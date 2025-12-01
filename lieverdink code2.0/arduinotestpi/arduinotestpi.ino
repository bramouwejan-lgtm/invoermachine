#include <ArduinoJson.h>

void setup() {
  Serial.begin(115200);
  
  while (!Serial);  // wacht tot seriële verbinding actief is
  Serial.println("Arduino JSON test gestart...");
}

void loop() {
  if (Serial.available()) {
    String jsonString = Serial.readStringUntil('\n'); // wacht tot newline
    Serial.print("Ontvangen JSON: ");
    Serial.println(jsonString);

    //Parse de JSON-string
    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, jsonString);

    if (error) {
      Serial.print("Fout bij JSON lezen: ");
      Serial.println(error.c_str());
      return;
    }

    // Lees waarden uit
    const char* message = doc["Message"];
    int breedte = doc["Breedte"] | -1;   // default -1 als niet aanwezig
    bool forward = doc["Forward"] | false;

    // Print waarden
    Serial.print("Message: "); Serial.println(message);
    Serial.print("Breedte: "); Serial.println(breedte);
    Serial.print("Forward: "); Serial.println(forward ? "true" : "false");
    Serial.println("-----------------------------");
  }
}
