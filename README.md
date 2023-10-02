# Zillow ETL Pipeline 

This data pipeline is created to extract Zillow data from [RapidAPI](https://rapidapi.com/s.mahmoud97/api/zillow56/).

The data is extracted from the API using python and then loaded into an AWS S3 bucket as a bronze layer. The data was then cleaned/transformed using AWS Lambda to a new S3 bucket as a silver layer. The transformed data is then loaded into AWS Redshift for reporting and also loaded into AWS RDS (Postgres) for future projects. The whole process is orchestrated using Airflow in AWS EC2 instance.  

## Motivation
The project was implented to interlink different cloud services in AWS in a single pipeline and develop skills and experience. Another important point is to a create a comprehensive beginner friendly tutorial to create such pipelines. The similar project can implemented in different styles, difficulties using various other tools available. 

## Architecture

<img src="https://github.com/rohitanumolu/zillow_rapidapi_aws_pipeline/blob/main/images/pipeline.png" width=90% height=80%>

1. Extract zillow data using [RapidAPI](https://rapidapi.com/s.mahmoud97/api/zillow56/)
2. Load the bronze layer (raw) of data into [AWS S3](https://aws.amazon.com/s3/)
3. Utilize [AWS Lambda](https://aws.amazon.com/lambda/) to clean the raw data and load it into a new [AWS S3](https://aws.amazon.com/s3/) bucket.
4. Load the cleaned data into [AWS Redshift](https://aws.amazon.com/redshift/) for reporting.
5. Load the cleaned data also into [Amazon RDS](https://aws.amazon.com/rds/) for future projects. 
6. Orchestrate with [Airflow](https://airflow.apache.org) in [Amazon EC2](https://aws.amazon.com/ec2/instance-types/).

## Final DAG
<img src="https://github.com/rohitanumolu/zillow_rapidapi_aws_pipeline/blob/main/images/dag.png" width=100% height=130%>

## Future steps

* Create a dashboard using [Looker](https://cloud.google.com/looker), [PowerBI](https://powerbi.microsoft.com/en-gb/) or [Google Data Studio](https://datastudio.google.com).
* Transform the data in Amazon Redshift using [dbt](https://www.getdbt.com)
* Create AWS resources with [Terraform](https://www.terraform.io) instead of manually creating them. 

## Setup

 I've tried to provide step-by-step instructions to setup and develop this pipeline. You can follow below steps to setup pipeline. Feel free to make improvements/changes.

> **NOTE**: The entire project was developed in a AWS EC2 instance (ubuntu). Technically, you would not need to install anything in your local PC. If you want to launch any other instance other than ubuntu, then you might need to change some commands. 

As AWS offer a free tier, this wouldn't cost you much. The minimum requirement for EC2 instance to run Airflow is **t2.medium** which would cost. From my experience developin this project, the instance ran for around 25-30 hours and it cost me less than a $. Redshift and RDS are not free (you can use the serverless options). More details about pricing will be updated soon. However, please check [AWS free tier](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all) limits, as this may change.

1. [Introduction](instructions/introduction.md)
2. [Setting up Rapid API](instructions/rapidapi_setup.md)
3. [AWS Services](instructions/aws_services.md)
4. [Setup EC2 and connect to it with VSCode (ssh)](instructions/ec2_setup.md)
5. [Extracting data from API and loading to S3 bucket](instructions/extract_data.md)
6. [Cleaning raw data using AWS Lambda](instructions/lambda_transformation.md)
7. [Setting up redshift cluster](instructions/redshift_setup.md)
8. [Setting up RDS database](instructions/rds_setup.md)
9. [Final run](instructions/final.md)


