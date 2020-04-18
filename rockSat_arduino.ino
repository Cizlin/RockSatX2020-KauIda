#include "Adafruit_BLE.h"
#include "Adafruit_BluefruitLE_UART.h"
#include "BluefruitConfig.h"

#include <Adafruit_Sensor.h>
#include "Adafruit_BME680.h"


#if SOFTWARE_SERIAL_AVAILABLE
  #include <SoftwareSerial.h>
#endif

    #define FACTORYRESET_ENABLE         0
    #define MINIMUM_FIRMWARE_VERSION    "0.6.6"
    #define MODE_LED_BEHAVIOUR          "MODE"

#define BME_SCK 13
#define BME_MISO 12
#define BME_MOSI 11
#define BME_CS 10

#define SEALEVELPRESSURE_HPA (1013.25)
/*=========================================================================*/

// Create the bluefruit object, either software serial...uncomment these lines

SoftwareSerial bluefruitSS = SoftwareSerial(BLUEFRUIT_SWUART_TXD_PIN, BLUEFRUIT_SWUART_RXD_PIN);

Adafruit_BluefruitLE_UART ble(bluefruitSS, BLUEFRUIT_UART_MODE_PIN,
                      BLUEFRUIT_UART_CTS_PIN, BLUEFRUIT_UART_RTS_PIN);


Adafruit_BME680 bme; // I2C

void setup(void)
{

  delay(500);

  Serial.begin(115200);
  if (!bme.begin()) {
    //Serial.println(F("Could not find a valid BME680 sensor, check wiring!"));
    while (1);
  }
  /* Initialise the module */

  if ( !ble.begin(VERBOSE_MODE) )
  {
    //error(F("Couldn't find Bluefruit, make sure it's in CoMmanD mode & check wiring?"));
  }
  ble.echo(false);

  ble.sendCommandCheckOK(F("AT+GATTLIST"));


  ble.verbose(false);
  
  /* Wait for connection */
  ble.setMode(BLUEFRUIT_MODE_COMMAND);
  //Serial.println(F("Waiting for connection..."));
  while (!ble.isConnected()) {
      delay(500);
  }


  // Sensors
  bme.setTemperatureOversampling(BME680_OS_8X);
  bme.setHumidityOversampling(BME680_OS_2X);
  bme.setPressureOversampling(BME680_OS_4X);
  bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
  bme.setGasHeater(320, 150); // 320*C for 150 ms
  Serial.println(F("******************************"));
}

/**************************************************************************/
/*!
    @brief  Constantly poll for new command or response data
*/
/**************************************************************************/
char value_string[5] = {""};
int cur = 0;
char c;
void loop(void)
{
  

  //                                   RSSI
  //************************************************************************************//
  ble.println(F("AT+BLEGETRSSI"));

  while ( ble.available() )
  {
    c = ble.read();
    //c != 'O' && c != 'K' && c != 'E' && c != 'R' && c != '-' && c != '\n' && c != '\r'
    if (c >= '0' && c <= '9') {
      value_string[cur] = c;
      cur++;
     }
  } 
  cur = 0;
  ble.print(F("AT+GATTCHAR=1,"));
  ble.println(atoi(value_string));

  for (int a = 0; a < 5; a++) {
    value_string[a] = "";
  }

  
  //                                Sensors
  //*********************************************************************************/

  // Temp
  ble.print(F("AT+GATTCHAR=2,"));
  ble.println(int(bme.temperature*100));
  // Pressure
  ble.print(F("AT+GATTCHAR=3,"));
  ble.println(bme.pressure);
  // Humidity
  ble.print(F("AT+GATTCHAR=4,"));
  ble.println(int(bme.humidity*100));
  // Gas
  ble.print(F("AT+GATTCHAR=5,"));
  ble.println(bme.gas_resistance / 10);
  // Altitude
  ble.print(F("AT+GATTCHAR=6,"));
  ble.println(int(bme.readAltitude(SEALEVELPRESSURE_HPA)*100));
  

    delay(100);
}
