import os

import boto3

from .prompts import SYSTEM_PROMPT


def get_answer(question: str, bedrock: boto3.client) -> str:
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

    return response["output"]["message"]["content"][0]["text"]