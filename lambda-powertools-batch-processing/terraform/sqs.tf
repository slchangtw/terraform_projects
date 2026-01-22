resource "aws_sqs_queue" "dlq" {
  name = "batch-processing-dlq"
}

resource "aws_sqs_queue" "main_queue" {
  name = "batch-processing-queue"
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.dlq.arn
    maxReceiveCount     = 2
  })
}
