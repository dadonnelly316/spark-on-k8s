from typing import TypedDict
import os

# https://github.com/apache/hadoop/blob/trunk/hadoop-tools/hadoop-aws/src/site/markdown/tools/hadoop-aws/index.md
# https://hadoop.apache.org/docs/stable/hadoop-aws/tools/hadoop-aws/index.html


class AwsCredentialsNotPassedFromK8s(Exception):
    """Raised when AWS Credentails are not set as environmental variables"""

    ...


AwsHadoopConfig = TypedDict(
    "AwsHadoopConfig",
    {
        "fs.s3a.access.key": str,
        "fs.s3a.secret.key": str,
        "fs.s3a.impl": str,
        "fs.s3a.endpoint": str,
        "fs.s3a.path.style.access": str,
    },
)


# todo: check why this isn't showing as a type error when key isn't present in TypedDict
# todo: AWS secrets should probably get mounted into secrets file ~/.aws/credentials
# todo: make class that takes in this config. It comes with functions to generate path to write to s3
def export_hadoop_config() -> AwsHadoopConfig:

    try:
        AWS_ACCESS_KEY = os.environ["AWS_ACCESS_KEY_ID"]
        AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
    except KeyError as e:
        raise AwsCredentialsNotPassedFromK8s(f"{e}: Unable to locate aws credentials.")

    hadoop_config = {
        "fs.s3a.access.key": AWS_ACCESS_KEY,
        "fs.s3a.secret.key": AWS_SECRET_ACCESS_KEY,
        "fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
        "fs.s3a.endpoint": "s3.amazonaws.com",
        "fs.s3a.path.style.access": "true",
    }

    return hadoop_config
