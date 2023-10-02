# Introduction

One of the main motivation of designing this pipeline/project was to a beginner friendly introduction to AWS cloud, airflow and designign pipelines using multiple tools, develop new skills, and hopefully be helpful to many.

## How the pipeline works

There is one DAG (pipeline), when triggered extracts API data, make transformation and load it to Redshift and RDS. It is setup to extract data daily and store it in a CSV in S3 and then into the databases. 

This entire process is running with Apache Airflow (orchestration tool) running in a EC2 instance. This saves us having to manually setup Airflow in our local PC.  

Proceed to the next step to get started.

---

[Next Step](reddit.md)

or

[Back to main](https://github.com/rohitanumolu/zillow_rapidapi_aws_pipeline/tree/main)