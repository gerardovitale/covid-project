from pyspark.sql import SparkSession

from config.mongo_uri import MONGODB_URI_COVID_DEATHS
from config.spark_session import spark


def collect_total_new_cases():
    covid_deaths = spark.read.format('mongo')\
                             .option('uri', MONGODB_URI_COVID_DEATHS)\
                             .load()
    covid_deaths.createOrReplaceTempView('mongo_covid_deaths')
    total_new_cases_per_month_and_country = spark.sql('''
        SELECT YEAR(date) as year, MONTH(date) as month, location, 
            SUM(new_cases) as total_new_cases
        FROM mongo_covid_deaths
        WHERE continent IS NOT NULL
        GROUP BY location, YEAR(date), MONTH(date)
        ORDER BY location, YEAR(date), MONTH(date)
    ''')
    
    return total_new_cases_per_month_and_country

