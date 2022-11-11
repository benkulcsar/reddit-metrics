resource "aws_sns_topic" "reddit_lambda_errors" {
  name = "reddit-lambda-errors"
}

resource "aws_sns_topic_subscription" "reddit_lambda_errors_email_target" {
  topic_arn = aws_sns_topic.reddit_lambda_errors.arn
  protocol  = "email"
  endpoint  = var.MY_EMAIL
}
