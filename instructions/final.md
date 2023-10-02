# Final run

1. Once you set up RDS and Redshift and update the dag file and navigate to your dag in Airflow UI and your graph of DAG should look like this (The image is after successful run of the dag. You might not see the green mark with success written): 

<img src="https://github.com/rohitanumolu/zillow_rapidapi_aws_pipeline/blob/main/images/dag.png" width=100% height=100%>

2. Trigger the dag now, and you should start to see it run. It should not take much long for a successful run. If you see any task failing, you can select it and go to lags and see what is the error and try to fix it.

3. To check if the data is added to Redshift, you can open the query editor and run the below script. It should give some number as output
```bash
select count(*)
from zillow_apidata
```

4. Similarly, to check if the data is added to RDS, you can connect to the RDS from the EC2 using (change the host name):
```bash
psql --host=111122223333.aws-region.rds.amazonaws.com --port=5432 --username=postgres --password
```
This should connect to to the database after providing the password and run the query and check the output.
```bash
select count(*)
from zillow_apidata
```

## Next Steps
* You can connect Redshift to PowerBI following steps [here]() and create a dashboard.
* You can further transform data in Redshift using [dbt](https://www.getdbt.com/). 