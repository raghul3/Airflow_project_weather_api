from airflow import DAG
from datetime import timedelta, datetime
from airflow.providers.http.sensors.http import HttpSensor
import json
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
import pandas as pd


def kelvin_to_fahrenheit(temp_in_kelvin):
    # Converts temperature from Kelvin to Fahrenheit
    temp_in_fahrenheit = (temp_in_kelvin - 273.15) * (9 / 5) + 32
    return temp_in_fahrenheit


def transform_load_data(task_instance):
    # Extracts the weather data from XCom, transforms it, and loads it to an S3 bucket
    data = task_instance.xcom_pull(task_ids="extract_weather_data")
    city = data["name"]
    weather_description = data["weather"][0]['description']
    temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp"])
    feels_like_farenheit = kelvin_to_fahrenheit(data["main"]["feels_like"])
    min_temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp_min"])
    max_temp_farenheit = kelvin_to_fahrenheit(data["main"]["temp_max"])
    pressure = data["main"]["pressure"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    time_of_record = datetime.utcfromtimestamp(data['dt'] + data['timezone'])
    sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
    sunset_time = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])

    # Create a dictionary with the transformed data
    transformed_data = {"City": city,
                        "Description": weather_description,
                        "Temperature (F)": temp_farenheit,
                        "Feels Like (F)": feels_like_farenheit,
                        "Minimun Temp (F)": min_temp_farenheit,
                        "Maximum Temp (F)": max_temp_farenheit,
                        "Pressure": pressure,
                        "Humidty": humidity,
                        "Wind Speed": wind_speed,
                        "Time of Record": time_of_record,
                        "Sunrise (Local Time)": sunrise_time,
                        "Sunset (Local Time)": sunset_time
                        }

    # Convert the dictionary to a DataFrame
    transformed_data_list = [transformed_data]
    df_data = pd.DataFrame(transformed_data_list)

    # Define AWS credentials
    aws_credentials = {"key": "xxxxxxxxxxxxx", "secret": "xxxxxxxxxxxxx", "token": "xxxxxxxxxxxxx"}

    # Generate a unique filename based on the current timestamp
    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H%M%S")
    dt_string = 'current_weather_data_portland_' + dt_string

    # Save the DataFrame to an S3 bucket
    df_data.to_csv(f"s3://weatherapiairflowbuckets3-yml/{dt_string}.csv", index=False, storage_options=aws_credentials)


# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 8),
    'email': ['myemail@domain.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=2)
}

# Define the DAG
with DAG('weather_dag',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:
    # Task to check if the weather API is available
    is_weather_api_ready = HttpSensor(
        task_id='is_weather_api_ready',
        http_conn_id='weathermap_api',
        endpoint='/data/2.5/weather?q=Portland&APPID=xxxxxxxxxxxxx'
    )

    # Task to extract weather data from the API
    extract_weather_data = SimpleHttpOperator(
        task_id='extract_weather_data',
        http_conn_id='weathermap_api',
        endpoint='/data/2.5/weather?q=Portland&APPID=xxxxxxxxxxxxx',
        method='GET',
        response_filter=lambda r: json.loads(r.text),
        log_response=True
    )

    # Task to transform and load the extracted data
    transform_load_weather_data = PythonOperator(
        task_id='transform_load_weather_data',
        python_callable=transform_load_data
    )

    # Define task dependencies
    is_weather_api_ready >> extract_weather_data >> transform_load_weather_data
