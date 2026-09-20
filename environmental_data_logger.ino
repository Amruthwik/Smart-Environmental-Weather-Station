#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP085_U.h>
#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT11
#define GAS_PIN 34

DHT dht(DHTPIN, DHTTYPE);
Adafruit_BMP085_Unified bmp = Adafruit_BMP085_Unified(10085);

unsigned long lastMillis = 0;
const unsigned long interval_ms = 15000; // 15 seconds

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("\n============================================");
  Serial.println("     BMP180 + DHT11 + FC-22 Logger");
  Serial.println("============================================");
  Serial.println("Sensor warm-up: FC-22 requires ~120 s for stable readings.\n");

  dht.begin();

  if (!bmp.begin()) {
    Serial.println("ERROR: BMP180 not detected! Check wiring.");
    while (1);
  }

  analogReadResolution(12);
  delay(2000);

  Serial.println("Temperature (C),Humidity (%),Pressure (hPa),Gas (ADC)");
  Serial.println("----------------------------------------------------------");
}

void loop() {
  unsigned long now = millis();

  if (now - lastMillis >= interval_ms) {
    lastMillis = now;

    float hum = dht.readHumidity();

    float temp_bmp = 0;
    float pressure = 0;

    bmp.getTemperature(&temp_bmp);
    bmp.getPressure(&pressure);
    pressure = pressure / 100.0; // Pa to hPa

    int gas_raw = analogRead(GAS_PIN);

    if (isnan(hum)) {
      Serial.println("#ERR_DHT");
    } else {
      Serial.printf("%.2f,%.2f,%.2f,%d\n",
                    temp_bmp, hum, pressure, gas_raw);
    }
  }
}
