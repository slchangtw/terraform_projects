import boto3
from libs.conversation import get_answer

bedrock = boto3.client(service_name="bedrock-runtime", region_name="eu-central-1")


def lambda_handler(event: dict, context: dict) -> dict:
    try:
        max_tokens = event.get("MAX_INPUT_CHARACTERS")
        question = event["question"][:max_tokens]

        answer = get_answer(question, bedrock)

        return {
            "status": "success",
            "body": answer,
        }
    except Exception as e:
        return {
            "status": "error",
            "body": str(e),
        }
