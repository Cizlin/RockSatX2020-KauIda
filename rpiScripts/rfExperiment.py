# Prints rssi out


import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART
import uuid
import time
import dbus

# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()

UART_SERVICE_UUID = uuid.UUID('6E400001-B5A3-F393-E0A9-E50E24DCCA9E')
TX_CHAR_UUID      = uuid.UUID('6E400002-B5A3-F393-E0A9-E50E24DCCA9E')
RX_CHAR_UUID      = uuid.UUID('6E400003-B5A3-F393-E0A9-E50E24DCCA9E')

SENSE_SERVICE_UUID = uuid.UUID('00006969-6969-6969-6969-696969696969')
RSSI_CHAR_UUID    = uuid.UUID('00000420-6969-6969-6969-696969696969')
TEMP_CHAR_UUID    = uuid.UUID('00000421-6969-6969-6969-696969696969')
PRESS_CHAR_UUID   = uuid.UUID('00000422-6969-6969-6969-696969696969')
HUM_CHAR_UUID     = uuid.UUID('00000423-6969-6969-6969-696969696969')
GAS_CHAR_UUID     = uuid.UUID('00000424-6969-6969-6969-696969696969')
ALT_CHAR_UUID     = uuid.UUID('00000425-6969-6969-6969-696969696969')

# Main function implements the program logic so it can run in a background
# thread.  Most platforms require the main thread to handle GUI events and other
# asyncronous events like BLE actions.  All of the threading logic is taken care
# of automatically though and you just need to provide a main function that uses
# the BLE provider.
def main():
    # Clear any cached data because both bluez and CoreBluetooth have issues with
    # caching data and it going stale.
    ble.clear_cached_data()

    # Get the first available BLE network adapter and make sure it's powered on.
    adapter = ble.get_default_adapter()
    adapter.power_on()
    #print('Using adapter: {0}'.format(adapter.name))

    # Disconnect any currently connected UART devices.  Good for cleaning up and
    # starting from a fresh state.
    #print('Disconnecting any connected UART devices...')
    ble.disconnect_devices()

    # Scan for UART devices.
    #print('Searching for UART device...')
    try:
        adapter.start_scan()
        # Search for the first UART device found (will time out after 60 seconds
        # but you can specify an optional timeout_sec parameter to change it).
        device = UART.find_device()
        if device is None:
            raise RuntimeError('Failed to find UART device!')
    finally:
        # Make sure scanning is stopped before exiting.
        adapter.stop_scan()

    #print('Connecting to device...')
    device.connect()  # Will time out after 60 seconds, specify timeout_sec parameter
                      # to change the timeout.
    # Once connected do everything else in a try/finally to make sure the device
    # is disconnected when done.
    try:
        # Wait for service discovery to complete for the UART service.  Will
	# time out after 60 seconds (specify timeout_sec parameter to override).
        #print('Discovering services...')

        try:
		device.discover([SENSE_SERVICE_UUID],[RSSI_CHAR_UUID,TEMP_CHAR_UUID,PRESS_CHAR_UUID,
			HUM_CHAR_UUID,GAS_CHAR_UUID,ALT_CHAR_UUID])
	finally:
		#print('Discovery finished...')
		pass
        # Once service discovery is complete create an instance of the service
        # and start interacting with it.

	# Open a file to write to
	file = open("rfOutput.csv","w")

	try:
		sensors  = device.find_service(SENSE_SERVICE_UUID)
		rssi_char     = sensors.find_characteristic(RSSI_CHAR_UUID)
		temp_char     = sensors.find_characteristic(TEMP_CHAR_UUID)
		pressure_char = sensors.find_characteristic(PRESS_CHAR_UUID)
		humidity_char = sensors.find_characteristic(HUM_CHAR_UUID)
		gas_char      = sensors.find_characteristic(GAS_CHAR_UUID)
		alt_char      = sensors.find_characteristic(ALT_CHAR_UUID)

	finally:
		#print('Sensors discovered succesfully')
		pass


	def unwrap(val):
       		if isinstance(val, (dbus.Array, list, tuple)):
			hex_ans = ''
			#return [unwrap(x) for x in val]
			for x in val:
				hex_ans = hex_ans + unwrap(x)
			return int(hex_ans, 16)
    		if isinstance(val, dbus.Byte):
			hex_string = str(bytes(hex(val)))
	     		return hex_string.replace('0x','')
    		print ('Error: Recieved different type!')
		return val

	timeout = 10 # 10 seconds

        timeout_start = time.time()
	print('RF Experiment has started')
	#print('RSSI:  TEMP:  PRESSURE:  HUMIDITY:  GAS:  ALT: ')
	file.write('RSSI (dB),TEMP (*C),PRESSURE (hPa),HUMIDITY (%),GAS (KOhms),ALT (m)\n')
	while time.time() < timeout_start + timeout:

       		rssi     = str(unwrap(rssi_char.read_value()))
		temp     = str(float(unwrap(temp_char.read_value()))/100)
		pressure = str(float(unwrap(pressure_char.read_value())))
		humidity = str(float(unwrap(humidity_char.read_value()))/100)
		gas      = str(float(unwrap(gas_char.read_value()))/100)
		alt	 = str(float(unwrap(alt_char.read_value()))/100)


		#print(' ' + rssi + '    ' + temp + '   ' + pressure + '    ' + humidity + '    ' + gas + '    ' + alt)
		file.write(rssi + ',' + temp + ',' + pressure + ',' + humidity + ',' + gas + ',' + alt + '\n')
    finally:
	print('Disconnecting...')
        # Make sure device is disconnected on exit.
        device.disconnect()
	file.close()


# Initialize the BLE system.  MUST be called before other BLE calls!
ble.initialize()

# Start the mainloop to process BLE events, and run the provided function in
# a background thread.  When the provided main function stops running, returns
# an integer status code, or throws an error the program will exit.
ble.run_mainloop_with(main)
