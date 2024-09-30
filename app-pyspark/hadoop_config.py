from typing import TypedDict
import os


class AwsCredentialsNotPassedFromK8s(Exception):
    """Raised when AWS Credentails are not set as environmental Variables"""

    ...


AwsHadoopConfig = TypedDict(
    "AwsHadoopConfig",
    {
        "fs.s3n.awsAccessKeyId": str,
        "fs.s3n.awsSecretAccessKey": str,
        "fs.s3a.path.style.access": str,
        "fs.s3a.impl": str,
        "fs.s3a.endpoint": str,
    },
)


def export_hadoop_config() -> AwsHadoopConfig:

    try:
        AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY_ID"]
        AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
    except KeyError as e:
        raise AwsCredentialsNotPassedFromK8s(f"{e}: Unable to locate aws credentials.")

    hadoop_config = {
        "fs.s3n.awsAccessKeyId": AWS_ACCESS_KEY,
        "fs.s3n.awsSecretAccessKey": AWS_SECRET_ACCESS_KEY,
        "fs.s3a.path.style.access": "true",
        "fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
        "fs.s3a.endpoint": "s3.amazonaws.com",
    }

    return hadoop_config
