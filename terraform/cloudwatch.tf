locals {
  reddit_log_filters = {
    extract   = { lambda_name = aws_lambda_function.reddit_extract_lambda.function_name },
    transform = { lambda_name = aws_lambda_function.reddit_transform_lambda.function_name },
    load      = { lambda_name = aws_lambda_function.reddit_load_lambda.function_name }
  }
}

resource "aws_cloudwatch_log_subscription_filter" "reddit_monitoring_subscriptions" {
  for_each        = local.reddit_log_filters
  name            = "reddit_${each.key}_monitoring_subscription"
  log_group_name  = "/aws/lambda/${each.value.lambda_name}"
  filter_pattern  = "ERROR"
  destination_arn = aws_lambda_function.reddit_monitoring_sns.arn
}

resource "aws_lambda_permission" "allow_cloudwatch" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.reddit_monitoring_sns.function_name
  principal     = "logs.eu-west-1.amazonaws.com"
}
