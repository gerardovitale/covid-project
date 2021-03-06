from pipelines.extract.extract_covid_dataset import get_covid_dataset
from pipelines.load.publish_data_to_mongo import publish_covid_data_to_mongo, publish_total_new_cases_chart_data, \
    publish_total_new_deaths_chart_data
from pipelines.load.save_data_locally import save_covid_data_locally
from pipelines.transform.transform_covid_dataset import manage_null_values, add_missing_january_records_mongodb


def launch_data_pipeline() -> None:
    covid_data = get_covid_dataset()
    covid_data = manage_null_values(covid_data)

    save_covid_data_locally(covid_data)

    publish_covid_data_to_mongo()
    add_missing_january_records_mongodb()

    publish_total_new_cases_chart_data()
    publish_total_new_deaths_chart_data()


if __name__ == "__main__":
    launch_data_pipeline()
