import json
import requests
from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.python import PythonOperator
from airflow.operators.bash_operator import BashOperator

# Load JSON config file
with open('/home/ubuntu/airflow/config_api.json', 'r') as config_file:
    API_KEY = json.load(config_file)

DT_STRING = datetime.now().strftime("%d%m%Y%H%M%S")


def extract_zillow_data_rapidapi(**kwargs):
    url = kwargs['url']
    headers = kwargs['headers']
    querystring = kwargs['querystring']
    dt_string = kwargs['date_string']
    
    # getting the response
    response = requests.get(url, headers=headers, params=querystring)
    response_data = response.json()
    
    # Specify the output file path
    output_file_path = f"/home/ubuntu/response_data_{dt_string}.json"
    file_string = f'response_data_{dt_string}.csv'

    # Write the JSON response to a file
    with open(output_file_path, "w") as output_file:
        json.dump(response_data, output_file, indent=4) 

    output = [output_file_path, file_string]
    return output


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 30),
    'email': ['rohithanumolu@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(seconds=15)
}

with DAG('zillow_rapidapi_dag',
        default_args=default_args,
        schedule_interval = '@daily',
        catchup=False) as dag:

        extract_zillow_data_rapidapi_s3 = PythonOperator(
        task_id= 'task_extract_zillow_data_rapidapi_to_S3',
        python_callable=extract_zillow_data_rapidapi,
        op_kwargs={'url': 'https://zillow56.p.rapidapi.com/search', 'querystring': {"location":"atlanta, ga"}, 'headers': API_KEY, 'date_string': DT_STRING}
        )

        loading_to_bronze_s3 = BashOperator(
            task_id = 'task_load_to_bronze_s3',
            bash_command = 'aws s3 mv {{ ti.xcom_pull("task_extract_zillow_data_rapidapi_to_S3")[0]}} s3://<your bucket name>/',
        )

                

        extract_zillow_data_rapidapi_s3 >> loading_to_bronze_s3 