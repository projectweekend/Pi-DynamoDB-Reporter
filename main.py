import uuid
import time
import json
from serial import Serial
from boto.dynamodb2.table import Table


def main():
    # pi_bank = Table('pi_bank')
    ser = Serial(port='/dev/ttyAMA0', baudrate=9600)
    while True:
        data = {
            'id': uuid.uuid4(),
            'device': 'pi_01',
            'timestamp': int(time.time()),
            'reading_type': 'thpl_01',
            'reading_data': json.loads(ser.readline())
        }
        print(data)


if __name__ == '__main__':
    main()
