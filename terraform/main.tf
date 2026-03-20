terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# MISCONFIGURATION 1: S3 bucket with public access enabled
resource "aws_s3_bucket" "demo_bucket" {
  bucket = "my-demo-insecure-bucket"
}

resource "aws_s3_bucket_public_access_block" "demo_bucket" {
  bucket = aws_s3_bucket.demo_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

# MISCONFIGURATION 2: S3 bucket with no versioning
resource "aws_s3_bucket_versioning" "demo_bucket" {
  bucket = aws_s3_bucket.demo_bucket.id
  versioning_configuration {
    status = "Disabled"
  }
}

# MISCONFIGURATION 3: S3 bucket with no encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "demo_bucket" {
  bucket = aws_s3_bucket.demo_bucket.id
  # intentionally left empty — no encryption configured
}

# MISCONFIGURATION 4: Overly permissive IAM role
resource "aws_iam_role" "demo_role" {
  name = "demo-insecure-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action    = "*"
        Effect    = "Allow"
        Principal = "*"
      }
    ]
  })
}

# MISCONFIGURATION 5: Security group open to the world
resource "aws_security_group" "demo_sg" {
  name        = "demo-insecure-sg"
  description = "Demo security group"

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# MISCONFIGURATION 6: RDS instance with no encryption + publicly accessible
resource "aws_db_instance" "demo_db" {
  identifier        = "demo-insecure-db"
  engine            = "mysql"
  instance_class    = "db.t3.micro"
  allocated_storage = 20
  username          = "admin"
  password          = "password123"

  publicly_accessible = true
  storage_encrypted   = false
  skip_final_snapshot = true
}
