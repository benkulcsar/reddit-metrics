resource "aws_s3_bucket" "reddit" {
  bucket = var.REDDIT_S3_BUCKET
}

resource "aws_s3_bucket_acl" "reddit" {
  bucket = aws_s3_bucket.reddit.id
  acl    = "private"
}

resource "aws_s3_bucket_versioning" "reddit" {
  bucket = aws_s3_bucket.reddit.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_lambda_permission" "allow_s3_invoke_transform" {
  statement_id  = "allow-s3-invoke-transform"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.reddit_transform_lambda.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::${aws_s3_bucket.reddit.id}"
}

resource "aws_lambda_permission" "allow_s3_invoke_load" {
  statement_id  = "allow-s3-invoke-load"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.reddit_load_lambda.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::${aws_s3_bucket.reddit.id}"
}

resource "aws_s3_bucket_notification" "trigger_reddit_reddit_lambdas" {
  bucket = aws_s3_bucket.reddit.id
  lambda_function {
    lambda_function_arn = aws_lambda_function.reddit_transform_lambda.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "reddit-posts/"
  }
  lambda_function {
    lambda_function_arn = aws_lambda_function.reddit_load_lambda.arn
    events              = ["s3:ObjectCreated:*"]
    filter_prefix       = "reddit-metrics/"
  }
}
