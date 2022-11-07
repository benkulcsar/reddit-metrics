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
