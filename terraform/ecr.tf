resource "aws_ecr_repository" "moderation_repo" {
  name                 = "${var.project_name}-repo-${var.environment}"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
  
  tags = {
    Name = "Content Moderation Repo"
  }
}

output "ecr_repository_url" {
  value = aws_ecr_repository.moderation_repo.repository_url
}
