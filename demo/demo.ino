String valeur = "rien";
bool envoye = false;

void setup() {
  Serial.begin(115200);
}

void loop() {
  if (Serial.available()) {
    valeur = Serial.readString();
    envoye = false;
  } else if (!envoye) {
    Serial.println(valeur);
    envoye = true;
  }
}
