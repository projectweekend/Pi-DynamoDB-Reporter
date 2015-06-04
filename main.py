import json
from serial import Serial


def main():
    ser = Serial(port='/dev/ttyAMA0', baudrate=9600)
    while True:
        sensor_reading = ser.readline()
        data = json.loads(sensor_reading)
        print(data)


if __name__ == '__main__':
    main()
