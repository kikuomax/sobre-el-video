from __future__ import print_function
import base64
import boto3
from datetime import datetime, timezone
import hashlib
import json
import logging
import os


LOGGER = logging.getLogger('store_video')
LOGGER.setLevel(logging.DEBUG)


def sha256(data):
    """Caclaultes the SHA256 digest of given data.

    Returns the SHA256 digest of `data` represented as a sequence of hexadecimal
    digits.
    """
    m = hashlib.sha256()
    m.update(data)
    return m.hexdigest()


def save_data(bucket, key, data):
    """Saves given data associated with a given key in a specified bucket.
    """
    global LOGGER
    s3 = boto3.client('s3')
    response = s3.put_object(Bucket=bucket, Key=key, Body=data)
    LOGGER.info(json.dumps(response, indent=2))


def write_record(table_name, user, key):
    """Writes records which associates a given user and a given hash key of
    the video data.

    A record has the following attributes,
    - `user`: (`str`) user name (`user`)
    - `tag`: (`str`) a string "vidoe:" + the hash key of the video data (`key`)
    - `timestamp`: (`str`) timestamp when this function is called in
      the ISO 8601 form without timezone (UTC); e.g., `2019-07-21T00:48:00Z`
    """
    global LOGGER
    db = boto3.client('dynamodb')
    now = datetime.now(timezone.utc)
    now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ')
    item = {
        'User': {
            'S': user
        },
        'Tag': {
            'S': 'video:%s' % key
        },
        'Timestamp': {
            'S': now_str
        }
    }
    attribute_names = {
        '#U': 'User' # User conflicts with DynamoDB reserved words
    }
    LOGGER.debug('%s', json.dumps(item, indent=2))
    response = db.put_item(
        TableName=table_name,
        Item=item,
        ExpressionAttributeNames=attribute_names,
        ConditionExpression='attribute_not_exists(#U)', # avoids overwriting
        ReturnConsumedCapacity='TOTAL')
    LOGGER.info('%s', json.dumps(response, indent=2))


def lambda_handler(event, context):
    """Stores a given video file and associates the user with it.

    `event` has the following key-value pairs,
    - `user`: (`str`) ID of the user who posted the video.
    - `videoBase64`: (`str`) Base64 encoded video data.
    - `type`: (`str`) Type of the video.
    """
    global LOGGER
    # obtains the configuration
    bucket_name = os.environ['VIDEO_BUCKET_NAME']
    main_table_name = os.environ['MAIN_TABLE_NAME']
    LOGGER.info('video bucket: %s', bucket_name)
    # obtains the input
    user = event['user']
    video_data_64 = event['videoBase64']
    video_type = event['type']
    LOGGER.info('user: %s', event['user'])
    LOGGER.info('video: %s', video_data_64[:32])
    LOGGER.info('type: %s', video_type)
    # decodes the video data
    video_data = base64.b64decode(video_data_64, validate=True)
    # calculates SHA256 hash
    digest = sha256(video_data)
    LOGGER.info('digest: %s', digest)
    # saves the video data in the S3 bucket
    LOGGER.info('saving video data')
    save_data(bucket_name, key=digest, data=video_data)
    # writes the record
    write_record(main_table_name, user, digest)
    return {
        'digest': digest
    }
