import os


def handler(event, context):
    return {
        "statusCode": 200,
        "body": f"Hello world from {os.getenv('ENVIRONMENT')}!",
    }
