import json
import requests
from airflow import DAG
from datetime import timedelta, datetime
from airflow.operators.python import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.task_group import TaskGroup

# Load JSON config file
with open('/home/ubuntu/airflow/config_api.json', 'r') as config_file:
    API_KEY = json.load(config_file)

DT_STRING = datetime.now().strftime("%d%m%Y%H%M%S")

S3_BUCKET='zillow-rapidapi-data-cleaned'

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
            bash_command = 'aws s3 mv {{ ti.xcom_pull("task_extract_zillow_data_rapidapi_to_S3")[0]}} s3://zillow-rapidapi-data-raw/',
        )

        is_cleaned_file_available_s3 = S3KeySensor(
        task_id='task_is_cleaned_file_available_S3',
        bucket_key='{{ti.xcom_pull("task_extract_zillow_data_rapidapi_to_S3")[1]}}',
        bucket_name=S3_BUCKET,
        aws_conn_id='aws_s3_conn',
        wildcard_match=False,  # Set this to True if you want to use wildcards in the prefix
        timeout=60,  # Optional: Timeout for the sensor (in seconds)
        poke_interval=5,  # Optional: Time interval between S3 checks (in seconds)
        )

        end_pipeline = DummyOperator(
                task_id = 'task_end_pipeline'
        )

        with TaskGroup(group_id = 'grouped', tooltip= "Loading_to_RDS_Redshift") as grouped:
                create_table_rds = PostgresOperator(
                    task_id='task_create_rds_table',
                    postgres_conn_id = "rds_postgres_conn",
                    sql= '''  
                        CREATE TABLE IF NOT EXISTS zillow_apidata(
                        bathrooms NUMERIC,
                        berooms NUMERIC,
                        homeType VARCHAR(255),
                        homeStatus VARCHAR(255),
                        city VARCHAR(255),
                        latitude NUMERIC,
                        longitude NUMERIC,
                        lotAreaUnit VARCHAR(255),
                        lotAreaValue NUMERIC,
                        livingArea NUMERIC,
                        price NUMERIC,
                        rentZestimate NUMERIC,
                        zipcode INT
                        );
                    '''
                )

                upload_3_to_rds_postgres  = PostgresOperator(
                    task_id = "task_upload_S3_to_rds_postgres",
                    postgres_conn_id = "rds_postgres_conn",
                    sql = '''
                                SELECT aws_s3.table_import_from_s3(
                                 'zillow_apidata', '', '(format csv, HEADER TRUE)',
                                 'zillow-rapidapi-data-cleaned','{{ti.xcom_pull("task_extract_zillow_data_rapidapi_to_S3")[1]}}', 'us-east-1'
                                );
                            '''
                )

                cleaned_s3_to_redshift = S3ToRedshiftOperator(
                    task_id="task_cleaned_s3_to_redshift",
                    aws_conn_id='aws_s3_conn',
                    redshift_conn_id='reddshift_conn',
                    s3_bucket=S3_BUCKET,
                    s3_key='{{ti.xcom_pull("task_extract_zillow_data_rapidapi_to_S3")[1]}}', ###filename
                    schema="PUBLIC",
                    table="zillow_apidata",
                    copy_options=["csv IGNOREHEADER 1"],
                )

                
                create_table_rds >> upload_3_to_rds_postgres
                cleaned_s3_to_redshift
                

        extract_zillow_data_rapidapi_s3 >> loading_to_bronze_s3 >> is_cleaned_file_available_s3 >> grouped >> end_pipeline