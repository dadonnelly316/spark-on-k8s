from config_hadoop import get_hadoop_s3a_client_aws_config
from pyspark.sql import SparkSession
from datetime import date, datetime
import os

# todo: better error handling if environ isn't found
S3_BUCKET_NAME = os.environ["S3_BUCKET_NAME"]


def set_hadoop_config(spark_session: SparkSession) -> None:

    s3a_hadoop_config = get_hadoop_s3a_client_aws_config()
    sc_hadoop_config = spark_session._jsc.hadoopConfiguration()

    for config_key, config_value in s3a_hadoop_config.items():
        sc_hadoop_config.set(config_key, config_value)


def main() -> None:
    spark = SparkSession.builder.getOrCreate()

    try:
        set_hadoop_config(spark)

        df = spark.createDataFrame(
            [
                (1, 2.0, "string1", date(2000, 1, 1), datetime(2000, 1, 1, 12, 0)),
                (2, 3.0, "string2", date(2000, 2, 1), datetime(2000, 1, 2, 12, 0)),
                (3, 4.0, "string3", date(2000, 3, 1), datetime(2000, 1, 3, 12, 0)),
            ],
            schema="a long, b double, c string, d date, e timestamp",
        )

        output_folder = "spark_test"
        df.write.parquet(f"s3a://{S3_BUCKET_NAME}/{output_folder}", mode="overwrite")

        df.show()
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
