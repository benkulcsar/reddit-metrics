resource "aws_lambda_function" "reddit_extract_lambda" {
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.reddit_extract.repository_url}@${data.aws_ecr_image.reddit_extract_image.image_digest}"
  function_name = "reddit-extract"
  role          = aws_iam_role.reddit_lambda_role.arn
  timeout       = "900"
  memory_size   = 256

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

resource "aws_lambda_function" "reddit_transform_lambda" {
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.reddit_transform.repository_url}@${data.aws_ecr_image.reddit_transform_image.image_digest}"
  function_name = "reddit-transform"
  role          = aws_iam_role.reddit_lambda_role.arn
  timeout       = "300"
  memory_size   = 256

  ephemeral_storage {
    size = 512
  }

  environment {
    variables = {
      TF_VAR_REDDIT_S3_BUCKET = var.REDDIT_S3_BUCKET
    }
  }
}
