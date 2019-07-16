from __future__ import print_function
import boto3
import json
import logging

def lambda_handler(event, context):
    """Stores a given video file and associates the user with it.
    """
    print('Received event: %s' % json.dumps(event, indent=2))
    return {}
