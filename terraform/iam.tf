resource "aws_iam_role" "reddit_lambda_role" {
  name               = "reddit-lambda-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
  inline_policy {
    name   = "log_and_access_s3"
    policy = data.aws_iam_policy_document.log_and_access_s3.json
  }
}

data "aws_iam_policy_document" "lambda_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

data "aws_iam_policy_document" "log_and_access_s3" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = ["*"]
  }
  statement {
    actions = [
      "s3:*",
      "s3-object-lambda:*"
    ]
    resources = [aws_s3_bucket.reddit.arn, "${aws_s3_bucket.reddit.arn}/*"]
  }
}


resource "aws_iam_role" "reddit_lambda_monitoring_sns_role" {
  name               = "reddit-lambda-monitoring-sns-role"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
  inline_policy {
    name   = "sns_publish"
    policy = data.aws_iam_policy_document.sns_publish.json
  }
}

data "aws_iam_policy_document" "sns_publish" {
  statement {
    actions   = ["sns:Publish"]
    resources = [aws_sns_topic.reddit_lambda_errors.arn]
  }
}
