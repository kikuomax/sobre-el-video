from __future__ import print_function
import base64
import boto3
import hashlib
import json
import logging
import os


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def sha256(data):
    """Caclaultes the SHA256 digest of given data.

    Returns a digest string of `data` represented as a sequence of hexadecimal
    digits.
    """
    m = hashlib.sha256()
    m.update(data)
    return m.hexdigest()


def save_data(bucket, key, data):
    """Saves given data associated with a given key in a specified bucket.
    """
    s3 = boto3.client('s3')
    response = s3.put_object(Bucket=bucket, Key=key, Body=data)
    print(json.dumps(response, indent=2))


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
    return {
        'digest': digest
    }
