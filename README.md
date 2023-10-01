# Zillow ETL Pipeline 

This data pipeline is created to extract Zillow data from [RapidAPI](https://rapidapi.com/s.mahmoud97/api/zillow56/).

The data is extracted from the API using python and then loaded into an AWS S3 bncket as a bronze layer. The data was then cleaned/transformed using AWS Lambda to a new S3 bucket as a silver layer. The transformed data is then loaded into AWS Redshift for reporting and also loaded into AWS RDS (Postgres) for future projects. The whole process is orchestrated using Airflow in AWS EC2 instance.  














A pipeline to gather data from RapidAPI-Zillow, clean and transform them in Lambda, and load them to redshift for BI reporting and RDS for future products. The whole pipeline is orchestrated using Airflow in EC2
