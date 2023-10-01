# Zillow ETL Pipeline 

This data pipeline is created to extract Zillow data from [RapidAPI](https://rapidapi.com/s.mahmoud97/api/zillow56/).

The data is extracted from the API using python and then loaded into an AWS S3 bucket as a bronze layer. The data was then cleaned/transformed using AWS Lambda to a new S3 bucket as a silver layer. The transformed data is then loaded into AWS Redshift for reporting and also loaded into AWS RDS (Postgres) for future projects. The whole process is orchestrated using Airflow in AWS EC2 instance.  

## Motivation
The project was implented to interlink different cloud services in AWS in a single pipeline and develop skills and experience. Another important point is to a create a comprehensive beginner friendly tutorial to create such pipelines. The similar project can implemented in different styles, difficulties using various other tools available. 

## Architecture


1. Extract zillow data using [RapidAPI](https://rapidapi.com/s.mahmoud97/api/zillow56/)
2. Load the bronze layer (raw) of data into [AWS S3](https://aws.amazon.com/s3/)
3. Utilize [AWS Lambda](https://aws.amazon.com/lambda/) to clean the raw data and load it into a new [AWS S3](https://aws.amazon.com/s3/) bucket.
4. Load the cleaned data into [AWS Redshift](https://aws.amazon.com/redshift/) for reporting.
5. Load the cleaned data also into [Amazon RDS](https://aws.amazon.com/rds/) for future projects. 
6. Orchestrate with [Airflow](https://airflow.apache.org) in [Amazon EC2](https://aws.amazon.com/ec2/instance-types/).





