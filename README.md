# Weather API Workflow with Apache Airflow

## Project Overview

This project involves creating an automated ETL (Extract, Transform, Load) pipeline to fetch weather data from an API, process and store it in CSV format using Python and Pandas, and finally load it into an Amazon S3 bucket. Apache Airflow is used to orchestrate and automate the workflow, while EC2 instances are used for hosting the Airflow scheduler and workers.

## Components

1. **Weather API**: Source of weather data.
2. **Python**: Used for data extraction and transformation.
3. **Apache Airflow**: Orchestration tool for managing the ETL workflow.
4. **EC2 Instances**: Hosts the Airflow scheduler and workers.
5. **Pandas**: Python library used to process and store the data in CSV format.
6. **Amazon S3**: Storage service where the processed data is stored.

### Weather API Key 

**Obtain Weather API Key**:
    - Sign up at [OpenWeatherMap](https://openweathermap.org/) to get your API key.
    - Follow the instructions to create an account and generate an API key.

## Airflow's workflow

![Airflow UI](https://github.com/raghul3/Airflow_project_weather_api/assets/81759525/83926570-e291-4b47-8730-d3b1482ca002)

![Weather API Workflow Architecture](https://github.com/raghul3/Airflow_project_weather_api/assets/81759525/746893b5-21e2-418d-921e-17fd2a19cdc5)

## Architecture Diagram

![Architecture](https://github.com/raghul3/Airflow_project_weather_api/assets/81759525/c373927b-92a0-4b00-99de-dbf9aab56097)

