resource "aws_dynamodb_table" "order_idempotency_table" {
  name         = "OrderIdempotencyTable"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }

  ttl {
    attribute_name = "expiration"
    enabled        = true
  }
}
