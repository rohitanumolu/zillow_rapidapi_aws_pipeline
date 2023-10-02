# AWS Services

Subscribe to [AWS free tier](https://aws.amazon.com/free/?all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all). 

We'll be using different AWS services including EC2, Lambda, S3, Redshift and RDS.

* [Amazon EC2](https://aws.amazon.com/ec2/instance-types/) provides secure, resizable compute capacity in the cloud. Instead of running our scripts, airflow, etc. in our local machine, we run it in these intances.

* [AWS Lambda](https://aws.amazon.com/lambda/) is a serverless compute service that lets you run code without provisioning or managing servers. We clean the raw data in S3 which comes from API and store it in a new S3 bucket. 

* [Simple Storage Service (S3)](https://aws.amazon.com/s3/) is an Object Storage. When we extract data from API, we'll store it in a json and push to an S3 Bucket as an object. This allows us to store all our raw data in the cloud. After Lambda transformation is done, the json is converted to CSV and saved in a new bucket. 

* [Redshift](https://aws.amazon.com/redshift/) is a Data Warehousing service. Utilising its Massively Parallel Processing (MPP) technology, Redshift is able to execute operations on large datasets at fast speeds. It's based on PostgreSQL, so we can use SQL to run operations here. We can store the data in this and use a reporting tool like Power BI, Looker, etc. 

* [Amazon RDS](https://aws.amazon.com/rds/) is a managed service that makes it easy to set up, operate, and scale a relational database in the cloud. We store the cleaned data in RDS for future projects. 

For this project, we can only use Postgres local (or in Docker) instead of cloud to make it easy. But, it is a good practive to work with cloud tools and get exposure. 

## Setup 
1. Setup your free tier [AWS account](https://aws.amazon.com/getting-started/guides/setup-environment/module-one/)

2. This step is not mandatory for this project but recommended. Setup/Create an IAM user which will have its own set of permissions (in this case, AdministratorAccess). Generally in production, you should only use the root account for tasks that can only be done with the root account. Save the credentials (you can download the .csv file while creating the user) and login as the IAM User. Steps to create a new user can be found [here](https://www.techtarget.com/searchcloudcomputing/tutorial/Step-by-step-guide-on-how-to-create-an-IAM-user-in-AWS). Make sure you select the correct policy (AdministratorAccess).

3. We will continue the setup in next instuction set. 

---

[Previous Step](rapidapi_setup.md) | [Next Step](ec2_setup.md)

or

[Back to main](https://github.com/rohitanumolu/zillow_rapidapi_aws_pipeline/tree/main)