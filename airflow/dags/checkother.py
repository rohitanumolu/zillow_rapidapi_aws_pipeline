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

with DAG('zillow_rapidapi_dag2',
        default_args=default_args,
        dagrun_timeout=timedelta(seconds=200),
        schedule_interval = '@daily',
        catchup=False) as dag:

        is_cleaned_file_available_s3 = S3KeySensor(
        task_id='task_is_cleaned_file_available_S3',
        bucket_key='response_data_01102023215404.csv',
        bucket_name=S3_BUCKET,
        aws_conn_id='aws_s3_conn',
        wildcard_match=False,  # Set this to True if you want to use wildcards in the prefix
        timeout=60,  # Optional: Timeout for the sensor (in seconds)
        poke_interval=5,  # Optional: Time interval between S3 checks (in seconds)
        )

        create_table_rds = PostgresOperator(
                    task_id='task_create_rds_table',
                    postgres_conn_id = "rds_postgres_conn",
                    sql= '''  
                        CREATE TABLE IF NOT EXISTS zillow_apidata(
                        bathrooms NUMERIC NULL,
                        bedrooms NUMERIC NULL,
                        homeType VARCHAR(255) NULL,
                        homeStatus VARCHAR(255) NULL,
                        city VARCHAR(255) NULL,
                        latitude NUMERIC NULL,
                        longitude NUMERIC NULL,
                        lotAreaUnit VARCHAR(255) NULL,
                        lotAreaValue NUMERIC NULL,
                        livingArea NUMERIC NULL,
                        price NUMERIC NULL,
                        rentZestimate NUMERIC NULL,
                        zipcode INT NULL
                    );
                    '''
                )

        cleaned_s3_to_redshift = S3ToRedshiftOperator(
                    task_id="task_cleaned_s3_to_redshift",
                    aws_conn_id='aws_s3_conn',
                    redshift_conn_id='reddshift_conn',
                    s3_bucket=S3_BUCKET,
                    s3_key='response_data_01102023215404', ###filename
                    schema="public",
                    table="zillow_apidata",
                    copy_options=["csv IGNOREHEADER 1"],
                )

        upload_3_to_rds_postgres  = PostgresOperator(
                    task_id = "task_upload_S3_to_rds_postgres",
                    postgres_conn_id = "rds_postgres_conn",
                    sql = '''
                            SELECT aws_s3.table_import_from_s3(
                            'zillow_apidata', '', '(format csv, HEADER TRUE)',
                            'zillow-rapidapi-data-cleaned','response_data_01102023230936.csv', 'us-east-1'
                            );
                    '''
                )

        end_pipeline = DummyOperator(
                task_id = 'task_end_pipeline'
        )

        # with TaskGroup(group_id = 'grouped', tooltip= "Loading_to_RDS_Redshift") as grouped:
        #         create_table_rds = PostgresOperator(
        #             task_id='task_create_rds_table',
        #             postgres_conn_id = "rds_postgres_conn",
        #             sql= '''  
        #                 CREATE TABLE IF NOT EXISTS zillow_apidata(
        #                 bathrooms INT NULL,
        #                 bedrooms NUMERIC NULL,
        #                 homeType VARCHAR(255) NULL,
        #                 homeStatus VARCHAR(255) NULL,
        #                 city VARCHAR(255) NULL,
        #                 latitude NUMERIC NULL,
        #                 longitude NUMERIC NULL,
        #                 lotAreaUnit VARCHAR(255) NULL,
        #                 lotAreaValue NUMERIC NULL,
        #                 livingArea NUMERIC NULL,
        #                 price NUMERIC NULL,
        #                 rentZestimate NUMERIC NULL,
        #                 zipcode INT NULL
        #             );
        #             '''
        #         )

        #         # upload_3_to_rds_postgres  = PostgresOperator(
        #         #     task_id = "task_upload_S3_to_rds_postgres",
        #         #     postgres_conn_id = "rds_postgres_conn",
        #         #     sql = '''
        #         #             SELECT aws_s3.table_import_from_s3(
        #         #             'zillow_apidata', '', '(format csv)',
        #         #             'zillow-rapidapi-data-cleaned','response_data_01102023215404.csv', 'us-east-1'
        #         #             );
        #         #     '''
        #         # )

        #         cleaned_s3_to_redshift = S3ToRedshiftOperator(
        #             task_id="task_cleaned_s3_to_redshift",
        #             aws_conn_id='aws_s3_conn',
        #             redshift_conn_id='reddshift_conn',
        #             s3_bucket=S3_BUCKET,
        #             s3_key='response_data_01102023215404.csv', ###filename
        #             schema="PUBLIC",
        #             table="zillow_apidata",
        #             copy_options=["csv IGNOREHEADER 1"],
        #         )

                
        #         create_table_rds >> 
                
                

        is_cleaned_file_available_s3 >> cleaned_s3_to_redshift >> upload_3_to_rds_postgres>> end_pipeline