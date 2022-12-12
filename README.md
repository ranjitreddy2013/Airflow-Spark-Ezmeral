# Airflow-Spark-Ezmeral

Apache Airflow is use for defining and managing a Directed Acyclic Graph of tasks. Data engineers orchestrate and schedule data pipelines and set alert and retries when a task fails. 

This repo will go over the steps required to run Airflow DAGs on Ezmeral Data Fabric. I will focus on running a simple Spark DAG using SparkSubmitOperator in Airflow.

### Installing Airflow

Detail instructions can be found here - https://docs.datafabric.hpe.com/70/AdvancedInstallation/InstallingAirflow.html

#### Installation on a Server Node or Edge Node

##### On a node where you want to install Airflow, install mapr-airflow, mapr-airflow-webserver, and mapr-airflow-scheduler:
   ###### On Ubuntu:
        apt-get install mapr-airflow mapr-airflow-webserver mapr-airflow-scheduler 
   ##### On RHEL/CentOS:
        yum install mapr-airflow mapr-airflow-webserver mapr-airflow-scheduler 
   ##### On SLES:
        zypper install mapr-airflow mapr-airflow-webserver mapr-airflow-scheduler 
         Note that installations on Oracle Enterprise Linux (OEL) must be done by the root user.
##### Run configure.sh -R.
        /opt/mapr/server/configure.sh -R 
        
#### Installation on a Client Node
Airflow can be installed on a client node. The installation steps are the same as for a server node or edge node. However, after installation on a client node, you must manage all Airflow services manually. For example:

##### To manage the webserver:
       /opt/mapr/airflow/airflow-<version>/bin/airflow.sh [start|stop] webserver
##### To manage the scheduler:
       /opt/mapr/airflow/airflow-<version>/bin/airflow.sh [start|stop] scheduler

You can access Airflow web UI on https://<Data Fabric Node>:8780/home  Or login to Data Fabric MCS (https://<Data Fabric Node>:8443, after login, click on Services tab, find the AirflowWebserver service, click on it view the UI.
   
### Building the DAG
   A DAG is just a Python file used to organize tasks and set their execution context. DAGs do not perform any actual computation. Instead, tasks are the element of Airflow that actually "do the work" we want to be performed. And it is your job to write the configuration and organize the tasks in specific orders to create a complete data pipeline.

 ####  Step 1: Import modules
   Import Python dependencies needed for the workflow

```
   import airflow
    from datetime import timedelta
    from airflow import DAG
    from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator 
    from airflow.utils.dates import days_ago
   ```
   
  #### Step 2: Arguments
   Define default and DAG-specific arguments
```
default_args = {
    'owner': 'airflow',    
    #'start_date': airflow.utils.dates.days_ago(2),
    # 'end_date': datetime(),
    # 'depends_on_past': False,
    # 'email': ['airflow@example.com'],
    # 'email_on_failure': False,
    #'email_on_retry': False,
    # If a task fails, retry it once after waiting
    # at least 5 minutes
    #'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
```
   #### Step 3: Instantiate a DAG
   Give the DAG name, configure the schedule, and set the DAG settings:
   
   
   ```
   dag_spark = DAG(
        dag_id = "sparkoperator_demo",
        default_args=args,
        # schedule_interval='0 0 * * *',
        schedule_interval='@once',	
        dagrun_timeout=timedelta(minutes=60),
        description='use case of sparkoperator in airflow',
        start_date = airflow.utils.dates.days_ago(1)
)
```
   
   #### Step 4: Set the Tasks
   The next step is setting up the tasks  in the workflow. Here in the code, spark_submit_local code is a task created by instantiating.

```
    spark_submit_local = SparkSubmitOperator(
		application ='/home/mapr/basicsparksubmit.py' ,
		conn_id= 'spark_local', 
		task_id='spark_submit_task', 
		dag=dag_spark
		)
   ```
   
   #### Step 5: Setting up Dependencies
   Here we are setting up the dependencies or the order in which the tasks should be executed. Here are a few ways you can define dependencies between them:

```
    spark_submit_local

    if __name__ == "__main__":
    dag_spark.cli()
   ```
In the above code spark_submit_local will execute. There are no other tasks that it is dependent on.
   
   #### Step 6: Creating the connection

spark-submit script is used for submitting a Spark app to Data Fabric cluster. For example, running PySpark app sparksubmit_basic.py  is as follows:
   ```
   /opt/mapr/spark/spark-3.2.0/bin/spark-submit --master local[*] --name arrow-spark --queue root.default /home/mapr/sparksubmit_basic.py
   ```
   Creating the connection in airflow to connect the spark as shown in below. In the Airflow web ui, click on the Admin tab, select the connections, you will get a new window with options to add new connections. Click on "+" to create a new connection in Airflow to connect to Spark as shown below:
	![alt text](https://github.com/ranjitreddy2013/Airflow-Spark-Ezmeral/blob/main/connection/spark_yarn_connection.png)
   
   Enter desired conn id, select Ezmeral Spark as connection type, host as yarn, for extra, enter MAPR_TICKETFILE_LOCATION and other variables as shown in below example:
	
```
{"queue": "root.default", "master": "local[*]", "spark-home": "/opt/mapr/spark/spark-3.2.0/", "spark_binary": "spark-submit", "namespace": "default", "MAPR_TICKETFILE_LOCATION": "/tmp/maprticket_5000", "YARN_CONF_DIR": "/opt/mapr/hadoop/hadoop-2.7.6/etc/hadoop", "HADOOP_CONF_DIR": "/opt/mapr/hadoop/hadoop-2.7.6/etc/hadoop"}
```
	
   #### Step 7: Verifying the DAG tasks
Click on the "sparkoperator_demo" name in the DAG list and then select the graph view; as shown below, we have a task called spark_submit_task as shown below:
![alt text](https://github.com/ranjitreddy2013/Airflow-Spark-Ezmeral/blob/main/connection/sparkoperator_demo_graph.png)
	

Click on the task that will pop up a window with options. One of the options is "log", click on it to view the log. Here is a [sample log](https://github.com/ranjitreddy2013/Airflow-Spark-Ezmeral/blob/main/logs/sample_log).
	        
   ### Trigger the DAGs via REST API
   #### Step 1 - Enable the REST API
By default, airflow does not accept requests made to the API. However, it’s easy  to turn on:

Comment out the original line "auth_backend = airflow.api.auth.backend.deny_all" with "auth_backend = airflow.api.auth.backend.basic_auth" in the $AIRFLOW_HOME/conf/airflow.cfg.

To be validated by the API, we simply need to pass an Authorization header and the base64 encoded form of username:password where username and password are for the user created in Airflow.

#### Step 2: Test the API by Listing Dags
With Step 1 complete, we can list the dags in Airflow via /dags. For example:
![alt text](https://github.com/ranjitreddy2013/Airflow-Spark-Ezmeral/blob/main/connection/api_request_list_dags.png)

#### Step 3: Trigger the dag
In Step 2,  we saw that we can use a GET request to /dags to get a simple list. We can use a POST request to trigger the dag by name. The DAG I want to trigger is called tch_dag_run. As shown below:

   ![alt text](https://github.com/ranjitreddy2013/Airflow-Spark-Ezmeral/blob/main/connection/postman_request_trigger.png)
   
#### Step 4: Review the Triggered Dag
   
   With the DAG triggered, we can use the Airflow UI to review the process, but we can also use the REST API to poll the job for it’s status via a GET call to http://<airflow hostname>:<port>/api/v1/dags/tch_dag_run/dagRuns where again, we are passing in the dag name. In this case, we are passing in tch_dag_run but you would use the name of your own dag. In the below screenshot, DAG run can be verified in the Airflow UI by clicking on the "tch_dag_run" DAG. Selecting the Run as shown below:
      ![alt text](https://github.com/ranjitreddy2013/Airflow-Spark-Ezmeral/blob/main/connection/api_trigger_dag.png)


   
   

