# Extracting data from API and loading to S3 bucket

1. Create a S3 bucket to store raw json data that we extract from API. 
2. As you are connected to EC2 in VS code, open the home folder. Here you can see different folders like airflow, virtual environment folder etc. 
3. Create a dags folder in airflow. This folder should contain all the dag files which can further see in airflow UI.
4. Create a new **.py** file in dags folder. Copy the content of [zillow_pipeline_1.py](https://github.com/rohitanumolu/zillow_rapidapi_aws_pipeline/tree/main/archive/zillow_pipeline_1.py)   
5. We created two task, one is to extract data from API to EC2 and second one is to move the file to S3 bucket created. 
6. Also make sure you add your bucket name in second task and then create a **config_api.json** in airflow folder with the RapidAPI key and host. 
> {
> 	"X-RapidAPI-Key": <Paste from RapidAPI code snippet>,
> 	"X-RapidAPI-Host": <Paste from RapidAPI code snippet>"
> }
7. Now when you refresh airflow UI (if closed, you can use airflow standalone to run again), this new dag with name **zillow_rapidapi_dag** should we available. 
8. Check the graph, code in UI and trigger it. This should start and then extract the data and load it into S3 bucket created.

---

[Previous Step](ec2_setup.md) | [Next Step](lambda_transformation.md)

or

[Back to main](https://github.com/rohitanumolu/zillow_rapidapi_aws_pipeline/tree/main)