locals {
  reddit_repos = {
    extract : { repo_name : "reddit-extract" },
    transform : { repo_name : "reddit-transform" },
    load : { repo_name : "reddit-load" }
  }
}

resource "aws_ecr_repository" "reddit_repos" {
  for_each             = local.reddit_repos
  name                 = each.value.repo_name
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = false
  }
}

data "aws_ecr_image" "reddit_images" {
  for_each        = local.reddit_repos
  repository_name = each.value.repo_name
  image_tag       = "latest"
}
