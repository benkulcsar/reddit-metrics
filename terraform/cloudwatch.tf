resource "aws_cloudwatch_log_subscription_filter" "reddit_extract_monitoring_subscription" {
  name            = "reddit_extract_monitoring_subscription"
  log_group_name  = "/aws/lambda/${aws_lambda_function.reddit_extract_lambda.function_name}"
  filter_pattern  = "ERROR"
  destination_arn = aws_lambda_function.reddit_monitoring_sns.arn
}

resource "aws_cloudwatch_log_subscription_filter" "reddit_transform_monitoring_subscription" {
  name            = "reddit_transform_monitoring_subscription"
  log_group_name  = "/aws/lambda/${aws_lambda_function.reddit_transform_lambda.function_name}"
  filter_pattern  = "ERROR"
  destination_arn = aws_lambda_function.reddit_monitoring_sns.arn
}

resource "aws_cloudwatch_log_subscription_filter" "reddit_load_monitoring_subscription" {
  name            = "reddit_load_monitoring_subscription"
  log_group_name  = "/aws/lambda/${aws_lambda_function.reddit_load_lambda.function_name}"
  filter_pattern  = "ERROR"
  destination_arn = aws_lambda_function.reddit_monitoring_sns.arn
}


resource "aws_lambda_permission" "allow_cloudwatch" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.reddit_monitoring_sns.function_name
  principal     = "logs.eu-west-1.amazonaws.com"
}
