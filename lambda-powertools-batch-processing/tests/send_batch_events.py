import json
import subprocess
from pathlib import Path

import boto3
import pytest


@pytest.fixture
def queue_url() -> str:
    """Fixture to get the SQS queue URL from Terraform outputs"""
    try:
        # Determine terraform directory relative to this script
        # Assumes script is in tests/ and terraform is in terraform/
        script_dir = Path(__file__).resolve().parent
        terraform_dir = script_dir.parent / "terraform"

        if not terraform_dir.exists():
            pytest.fail(f"Terraform directory not found at {terraform_dir}")

        result = subprocess.run(
            ["terraform", "output", "-raw", "sqs_queue_url"],
            cwd=str(terraform_dir),
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Error getting Terraform output: {e.stderr}")
    except Exception as e:
        pytest.fail(f"Unexpected error retrieving queue URL: {e}")


@pytest.fixture
def sqs_client():
    return boto3.client("sqs")


def test_send_valid_orders_for_SQS(sqs_client, queue_url):
    """Test sending a mixed batch of valid and invalid coffee shop orders"""
    entries = [
        {
            "Id": "1",
            "MessageBody": json.dumps(
                {
                    "order_id": "101",
                    "item": "Cappuccino",
                    "amount": 1,
                    "price": 4.50,
                }
            ),
        },
        {
            "Id": "2",
            "MessageBody": json.dumps(
                {
                    "order_id": "102",
                    "item": "Croissant",
                    "amount": 2,
                    "price": 3.75,
                }
            ),
        },
        {
            "Id": "3",
            "MessageBody": json.dumps(
                {
                    "order_id": "103",
                    "item": "Cappuccino",
                    "amount": 3,
                    "price": 4.50,
                }
            ),
        },
        {
            "Id": "4",
            "MessageBody": json.dumps(
                {
                    "order_id": "104",
                    "item": "Ham Sandwich",
                    "amount": -1,  # invalid amount, but will be passed to Lambda function
                    "price": 8.99,
                }
            ),
        },
    ]

    response = sqs_client.send_message_batch(QueueUrl=queue_url, Entries=entries)

    successful = response.get("Successful", [])

    assert "Successful" in response
    assert len(successful) == 4, "Not all messages were accepted by SQS"


def test_same_order_id_for_SQS(sqs_client, queue_url):
    """Test sending orders with duplicate batch IDs, which SQS should reject"""
    entries = [
        {
            "Id": "1",
            "MessageBody": json.dumps(
                {
                    "order_id": "101",
                    "item": "Cappuccino",
                    "amount": 1,
                    "price": 3.50,
                }
            ),
        },
        {
            "Id": "1",  # Duplicate Batch ID (same as above)
            "MessageBody": json.dumps(
                {
                    "order_id": "101",
                    "item": "Croissant",
                    "amount": 1,
                    "price": 4.50,
                }
            ),
        },
    ]

    with pytest.raises(sqs_client.exceptions.BatchEntryIdsNotDistinct):
        sqs_client.send_message_batch(QueueUrl=queue_url, Entries=entries)
