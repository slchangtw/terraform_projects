# Lambda Powertools Batch Processing (SQS)

This example shows how to use AWS Lambda Powertools for Python to process SQS messages in batches using the `BatchProcessor` utility.

## Features

- Batch Processing: Automatically handles partial batch failures using `ReportBatchItemFailures`.
- SQS Integration: Triggered by an SQS queue.


## Deployment

```bash
terraform -chdir=terraform init
terraform -chdir=terraform apply
```

## Testing

Test sending a batch of valid and invalid orders. 
```bash
uv run pytest tests/send_batch_events.py
```


## Remove the infrastructure

```bash
terraform -chdir=terraform destroy
```
