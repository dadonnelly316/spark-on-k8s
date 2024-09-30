
# todo: once i get a EKS cluster, do this - https://docs.aws.amazon.com/vpc/latest/privatelink/vpc-endpoints-s3.html#:~:text=Amazon%20S3%20supports%20both%20gateway,and%20with%20no%20additional%20cost.

# todo - how to make public by default for local testing?
resource "aws_s3_bucket" "lakehouse_storage" {
  bucket_prefix = "lakehouse-storage"

  tags = {
    Name        = "lakehouse-storage"
    Environment = "Prod"
  }
}