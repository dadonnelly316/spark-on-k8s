from config_hadoop import get_hadoop_s3a_client_aws_config
from pyspark.sql import SparkSession
from config_spark import get_spark_config_iceberg
import os

# todo: better error handling if environ isn't found
S3_BUCKET_NAME = os.environ["S3_BUCKET_NAME"]


def set_hadoop_config(spark_session: SparkSession) -> None:

    hadoop_s3a_config = get_hadoop_s3a_client_aws_config()
    sc_hadoop_config = spark_session._jsc.hadoopConfiguration()

    for config_key, config_value in hadoop_s3a_config.items():
        sc_hadoop_config.set(config_key, config_value)


def main() -> None:

    catalog_name = "iceberg"
    default_namespace = "test_ns"

    spark = (
        SparkSession.builder.appName("test_iceberg_write")
        .config(
            map=get_spark_config_iceberg(
                default_namespace=default_namespace, catalog_name=catalog_name
            )
        )
        .enableHiveSupport()
        .getOrCreate()
    )

    try:
        set_hadoop_config(spark)

        spark.sql(f"CREATE NAMESPACE IF NOT EXISTS {catalog_name}.{default_namespace};")
        spark.sql(
            f"""
            CREATE TABLE IF NOT EXISTS {catalog_name}.{default_namespace}.pizza_test (
                id bigint,
                data string,
                category string)
            USING iceberg
            OPTIONS (
                'write.object-storage.enabled'=true, 
                'write.data.path'='s3a://lakehouse-storage20240929210918549500000001/warehouse',
                'write.format.default'='parquet'
            )
            PARTITIONED BY (category);
    
        """
        )

        spark.sql(
            f'INSERT INTO {catalog_name}.{default_namespace}.pizza_test VALUES (1, "Pizza", "orders");'
        )

        df_result = spark.read.format(f"iceberg").load(
            f"iceberg.{default_namespace}.pizza_test"
        )

        df_result.show()

    finally:
        spark.stop()


if __name__ == "__main__":
    main()


# interesting reads
# https://github.com/apache/iceberg/issues/7570
# https://github.com/apache/iceberg/issues/7574
# https://github.com/apache/iceberg/issues/10078 - explains my credentaials error
# https://stackoverflow.com/questions/49242563/hive-s3-error-no-filesystem-for-scheme-s3
# https://stackoverflow.com/questions/72620351/getting-error-when-querying-iceberg-table-via-spark-thrift-server-using-beeline
# https://www.waitingforcode.com/apache-spark-sql/writing-custom-external-catalog-listeners-apache-spark-sql/read
# https://www.dremio.com/blog/deep-dive-into-configuring-your-apache-iceberg-catalog-with-apache-spark/
# https://jaceklaskowski.gitbooks.io/mastering-spark-sql/content/spark-sql-ExternalCatalog.html
# https://iceberg.apache.org/docs/latest/spark-configuration/
# https://stackoverflow.com/questions/43874124/does-spark-sql-use-hive-metastore
# https://medium.com/@sarfarazhussain211/metastore-in-apache-spark-9286097180a4
# https://stackoverflow.com/questions/46740670/no-filesystem-for-scheme-s3-with-pyspark
# https://stackoverflow.com/questions/31980584/how-to-connect-spark-sql-to-remote-hive-metastore-via-thrift-protocol-with-no
# https://stackoverflow.com/questions/76014842/pyspark-read-iceberg-table-via-hive-metastore-onto-s3
# https://github.com/apache/hadoop/blob/trunk/hadoop-tools/hadoop-aws/src/site/markdown/tools/hadoop-aws/index.md
# https://hadoop.apache.org/docs/current/hadoop-aws/tools/hadoop-aws/index.html - this works for non aws equivalents
# https://github.com/apache/iceberg/blob/main/aws-bundle/build.gradle
# https://mvnrepository.com/artifact/software.amazon.awssdk/apache-client
# https://mvnrepository.com/artifact/software.amazon.awssdk/bundle THIS COMES WITH ICEBERG-AWS
# https://stackoverflow.com/questions/64214481/standalone-hive-metastore-with-iceberg-and-s3
