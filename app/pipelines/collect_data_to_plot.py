from pyspark.sql import DataFrame

from config.mongo_config import MONGODB_URI_COVID
from config.spark_session import spark
from pipelines.resources.time_it import time_it


@time_it
def collect_total_new_cases() -> DataFrame:
    covid_df = spark.read.format('mongo')\
                         .option('uri', MONGODB_URI_COVID)\
                         .load()
    covid_df.createOrReplaceTempView('mongo_covid')
    total_new_cases = spark.sql('''
        SELECT YEAR(date) as year, MONTH(date) as month, 
            location, SUM(new_cases) as total_new_cases
        FROM mongo_covid
        WHERE continent IS NOT NULL
        GROUP BY location, YEAR(date), MONTH(date)
        ORDER BY location, YEAR(date), MONTH(date)
    ''')
    return total_new_cases


@time_it
def collect_total_new_deaths() -> DataFrame:
    covid_df = spark.read.format('mongo') \
                         .option('uri', MONGODB_URI_COVID) \
                         .load()
    covid_df.createOrReplaceTempView('mongo_covid')
    total_new_deaths = spark.sql('''
        SELECT YEAR(date) as year, MONTH(date) as month, 
            location, SUM(new_deaths) as total_new_deaths
        FROM mongo_covid
        WHERE continent IS NOT NULL
        GROUP BY location, YEAR(date), MONTH(date)
        ORDER BY location, YEAR(date), MONTH(date)
    ''')
    return total_new_deaths
