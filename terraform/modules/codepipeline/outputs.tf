output "pipeline_name" {
  value = aws_codepipeline.this.name
}

output "github_connection_arn" {
  value = aws_codestarconnections_connection.github.arn
}