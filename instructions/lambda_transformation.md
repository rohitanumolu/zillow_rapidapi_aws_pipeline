# Cleaning raw data using AWS Lambda

1. Check if the raw API data has been uploaded to the S3 bucket. 
2. Go to AWS Lambda and create a new function. Select 'author from scratch', give a name and choose runtime as python. In 'Change default execution role', select an existing one and in new tab open IAM and create a new role. Select AWS service and in next section Lambda and press next. Now add **AmazonS3FullAccess** and **AWSLambdaBasicExecution**. Go next, give it a name and create the role. Go back to lambda function create and select this role created.
3. Open the created function and Add trigger. Select S3 and the bucket you created. In event types select 'All object create events' and ad the trigger.  
4. In the code section, copy paste the following [lambda_function.py](https://github.com/rohitanumolu/zillow_rapidapi_aws_pipeline/tree/main/lambda_function.py)
5. The cleaning is quite basic and nothing fancy. If you want to, you can clean/transform  the data according to your needs.
6. Go through the code and provide the target bucket name. For this create a new S3 bucket and provide the name of it here. 
7. Now in your Lambda function,sccroll down to the layers section and add a layer specifically **AWSSDKPandas-Python311**.
8. In the configuration section (besides code, test, monitor...), edit general configuration and increase the timeout to 2 minutes. As our data is small memory of 128 mb is sufficient but you can increase if you want to. 
9. So what this function does is, when ever a file is added to the raw s3 bucket, lambda is triggered which will the run the transformation job (code we provided) on that file and then save a new file in the new s3 bucket
10. Update your dag with the content of[zillow_pipeline_2.py](https://github.com/rohitanumolu/zillow_rapidapi_aws_pipeline/tree/main/archive/zillow_pipeline_2.py)  
11. We added a new task to check if the cleaned file is uploaded into the new S3 bucket (Provide the bucket name in S3_BUCKET variable).  
12. Now you need to create a connection from airflow to aws ('aws_conn_id'). To set this up, go to airflow, admin/connections and press the **+** mark to add new. Connection id is 'aws_conn_id', type is AWS, and copy paste the access and secret key which we downloaded previously for the user in [aws_services.md](aws_services.md) and save it.
13. When you now refresh the airflow, you see a new task in the graph section of the dag. You can now execute and check how the tasks are running. You can check logs to see what is happening, and errors in case if it failed. 


---

[Previous Step](extract_data.md) | [Next Step](redshift_setpu.md)

or

[Back to main](https://github.com/rohitanumolu/zillow_rapidapi_aws_pipeline/tree/main)