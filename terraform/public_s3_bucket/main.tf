resource "aws_s3_bucket" "tf_bucket_name" { 
  bucket = var.aws_bucket_name
  acl = "public-read"
  versioning { 
    enabled = false
  } 
  tags = { 
    "Name" = var.aws_bucket_name
  } 
}
resource "aws_s3_bucket_public_access_block" "tf_resource_name" {
  bucket = aws_s3_bucket.public-keys-bucket.id
  block_public_acls   = false
  block_public_policy = false
}