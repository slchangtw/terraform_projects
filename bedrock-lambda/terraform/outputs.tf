# API Gateway URL output
output "api_gateway_url" {
  description = "The URL of the API Gateway"
  value       = "https://${aws_api_gateway_rest_api.api.id}.execute-api.${data.aws_region.current.region}.amazonaws.com/${aws_api_gateway_stage.stage.stage_name}${aws_api_gateway_resource.resource.path}"
}
