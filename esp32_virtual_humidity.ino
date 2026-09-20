#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BMP085_U.h>
#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT11
#define GAS_PIN 34

DHT dht(DHTPIN, DHTTYPE);
Adafruit_BMP085_Unified bmp = Adafruit_BMP085_Unified(10085);

// Regression coefficients obtained from the trained Python model
const float A_TEMP = -1.542;
const float B_PRESS = 4.607;
const float C_INT  = -4440.737;

unsigned long lastMillis = 0;
const unsigned long interval_ms = 15000; // 15 seconds

void setup() {
  Serial.begin(115200);
  delay(1000);

  Serial.println("\n============================================");
  Serial.println("   BMP180 + DHT11 + FC-22 + Virtual Humidity");
  Serial.println("============================================");
  Serial.println("Sensor warm-up: FC-22 requires ~120 s for stable readings.\n");

  dht.begin();

  if (!bmp.begin()) {
    Serial.println("ERROR: BMP180 not detected! Check wiring.");
    while (1);
  }

  analogReadResolution(12);
  delay(2000);

  Serial.println("Temp_BMP(C)\tPressure(hPa)\tGas(ADC)\tReal_Humidity(%)\tPred_Humidity(%)");
  Serial.println("--------------------------------------------------------------------------");
}

void loop() {
  unsigned long now = millis();

  if (now - lastMillis >= interval_ms) {
    lastMillis = now;

    float hum_real = dht.readHumidity();

    float temp_bmp = 0;
    float pressure = 0;

    bmp.getTemperature(&temp_bmp);
    bmp.getPressure(&pressure);
    pressure = pressure / 100.0; // Pa to hPa

    int gas_raw = analogRead(GAS_PIN);

    // Predict humidity using the trained regression model
    float hum_pred = (A_TEMP * temp_bmp) + (B_PRESS * pressure) + C_INT;
    hum_pred = constrain(hum_pred, 0.0, 100.0);

    if (isnan(hum_real)) {
      Serial.println("#ERR_DHT");
    } else {
      Serial.printf("%.2f\t%.2f\t%d\t%.2f\t%.2f\n",
                    temp_bmp, pressure, gas_raw, hum_real, hum_pred);
    }
  }
}
