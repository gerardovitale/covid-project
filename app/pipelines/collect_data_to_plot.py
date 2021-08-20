from pyspark.sql import DataFrame

from config.mongo_uri import MONGODB_URI_COVID
from config.spark_session import spark


def collect_total_new_cases() -> DataFrame:
    covid_df = spark.read.format('mongo')\
                         .option('uri', MONGODB_URI_COVID)\
                         .load()
    covid_df.createOrReplaceTempView('mongo_covid')
    total_new_cases_per_month_and_country = spark.sql('''
        SELECT YEAR(date) as year, MONTH(date) as month, 
            location, SUM(new_cases) as total_new_cases
        FROM mongo_covid
        WHERE continent IS NOT NULL
        GROUP BY location, YEAR(date), MONTH(date)
        ORDER BY location, YEAR(date), MONTH(date)
    ''')
    return total_new_cases_per_month_and_country
