from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey, RangeKey
from boto.dynamodb2.types import NUMBER, STRING
from boto.exception import JSONResponseError


def main():
    try:
        Table.create(
            'pi_project_data',
            schema=[
                HashKey('device_name', data_type=STRING),
                RangeKey('timestamp', data_type=NUMBER)
            ],
            throughput={
                'read': 1,
                'write': 1
            }
        )
        print('Table created: pi_project_data')
    except JSONResponseError as e:
        print(e.message)


if __name__ == '__main__':
    main()
