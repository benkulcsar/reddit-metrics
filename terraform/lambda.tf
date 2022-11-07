resource "aws_lambda_function" "reddit_extract_lambda" {
  filename         = "../extract_lambda.zip"
  function_name    = "reddit-extract"
  role             = aws_iam_role.reddit_extract_lambda_role.arn
  handler          = "extract.lambda_handler"
  runtime          = "python3.9"
  timeout          = "900"
  source_code_hash = filebase64sha256("../extract_lambda.zip")
  memory_size      = 256

  ephemeral_storage {
    size = 512
  }

  environment {
    variables = {
      TF_VAR_REDDIT_CLIENT_ID     = var.REDDIT_CLIENT_ID
      TF_VAR_REDDIT_CLIENT_SECRET = var.REDDIT_CLIENT_SECRET
      TF_VAR_REDDIT_S3_BUCKET     = var.REDDIT_S3_BUCKET
    }
  }
}
