resource "aws_cloudwatch_dashboard" "orders_dashboard" {
  dashboard_name = "OrderServiceDashboard"

  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        x      = 0
        y      = 0
        width  = 12
        height = 6
        properties = {
          metrics = [
            ["order-service", "SuccessfulOrders", "service", "order-service", { stat = "Sum", period = 300 }]
          ]
          view    = "timeSeries"
          stacked = false
          region  = "eu-central-1"
          title   = "Successful Orders Count"
        }
      }
    ]
  })
}