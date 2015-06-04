import uuid
import time
import json
from serial import Serial
from boto.dynamodb2.table import Table


def main():
    pi_bank = Table('pi_bank')
    ser = Serial(port='/dev/ttyAMA0', baudrate=9600)
    while True:
        reading = json.loads(ser.readline())

        # convert floats to strings for DynamoDB
        for k, v in reading.iteritems():
            reading[k] = str(v)

        data = {
            'id': str(uuid.uuid4()),
            'device': 'pi_01',
            'timestamp': int(time.time()),
            'reading_type': 'thpl_01',
            'reading_data': reading
        }

        pi_bank.put_item(data=data)


if __name__ == '__main__':
    main()
