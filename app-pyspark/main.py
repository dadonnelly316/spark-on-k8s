from hadoop_config import export_hadoop_config
from pyspark.sql import SparkSession
from datetime import date, datetime


def set_hadoop_config(spark_session: SparkSession) -> None:

    aws_hadoop_config = export_hadoop_config()
    sc_hadoop_config = spark_session._jsc.hadoopConfiguration()

    for hadoop_key, hadoop_value in aws_hadoop_config.items():
        sc_hadoop_config.set(hadoop_key, hadoop_value)


def main() -> None:
    spark = SparkSession.builder.getOrCreate()
    set_hadoop_config(spark)

    try:
        df = spark.createDataFrame(
            [
                (1, 2.0, "string1", date(2000, 1, 1), datetime(2000, 1, 1, 12, 0)),
                (2, 3.0, "string2", date(2000, 2, 1), datetime(2000, 1, 2, 12, 0)),
                (3, 4.0, "string3", date(2000, 3, 1), datetime(2000, 1, 3, 12, 0)),
            ],
            schema="a long, b double, c string, d date, e timestamp",
        )

        df.show()
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
