resource "aws_ecr_repository" "reddit_extract" {
  name                 = "reddit-extract"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}

data "aws_ecr_image" "reddit_extract_image" {
  repository_name = aws_ecr_repository.reddit_extract.name
  image_tag       = "latest"
}

resource "aws_ecr_repository" "reddit_transform" {
  name                 = "reddit-transform"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}

data "aws_ecr_image" "reddit_transform_image" {
  repository_name = aws_ecr_repository.reddit_transform.name
  image_tag       = "latest"
}


resource "aws_ecr_repository" "reddit_load" {
  name                 = "reddit-load"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}

data "aws_ecr_image" "reddit_load_image" {
  repository_name = aws_ecr_repository.reddit_load.name
  image_tag       = "latest"
}
