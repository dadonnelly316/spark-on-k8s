from typing import TypedDict
import os


class AwsCredentialsNotPassedFromK8s(Exception):
    """Raised when AWS Credentails are not set as environmental variables"""

    ...


hadoop_s3a_client_config = TypedDict(
    "AwsHadoopConfig",
    {
        "fs.s3a.access.key": str,
        "fs.s3a.secret.key": str,
        "fs.s3a.impl": str,
        "fs.s3a.endpoint": str,
        "fs.s3a.path.style.access": str,
        "fs.s3a.endpoint.region": str,
    },
)


# todo: check why this isn't showing as a type error when key isn't present in TypedDict
# todo: AWS secrets should probably get mounted into secrets file ~/.aws/credentials
# todo: make class that takes in this config. It comes with functions to generate path to write to s3
def get_hadoop_s3a_client_aws_config() -> hadoop_s3a_client_config:

    try:
        AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
        AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
    except KeyError as e:
        raise AwsCredentialsNotPassedFromK8s(f"{e}: Unable to locate aws credentials.")

    hadoop_config = {
        "fs.s3a.access.key": AWS_ACCESS_KEY_ID,
        "fs.s3a.secret.key": AWS_SECRET_ACCESS_KEY,
        "fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
        "fs.s3a.endpoint": "us.east-1.s3.amazonaws.com",
        "fs.s3a.path.style.access": "true",
        "fs.s3a.endpoint.region": "us-east-1",
    }

    return hadoop_config
