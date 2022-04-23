import sys

import pandas as pd

from src.config.spark_session import spark
from src.resources.remove_files import remove_files
from src.resources.time_it import time_it

COVID_FILE_NAME = 'covid_dataset'


@time_it
def save_covid_data_locally(df: pd.DataFrame) -> None:
    spark_df = spark.createDataFrame(df)
    try:
        remove_files([f'data/{COVID_FILE_NAME}.parquet'])
        spark_df.write.parquet(f'data/{COVID_FILE_NAME}.parquet')
        print(f'[INFO] parquet files created: data/{COVID_FILE_NAME}.parquet')
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
