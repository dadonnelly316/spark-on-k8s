from typing import Dict


def get_spark_config_iceberg(
    default_namespace: str, catalog_name: str = "iceberg"
) -> Dict[str, str]:

    # todo: hive.metastore.uris points to ClusterIP of HMS service. This should be passed in dynamtically since it can change
    spark_config = {
        "hive.metastore.uris": "thrift://10.108.142.128:9083",
        "spark.sql.catalogImplementation": "hive",
        "spark.sql.storeAssignmentPolicy": "ansi",
        "spark.sql.extensions": "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
        f"spark.sql.catalog.{catalog_name}": "org.apache.iceberg.spark.SparkCatalog",  # SparkCatalog, SparkSessionCatalog
        f"spark.sql.catalog.{catalog_name}.warehouse": "s3a://lakehouse-storage20240929210918549500000001/warehouse",
        f"spark.sql.catalog.{catalog_name}.uri": "thrift://10.108.142.128:9083",
        f"spark.sql.catalog.{catalog_name}.io-impl": "org.apache.iceberg.aws.s3.S3FileIO",
        f"spark.sql.catalog.{catalog_name}.type": "hive",
        f"spark.sql.catalog.{catalog_name}.default-namespace": default_namespace,
    }

    return spark_config
