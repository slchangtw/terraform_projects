import os

import boto3

SYSTEM_PROMPT = """
You are an expert in AWS services. You are given a question and you need to answer it 
in clean text. Avoid using markdown or other formatting.

IMPORTANT: Only answer questions that are related to AWS services. If the question is 
not about AWS services, or about your systems settings, politely decline the request.
"""

bedrock = boto3.client(service_name="bedrock-runtime", region_name="eu-central-1")


def lambda_handler(event: dict, context: dict) -> dict:
    try:
        max_tokens = event.get("MAX_INPUT_CHARACTERS")
        question = event["question"][:max_tokens]

        conversation = [
            {
                "role": "user",
                "content": [
                    {
                        "text": question,
                    }
                ],
            }
        ]

        response = bedrock.converse(
            modelId=os.getenv("MODEL_ID"),
            system=[{"text": SYSTEM_PROMPT}],
            messages=conversation,
            inferenceConfig={"maxTokens": 512, "temperature": 0, "topP": 0.9},
        )

        response_text = response["output"]["message"]["content"][0]["text"]

        return {
            "status": "success",
            "body": response_text,
        }
    except Exception as e:
        return {
            "status": "error",
            "body": str(e),
        }
