import json

from aws_lambda_powertools import Logger, Metrics
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.parser import ValidationError, parse
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import BaseModel, Field

logger = Logger()
metrics = Metrics()


class OrderDetails(BaseModel):
    order_id: str
    item: str
    amount: int = Field(gt=0)
    price: float = Field(gt=0)


@metrics.log_metrics
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    logger.info("Received event")
    try:
        event: OrderDetails = parse(model=OrderDetails, event=event)

        # Calculate total cost
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

        metrics.add_metric(name="SuccessfulOrders", value=1, unit=MetricUnit.Count)
        metrics.add_dimension(name="item", value=event.item)
        metrics.add_metadata(key="request_id", value=context.aws_request_id)

        return {"statusCode": 200, "body": json.dumps(response)}

    except ValidationError as e:
        logger.exception("Validation error", extra={"event": event})
        return {"statusCode": 400, "body": json.dumps({"message": str(e)})}
    except Exception:
        logger.exception("Internal server error")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal processing error"}),
        }
