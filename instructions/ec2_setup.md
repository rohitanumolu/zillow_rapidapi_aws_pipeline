# Setup EC2 and connect to it with VSCode (ssh)

Steps to launch the instance:
1. Navigate to [EC2 console](https://console.aws.amazon.com/ec2/) and choose Launch instance.
2. Provide a name, description and choose Ubuntu as Amazon Machine Image (you can choose to select other images/OS but make sure you change commands while running in terminal accordingly)
3. Choose Instance type to be **t2.medium**. Though this is not free tier, this is minimum requirement to run airflow. 
4. Under Key pair (login), create a new key pair and download the .pem file.
5. Next to Network settings, choose Edit. Here select traffic from HTTPS and HTTP. We need to provide or open other ports for other servers which we will do later. 
6. Keep other sections default and Launch instance. It might take a minute or two for the instance to start running. 

## Connection to EC2 with VS Code

1. You can connect to the EC2 instance from your browser. Simple select the instance, choose connect and in the four options select EC2 instance Connect option annd press connect. A new tab opens connecting to EC2 instance. You can now run any bash commands that you want.
2. Though this is convenient, it is not so friendly especially when you want to create files (nano is not something, I prefer).
3. Connecting to VS Code, would provide several advantages (a very familiar and user friendlt development environment). The steps to do this can be found in this [blog]() - Upcoming.  

## Installing dependenices 

* Once you connect to the instance (open a terminal if in VS Code), run all the commands in [dependencies.txt](https://github.com/rohitanumolu/zillow_rapidapi_aws_pipeline/tree/main/dependencies.txt) to install all the dependencies needed to run the project. 

* In addition, we create a virtual environment to install and develop the entire project in. 
```bash
 python3 -m venv zillow_rapidapi_venv
 source zillow_rapidapi_venv/bin/activate
```

* If you ran all the commands, you installed airflow. To check if all is good, run
```bash
airflow standalone
```
Open your browser, copy the IP4 of EC2 instance and add **:8080** (airflow port) and open the link. This will not be successful because we did not open the 8080 port of the EC2 instance. 

* Open the port by following these steps. Select the instance in AWS portal, select security, security groups and Edit inbound rules. Add rule, custom TCP, port name 8080 and source Anywhere IP4. 

* Once this role is added, the airflow link (EC2_IP4:8080) should be loading. Provide the username and password (can be found in the terminal after running the command - airflow standalone)

* You can explore the airflow UI and check the default dags present.  


---

[Previous Step](aws_services.md) | [Next Step](extract_data.md)

or

[Back to main](https://github.com/rohitanumolu/zillow_rapidapi_aws_pipeline/tree/main)