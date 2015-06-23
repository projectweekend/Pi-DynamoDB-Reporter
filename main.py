import time
import json
from serial import Serial
from boto.dynamodb2.table import Table


def main():
    pi_bank = Table('pi_project_data')
    ser = Serial(port='/dev/ttyAMA0', baudrate=9600)
    while True:
        data = {
            'device_name': 'pi001',
            'timestamp': int(time.time()),
        }
        reading = json.loads(ser.readline())

        # convert floats to strings for DynamoDB
        for k, v in reading.iteritems():
            data[k] = str(v)

        pi_bank.put_item(data=data)


if __name__ == '__main__':
    main()
