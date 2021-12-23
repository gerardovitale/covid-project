from pyspark.sql.functions import to_timestamp

from src.config.spark_session import spark
from src.config.mongo_config import MONGODB_URI

from src.pipelines.load.collect_data_to_plot import collect_total_new_cases, collect_total_new_deaths
from src.resources.time_it import time_it


@time_it
def publish_covid_data_to_mongo() -> None:
    covid_df = spark.read.parquet('data/covid_dataset.parquet',
                                  inferSchema=True,
                                  header=True)
    covid_df = covid_df.withColumn('date', to_timestamp(covid_df.date))
    covid_df.write.format('mongo') \
        .mode('append') \
        .option('uri', MONGODB_URI) \
        .option('database', 'covid-project') \
        .option('collection', 'covid_dataset') \
        .save()


@time_it
def publish_total_new_cases_chart_data() -> None:
    total_new_cases = collect_total_new_cases()
    total_new_cases.write.format('mongo') \
        .mode('append') \
        .option('uri', MONGODB_URI) \
        .option('database', 'covid-project') \
        .option('collection', 'total_new_cases_chart_data') \
        .save()


@time_it
def publish_total_new_deaths_chart_data() -> None:
    total_new_cases = collect_total_new_deaths()
    total_new_cases.write.format('mongo') \
        .mode('append') \
        .option('uri', MONGODB_URI) \
        .option('database', 'covid-project') \
        .option('collection', 'total_new_deaths_chart_data') \
        .save()
