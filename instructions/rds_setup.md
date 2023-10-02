# Setting up RDS database

1. Go to Amazon RDS and create a databse. Select PostgreSQL, Free tier, database identifier, username and password (remember what you give here), Instance db.t3.micro, storage as 1GB, Public access Yes and create new VPC security group (give a name). Create that databse (might take few minutes).
2. Go to EC2 security groups/inbound rules, add new role for type PostgreSQL and source anywhere IPv4 and save.
3. Once the rds database is ready, go inside, it and in Connectivity and security open the vp security group. Go to inbound rules and add new role for type PostgreSQL and source as anywhere IPv4. 
4. Install the postgresql client following the steps [here](https://www.postgresql.org/download/linux/ubuntu/) in EC2 from the terminal. Make sure you are in the virtual environment that you created.
5. Steps Import data from Amazon S3 into an RDS for PostgreSQL DB instance using a postgres client can be found [here](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PostgreSQL.S3Import.html). This is to access the database and query in it from your terminal. 
6. You need to provide RDS access to import data from S3. You can follow steps [here](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PostgreSQL.S3Import.html) to do it from terminal or do it in the online portal. First go to IAM/Roles and create new role. Select AWS Service and in use case RDS and choose RDS-Add role to database. Go next and add **AmazonS3FullAccess** policy, next give it a name and create. Now go back to RDS, manage IAM roles, add the role the you created and feature as s3Import.  
7. As you have already updated the dag file. You can see two tasks for RDS. One is to create an empty table if it doesnt exist. The other is to add the s3 data from bucket to RDS database. The tasks related to RDS and Redshift are grouped together. 
8. RDS task one is to create a table. We use PostgresOperator to connect to the RDS using the 'rds_postgres_conn' and run a query. So to create the table we provide the following query:
```bash
'''  
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
``` 
9. The step is to add the data from s3 bucket to rds after the table is created. The function 'aws_s3.table_import_from_s3' serves this purpose. The query for this is:
```bash
SELECT aws_s3.table_import_from_s3(
        'zillow_apidata', '', '(format csv, HEADER TRUE)',
        '<cleaned bucket name>','{{ti.xcom_pull("task_extract_zillow_data_rapidapi_to_S3")[1]}}', 'us-east-1'
    );
```
10. As you must have guessed, you need to the 'rds_postgres_conn' in airflow. Go to airflow, admin/connections and press the **+** mark to add new. Connection id is 'rds_postgres_conn', type postgres, host is rds data endpoint (you can copy it from opening RDS database and Endpoint & port in Connectivity & security). Login and password are what you provided while creating database, and port is 5432.


---

[Previous Step](redshift_setup.md) | [Next Step](final.md)

or

[Back to main](https://github.com/rohitanumolu/zillow_rapidapi_aws_pipeline/tree/main)