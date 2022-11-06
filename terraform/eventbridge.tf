locals {
  extract_schedule = "cron(10 * ? * * *)" # Waiting 10 minutes after the hour improves timestamp consistency
}

resource "aws_cloudwatch_event_rule" "reddit_extract_schedule" {
  name                = "reddit-extract-schedule"
  description         = "Schedule for Extract Lambda Function"
  schedule_expression = local.extract_schedule
}

resource "aws_cloudwatch_event_target" "schedule_reddit_extract_lambda" {
  rule      = aws_cloudwatch_event_rule.reddit_extract_schedule.name
  target_id = "reddit-extract"
  arn       = aws_lambda_function.reddit_extract_lambda.arn
}

resource "aws_lambda_permission" "allow_events_bridge_to_run_lambda" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.reddit_extract_lambda.function_name
  principal     = "events.amazonaws.com"
}
