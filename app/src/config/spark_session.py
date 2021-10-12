import findspark
findspark.init('/usr/local/spark-3.1.2-bin-hadoop3.2')

from pyspark.sql import SparkSession


# PySpark connector model
spark = SparkSession.builder.appName("CovidApp") \
                    .config("spark.jars.packages",
                            "org.mongodb.spark:mongo-spark-connector_2.12:3.0.1",)\
                    .getOrCreate()
