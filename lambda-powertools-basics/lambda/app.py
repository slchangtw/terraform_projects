import json

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.parser import ValidationError, parse
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import BaseModel

logger = Logger(service="order-service")


class OrderDetails(BaseModel):
    order_id: str
    item: str
    amount: int
    price: float


def lambda_handler(event: OrderDetails, context: LambdaContext) -> dict:
    # Log the incoming event
    logger.info("Received event")
    try:
        event: OrderDetails = parse(model=OrderDetails, event=event)

        # Calculate total cost
        if event.amount <= 0 or event.price <= 0:
            raise ValueError("Amount and price must be greater than 0")

        total_cost = event.amount * event.price

        logger.info(
            f"Processing order {event.order_id}",
            extra={"item": event.item, "total_cost": total_cost},
        )

        # Construct success response
        response = {
            "message": "Order processed successfully",
            "order_id": event.order_id,
            "total_cost": total_cost,
            "status": "CONFIRMED",
        }

        return {"statusCode": 200, "body": json.dumps(response)}

    except ValidationError as e:
        logger.exception("Validation error", extra={"event": event})
        return {"statusCode": 400, "body": json.dumps({"message": str(e)})}
    except ValueError as e:
        logger.exception("Value error", extra={"event": event})
        return {"statusCode": 400, "body": json.dumps({"message": str(e)})}
    except Exception:
        logger.exception("Internal server error")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal processing error"}),
        }
