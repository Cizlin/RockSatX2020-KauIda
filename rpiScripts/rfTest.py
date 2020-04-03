# Example of interaction with a BLE UART device using a UART service
# implementation.
# Author: Tony DiCola
import Adafruit_BluefruitLE
from Adafruit_BluefruitLE.services import UART
import uuid
import time

# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()

#RSSI_UUID = uuid.UUID('00110011-4455-6677-8899-AABBCCDDEEFF')
#VALUE_UUID = uuid.UUID('00110011-4455-6677-8899-AABBCCDDEEFF')

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
    print('Using adapter: {0}'.format(adapter.name))

    # Disconnect any currently connected UART devices.  Good for cleaning up and
    # starting from a fresh state.
    print('Disconnecting any connected UART devices...')
    UART.disconnect_devices()

    # Scan for UART devices.
    print('Searching for UART device...')
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

    print('Connecting to device...')
    device.connect()  # Will time out after 60 seconds, specify timeout_sec parameter
                      # to change the timeout.

    # Once connected do everything else in a try/finally to make sure the device
    # is disconnected when done.
    try:
	# should be the easiest way to get rssi, but library has a bug
	print ('get rssi')
	rssi = device.rssi
	print (rssi)
        # Wait for service discovery to complete for the UART service.  Will
	# time out after 60 seconds (specify timeout_sec parameter to override).
#        print('Discovering services...')
#	UART.discover(device)
#        device.discover([RSSI_UUID],[VALUE_UUID])
#	print('RSSI service discovered...')

        # Once service discovery is complete create an instance of the service
        # and start interacting with it.
#        uart = UART(device)

	# Open a file to write to
#	file = open("rfTest_Output.txt","w")

        # Write a string to the TX characteristic.
	#uart.write(b'hi\n')

#	file.write('RSSI is measured in decibels from 0 to -120 with 0 being the strongest\n RSSI:\n')

#	timeout = 10 # 10 seconds

#	timeout_start = time.time()

	#uart = device.find_service(RSSI_UUID)
	#value = uart.find_characteristic(VALUE_UUID)

#	print('Outputting...')



#	rssi = value.read_value()
#	print(rssi)
	#def received(data):
	#	print('Received: {0}'.format(data))


	#value.start_notify(received)

	#print('Waiting to recieve data...')
	#time.sleep(60)



	#received = RSSI.read(timout_sec=60)
#	if received is not None:
#		print('{0}'.format(received))
#	else:
#		print('received no data!')


#	print('Finished...')
#	while time.time() < timeout_start + timeout:

       		# Now wait up to one minute to receive data from the device.
 #   		print('Waiting to receive rssi from the device...')
  #     		received = uart.read()
   #    		if received is not None:
     			# Received data, print it out.
#        		print('{0}'.format(received))
		#	file.write(received)
    #   		else:
          		# Timeout waiting for data, None is returned.
     #      		print('Received no data!')
    finally:
	print('Disconnecting...')
        # Make sure device is disconnected on exit.
        device.disconnect()
#	file.close()


# Initialize the BLE system.  MUST be called before other BLE calls!
ble.initialize()

# Start the mainloop to process BLE events, and run the provided function in
# a background thread.  When the provided main function stops running, returns
# an integer status code, or throws an error the program will exit.
ble.run_mainloop_with(main)
