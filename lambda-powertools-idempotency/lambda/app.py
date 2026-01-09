import json
import os

from aws_lambda_powertools import Logger, Metrics, Tracer
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.idempotency import (
    DynamoDBPersistenceLayer,
    IdempotencyConfig,
    idempotent_function,
)
from aws_lambda_powertools.utilities.idempotency.serialization.pydantic import (
    PydanticSerializer,
)
from aws_lambda_powertools.utilities.parser import ValidationError, parse
from aws_lambda_powertools.utilities.typing import LambdaContext
from utils import OrderDetails, OrderResponse

logger = Logger()
metrics = Metrics()
tracer = Tracer()

dynamodb_persistence_store = DynamoDBPersistenceLayer(
    table_name=os.getenv("IDEMPOTENCY_TABLE_NAME")
)
idempotency_config = IdempotencyConfig(
    event_key_jmespath="order_id",
)


@tracer.capture_method
def calculate_total_cost(amount: int, price: float) -> float:
    if amount <= 0 or price <= 0:
        raise ValueError("Amount and price must be greater than 0")
    return amount * price


# The data_keyword_argument identifies the argument name that
# will be used for the idempotency key.
@idempotent_function(
    data_keyword_argument="order",
    persistence_store=dynamodb_persistence_store,
    config=idempotency_config,
    output_serializer=PydanticSerializer(model=OrderResponse),
)
def process_order(order: OrderDetails) -> OrderResponse:
    total_cost = calculate_total_cost(amount=order.amount, price=order.price)
    return OrderResponse(
        order_id=order.order_id, total_cost=total_cost, status="CONFIRMED"
    )


@tracer.capture_lambda_handler
@metrics.log_metrics
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    logger.info("Received event")
    try:
        order: OrderDetails = parse(model=OrderDetails, event=event)

        logger.info(
            f"Processing order {order.order_id}",
            extra={"item": order.item, "amount": order.amount, "price": order.price},
        )

        response = process_order(order=order)

        metrics.add_metric(name="SuccessfulOrders", value=1, unit=MetricUnit.Count)

        return {"statusCode": 200, "body": json.dumps(response.model_dump())}

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
