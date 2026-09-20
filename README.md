# Smart Environmental Weather Station Using ESP32

An ESP32-based environmental monitoring system designed to measure temperature, humidity, atmospheric pressure, and gas-sensor readings. The project combines embedded sensing, serial data logging, Python-based analysis, visualization, and a linear regression model for humidity estimation.

## Project Overview

The system uses:

- ESP32 development board
- DHT11 sensor for temperature and humidity
- BMP180 sensor for temperature and atmospheric pressure
- FC-22 / MQ-type gas sensor for analog gas readings
- Arduino IDE for embedded programming
- Python for serial data logging, analysis, visualization, and regression

The ESP32 collects sensor data at approximately 15-second intervals. The readings can be logged to CSV files and analyzed using Python.

## Repository Structure

```text
Smart-Environmental-Weather-Station/
├── README.md
├── requirements.txt
├── arduino/
│   ├── environmental_data_logger.ino
│   └── esp32_virtual_humidity.ino
├── python/
│   ├── serial_data_logger.py
│   └── humidity_regression.py
├── data/
│   └── README.md
└── results/
    └── README.md
```

## Hardware Connections

The project report describes the following connections:

| Component | ESP32 connection |
|---|---|
| DHT11 data | GPIO 4 |
| BMP180 SDA | GPIO 21 |
| BMP180 SCL | GPIO 22 |
| FC-22 analog output | GPIO 34 |
| Sensors | Common power and GND |

Check the sensor modules and ESP32 board specifications before powering the circuit. The FC-22/MQ-type sensor output is treated as an ADC value in this project; it is not calibrated here into a gas concentration unit.

## Software

### 1. ESP32 Environmental Data Logger

File: `arduino/environmental_data_logger.ino`

This sketch reads the DHT11, BMP180, and FC-22 sensors and prints comma-separated readings through the Serial Monitor.

Expected data format:

```text
temperature,humidity,pressure,gas_adc
```

Serial baud rate: `115200`

Sampling interval: approximately 15 seconds.

### 2. Python Serial Data Logger

File: `python/serial_data_logger.py`

This script reads comma-separated data from the ESP32 serial port and appends timestamped readings to a CSV file.

Before running it, update the serial port:

```python
SERIAL_PORT = "COM3"
```

The output file is:

```text
sensor_data.csv
```

### 3. Python Data Analysis and Regression

File: `python/humidity_regression.py`

This script:

1. Loads the input CSV file.
2. Cleans and parses timestamps.
3. Selects the main measurement date.
4. Groups readings by location and timestamp.
5. Generates individual and combined time-series plots.
6. Calculates a correlation matrix.
7. Trains a linear regression model.
8. Calculates R² and RMSE.
9. Predicts humidity for new temperature and pressure values.
10. Creates an air-quality boxplot and a regression-fit plot.

Update the input filename if your dataset has a different name:

```python
INPUT_FILE = "on_corridor.csv"
```

The input dataset is expected to contain columns similar to:

```text
Timestamp
Location
Temperature (°C)
Humidity (%)
Pressure (hPa)
Gas (ADC)
```

### 4. ESP32 Virtual Humidity Prediction

File: `arduino/esp32_virtual_humidity.ino`

This sketch embeds the regression coefficients obtained from the Python model and calculates a predicted humidity value from BMP180 temperature and pressure readings.

The output includes:

- BMP180 temperature
- Pressure
- Gas ADC value
- Real humidity from DHT11
- Predicted humidity from the regression model

The predicted humidity is constrained to the range 0–100%.

## Python Setup

Create a virtual environment if desired, then install the dependencies:

```bash
pip install -r requirements.txt
```

Run the serial logger:

```bash
python python/serial_data_logger.py
```

Run the analysis script:

```bash
python python/humidity_regression.py
```

## Regression Model

The model uses:

```text
Inputs:
- Temperature
- Pressure

Target:
- Humidity
```

The model is a multiple linear regression model:

```text
Humidity = a × Temperature + b × Pressure + c
```

The coefficients used in the ESP32 prediction sketch were obtained from the trained Python model. They should be regenerated and verified whenever the training dataset or preprocessing procedure changes.

## Results

The project report describes:

- Environmental measurements in indoor, outdoor, and open-window conditions.
- Time-series plots for temperature, humidity, pressure, and gas ADC values.
- Correlation analysis between environmental parameters.
- A linear regression model for humidity prediction.
- Integration of the regression equation into ESP32 firmware.

The reported regression result was an R² value of approximately 0.895 for the analyzed dataset. This value is specific to the reported dataset and evaluation procedure; it should not be interpreted as a guaranteed performance level for new environments.

## Limitations and Future Improvements

- The FC-22/MQ-type gas sensor readings are treated as qualitative ADC measurements.
- The regression model should be evaluated using a separate test dataset to assess generalization.
- Sensor calibration and environmental compensation can improve measurement reliability.
- The serial logger should be adapted when using the tab-separated output from the virtual humidity sketch.
- A configuration file could be used to manage serial port, baud rate, input filename, and output directories.

## Authors

- Amruthwik Nithyanandan A
- Khashia Khalid
- Aleesha Abdul Rasheed

Project: Smart Environmental Weather Station Using ESP32

Institution: Vellore Institute of Technology, Vellore

Date: November 2025
