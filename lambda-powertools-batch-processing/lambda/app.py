import json
from typing import Any

from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.batch import (
    BatchProcessor,
    EventType,
    process_partial_response,
)
from aws_lambda_powertools.utilities.data_classes.sqs_event import SQSRecord
from aws_lambda_powertools.utilities.parser import ValidationError, parse
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import BaseModel, Field

logger = Logger()
metrics = Metrics()
tracer = Tracer()
processor = BatchProcessor(event_type=EventType.SQS)


class OrderDetails(BaseModel):
    order_id: str
    item: str
    amount: int = Field(gt=0)
    price: float = Field(gt=0)


@tracer.capture_method
def record_handler(record: SQSRecord) -> dict:
    logger.info("Received record")
    try:
        payload: str = record.json_body

        order: OrderDetails = parse(model=OrderDetails, event=payload)
        logger.info(
            f"Processing order {order.order_id}",
            extra={"item": order.item, "amount": order.amount, "price": order.price},
        )
        total_cost = order.amount * order.price
        response = {
            "message": "Order processed successfully",
            "order_id": order.order_id,
            "total_cost": total_cost,
            "status": "CONFIRMED",
        }

        metrics.add_metric(name="SuccessfulOrders", value=1, unit=MetricUnit.Count)
        metrics.add_dimension(name="item", value=order.item)

        return {"statusCode": 200, "body": json.dumps(response)}
    except ValidationError as e:
        logger.exception("Validation error", extra={"payload": payload})
        return {"statusCode": 400, "body": json.dumps({"message": str(e)})}
    except Exception:
        logger.exception("Internal server error")
        return {
            "statusCode": 500,
            "body": json.dumps({"message": "Internal processing error"}),
        }


@tracer.capture_lambda_handler
@metrics.log_metrics
def lambda_handler(
    event: [dict[str, Any] | list[dict[str, Any]]], context: LambdaContext
):
    return process_partial_response(
        event=event, record_handler=record_handler, processor=processor, context=context
    )
