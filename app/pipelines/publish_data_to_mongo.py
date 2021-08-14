from pyspark.sql import SparkSession
from pyspark.sql.functions import to_timestamp

from config.spark_session import spark
from config.mongo_uri import MONGODB_URI

from pipelines.collect_data_to_plot import collect_total_new_cases


def publish_covid_deaths() -> None:
    covid_deaths = spark.read.parquet('data/covid_deaths.parquet', 
                                      inferSchema=True, 
                                      header=True)
    covid_deaths = covid_deaths.withColumn('date', to_timestamp(covid_deaths.date))
    covid_deaths.write.format('mongo')\
                      .mode('append')\
                      .option('uri', MONGODB_URI)\
                      .option('database', 'covid-project')\
                      .option('collection', 'covid_deaths')\
                      .save()


def publish_covid_vaccination() -> None:
    covid_vaccinations = spark.read.parquet('data/covid_vaccinations.parquet', 
                                            inferSchema=True, 
                                            header=True)
    covid_vaccinations.write.format('mongo')\
                            .mode('append')\
                            .option('uri', MONGODB_URI)\
                            .option('database', 'covid-project')\
                            .option('collection', 'covid_vaccinations')\
                            .save()


def publish_total_new_cases_chart_data() -> None:
    total_new_cases = collect_total_new_cases()
    total_new_cases.write.format('mongo')\
                   .mode('append')\
                   .option('uri', MONGODB_URI)\
                   .option('database', 'covid-project')\
                   .option('collection', 'total_new_cases_chart_data')\
                   .save()