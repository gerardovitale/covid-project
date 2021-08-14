from notebooks.resources.update_local_data import (get_covid_data,
                                                   rearrenge_data)

from pipelines.publish_data_to_mongo import (publish_covid_deaths,
                                             publish_covid_vaccination,
                                             publish_total_new_cases_chart_data)


if __name__ == "__main__":
    get_covid_data()
    rearrenge_data()

    publish_covid_deaths()
    publish_covid_vaccination()

    publish_total_new_cases_chart_data()
