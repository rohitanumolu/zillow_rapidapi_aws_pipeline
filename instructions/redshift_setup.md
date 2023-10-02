# Setting up redshift cluster

1. Go to Amazon redshift. Create a cluster, give a identifier, node type as dc3.large and number of nodes is 1 (This might be free or not depending on your account, so remember to delete it after you are done with the project to not incur any costs). Give the cluster a admin user name and password. Create the cluster (It might take few minutes).
2. Open query editor 2. Press on the cluster name, connect to it using database username and password. Provide the database name (dev), username and password you provided while creating. 
3. Create a table by using the query below:
```bash
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
4. You can check if the table is created by the following query
```bash
select count(*)
from zillow_apidata
```
5. Also, we need to set inbound rules to access the redshift cluster from our EC2. Select the cluster, go to Properties/Network and security settings and open VPC security group. A new link will open and go to inbound rules in second section. Edit rules and add new one to allow all traffic from anywhere IP4.

6. The next step is to create a connection from airflow/ec2 to redshift. Go to airflow, admin/connections and press the **+** mark to add new. Connection id is 'redshift_conn', type amazon redshift, host is cluster endpoint (only till .com. Delete 5439/dev). Database is dev, User and password which were given while creating cluster, and port is 5439.

7. Update the dag with [zillow_rapidapi_pipeline.py](https://github.com/rohitanumolu/zillow_rapidapi_aws_pipeline/blob/main/airflow/dags/zillow_rapidapi_pipeline.py) but do not run it. 

8. Tasks are grouped for redshift and rds. For now check the task with S3ToRedshiftOperator to see what is happening ther. What is is doing is simply copying the csv data from bucket to the redshift table created. 


---

[Previous Step](lambda_transformation.md) | [Next Step](rds_setup.md)

or

[Back to main](https://github.com/rohitanumolu/zillow_rapidapi_aws_pipeline/tree/main)