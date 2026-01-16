from pydantic import BaseModel, Field


class OrderDetails(BaseModel):
    order_id: str
    item: str
    amount: int = Field(gt=0)
    price: float = Field(gt=0)


class OrderResponse(BaseModel):
    order_id: str
    total_cost: float
    status: str
