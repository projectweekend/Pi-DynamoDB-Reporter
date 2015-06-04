import json
from serial import Serial


def main():
    ser = Serial(port='/dev/ttyAMA0', baudrate=9600)
    while True:
        print(ser.readline())


if __name__ == '__main__':
    main()
