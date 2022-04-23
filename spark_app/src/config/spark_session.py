import findspark
from pyspark import SparkConf

findspark.init('/usr/local/spark-3.1.2-bin-hadoop3.2')

from pyspark.sql import SparkSession

conf = SparkConf().setAll([
    ('spark.spark_app.name', 'SparkApp'),
    ('spark.executor.instances', 2),
    ('spark.executor.cores', '4'),
    ('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1')
])

# PySpark connector model
spark = SparkSession.builder.appName("CovidApp") \
    .master('local[*]') \
    .config(conf=conf) \
    .getOrCreate()
