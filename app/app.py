from pipelines.manage_covid_database import (get_covid_data,
                                             save_covid_data)
from pipelines.publish_data_to_mongo import (publish_covid_dataset,
                                             publish_total_new_cases_chart_data,
                                             publish_total_new_deaths_chart_data)


if __name__ == "__main__":
    dataset = get_covid_data()
    save_covid_data(dataset)

    publish_covid_dataset()

    publish_total_new_cases_chart_data()
    publish_total_new_deaths_chart_data()
