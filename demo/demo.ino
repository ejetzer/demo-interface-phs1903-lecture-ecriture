byte valeur[4] = {4, 5, 6, 7};
bool envoye = false;

void setup() {
  Serial.begin(115200);
}

void loop() {
  if (Serial.available()) {
    //valeur = Serial.readString();
    for (int idx=0; idx<4; idx++) {
      byte c = Serial.read() & 0b11111;
      valeur[idx] = c;
    }
    envoye = false;
  } else if (!envoye) {
    for (int idx=0; idx<4; idx++) {
      Serial.write(valeur[idx] & 0b11111);
    }
    envoye = true;
  }
}
