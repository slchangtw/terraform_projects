from pydantic import BaseModel


class OrderDetails(BaseModel):
    order_id: str
    item: str
    amount: int
    price: float


class OrderResponse(BaseModel):
    order_id: str
    total_cost: float
    status: str
