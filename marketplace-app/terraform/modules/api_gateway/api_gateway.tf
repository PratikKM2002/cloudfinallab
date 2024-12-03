resource "aws_api_gateway_rest_api" "marketplace_api" {
  name        = var.api_name
  description = "API for the Marketplace application"
}

resource "aws_api_gateway_resource" "marketplace" {
  rest_api_id = aws_api_gateway_rest_api.marketplace_api.id
  parent_id   = aws_api_gateway_rest_api.marketplace_api.root_resource_id
  path_part   = "marketplace"
}

resource "aws_api_gateway_method" "get_marketplace" {
  rest_api_id   = aws_api_gateway_rest_api.marketplace_api.id
  resource_id   = aws_api_gateway_resource.marketplace.id
  http_method   = "GET"
  authorization = "NONE"
}

resource "aws_api_gateway_method" "post_marketplace" {
  rest_api_id   = aws_api_gateway_rest_api.marketplace_api.id
  resource_id   = aws_api_gateway_resource.marketplace.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "get_marketplace_integration" {
  rest_api_id             = aws_api_gateway_rest_api.marketplace_api.id
  resource_id             = aws_api_gateway_resource.marketplace.id
  http_method             = aws_api_gateway_method.get_marketplace.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${var.lambda_function_arn}/invocations"
}

resource "aws_api_gateway_integration" "post_marketplace_integration" {
  rest_api_id             = aws_api_gateway_rest_api.marketplace_api.id
  resource_id             = aws_api_gateway_resource.marketplace.id
  http_method             = aws_api_gateway_method.post_marketplace.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${var.lambda_function_arn}/invocations"
}

resource "aws_api_gateway_method" "delete_marketplace" {
  rest_api_id   = aws_api_gateway_rest_api.marketplace_api.id
  resource_id   = aws_api_gateway_resource.marketplace.id
  http_method   = "DELETE"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "delete_marketplace_integration" {
  rest_api_id             = aws_api_gateway_rest_api.marketplace_api.id
  resource_id             = aws_api_gateway_resource.marketplace.id
  http_method             = aws_api_gateway_method.delete_marketplace.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.region}:lambda:path/2015-03-31/functions/${var.lambda_function_arn}/invocations"

  depends_on = [aws_lambda_permission.delete_api_gateway_permission]
}

resource "aws_lambda_permission" "delete_api_gateway_permission" {
  statement_id  = "AllowAPIGatewayInvokeDelete"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_arn
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.marketplace_api.execution_arn}/*/DELETE/marketplace"
}

resource "aws_api_gateway_deployment" "marketplace_deployment" {
  depends_on = [
    aws_api_gateway_integration.get_marketplace_integration,
    aws_api_gateway_integration.post_marketplace_integration,
    aws_api_gateway_integration.delete_marketplace_integration
  ]
  rest_api_id = aws_api_gateway_rest_api.marketplace_api.id
}

resource "aws_api_gateway_stage" "marketplace_stage" {
  deployment_id = aws_api_gateway_deployment.marketplace_deployment.id
  stage_name    = "prod"
  rest_api_id   = aws_api_gateway_rest_api.marketplace_api.id
}

resource "aws_lambda_permission" "api_gateway_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_arn  # Use the passed Lambda function ARN
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.marketplace_api.execution_arn}/*/*"
}
