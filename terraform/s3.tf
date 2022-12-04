locals {
  lambda_permissions = {
    transform = { function_name = aws_lambda_function.reddit_transform_lambda.function_name },
    load      = { function_name = aws_lambda_function.reddit_load_lambda.function_name }
  }
}


resource "aws_s3_bucket" "reddit" {
  bucket = var.REDDIT_S3_BUCKET
}

resource "aws_s3_bucket_public_access_block" "example" {
  bucket = aws_s3_bucket.reddit.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "reddit" {
  bucket = aws_s3_bucket.reddit.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_lambda_permission" "allow_s3_invoke" {
  for_each = local.lambda_permissions

  statement_id  = "allow-s3-invoke-${each.key}"
  action        = "lambda:InvokeFunction"
  function_name = each.value.function_name
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::${aws_s3_bucket.reddit.id}"
}


resource "aws_s3_bucket_notification" "trigger_reddit_lambdas" {
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
