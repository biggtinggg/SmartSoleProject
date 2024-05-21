import bluetooth        # If libray is not install, try pip install pybluez OR pip install git+https://github.com/pybluez/pybluez.git#egg=pybluez

def scan():
    print("Scanning for bluetooth devices:")

    devices = bluetooth.discover_devices(lookup_names = True, lookup_class = True)

    number_of_devices = len(devices)

    print(number_of_devices,"devices found")

    for addr, name, device_class in devices:
        print("\n")
        print("Device:")
        print("Device Name: %s" % (name))
        print("Device MAC Address: %s" % (addr))
        print("Device Class: %s" % (device_class))
        print("\n")

    return

def pair():
    bd_addr = "d5:b6:c5:1e:71:4b"
    port = 1

    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((bd_addr, port))
    print("The bluetooth device was connected successfully")
