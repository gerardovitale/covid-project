import sys

import pandas as pd

from config.spark_session import spark
from pipelines.resources.remove_files import remove_files
from pipelines.resources.time_it import time_it
from pipelines.transform.transform_covid_dataset import COVID_FILE_NAME


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
