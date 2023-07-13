"""
Command line arguments:
<this.py> [key]

key: string
  Must be 16 characters long
"""

import sys
import boto3
import psycopg2
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from datetime import date


def validate_and_parse_keys():
    if len(sys.argv) != 2:
        sys.exit('Incorrect number of arguments. The first argument for key is required')

    key_raw = sys.argv[1]
    if len(key_raw) != 16:
        sys.exit('key has to be 16 characters long.')
    return key_raw.encode("utf-8")


def fetch_message(url):
    # Receive the message from the specified SQS queue
    response = sqs.receive_message(QueueUrl=url)
    return response['Messages']


def str_to_dict(text):
    result = json.loads(text)
    return result


def encrypt(data_str, key):
    data = pad(data_str.encode(), 16)
    cipher = AES.new(key, AES.MODE_ECB)
    masked_ip = cipher.encrypt(data)
    return masked_ip


def decrypt(masked_ip, key):
    cipher = AES.new(key, AES.MODE_ECB)
    data = cipher.decrypt(masked_ip)
    return unpad(data, 16).decode()


def version_converter(version):
    result = "".join(version.split('.'))
    return int(result)


def check_connection(connection):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM postgres.public.user_logins"
    )
    cursor.close()


def etl(connection, key):
    cursor = connection.cursor()

    messages = fetch_message(url=SQS_QUEUE_URL)

    for i in range(len(messages)):
        row_str = messages[i]['Body']
        row = str_to_dict(row_str)
        encrypted_ip = encrypt(row['ip'], key)
        encrypted_device_id = encrypt(row['device_id'], key)

        cursor.execute("""
                INSERT INTO postgres.public.user_logins 
                (user_id, device_type, masked_ip, masked_device_id,
                locale, app_version, create_date) 
                values(%s, %s, %s, %s, %s, %s, %s)
                """,
                       (row['user_id'], row['device_type'], encrypted_ip, encrypted_device_id,
                        row['locale'], version_converter(row['app_version']), date.today()
                        )
                       )

    connection.commit()
    cursor.close()


if __name__ == "__main__":
    # Set the variables
    SQS_QUEUE_URL = 'http://localhost:4566/000000000000/login-queue'

    # Set up the SQS client
    sqs = boto3.client(
        'sqs',
        endpoint_url='http://localhost:4566',
        region_name='us-east-1',
        aws_access_key_id='dummy',
        aws_secret_access_key='dummy',
        aws_session_token='dummy'
    )

    # Set up connection
    conn = psycopg2.connect(
        "host=localhost port=5432 dbname=postgres user=postgres "
        "password=postgres")

    # Retrieve key for encryption and decryption
    key = validate_and_parse_keys()

    # Execute
    etl(conn, key)
