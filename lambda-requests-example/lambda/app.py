import requests


def lambda_handler(event: dict, context: dict) -> dict:
    response = requests.get("https://api.github.com")
    return {
        "statusCode": 200,
        "body": response.json(),
    }
