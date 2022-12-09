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
		application ='/home/hduser/basicsparksubmit.py' ,
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
   Creating the connection airflow to connect the spark as shown in below. In the Airflow web ui, click on the Admin tab, select the connections, you will get a new window with options to add new connections. Click on "+" to create a new connection in Airflow to connect to Spark as shown below:
   
   Enter desired conn id, select Spark-Ezmeral as connection type, 
   
   
   
   
   spark-submit script is used for submitting a Spark app to Data Fabric cluster. For example, running PySpark app sparksubmit_basic.py  is as follows:
   ```
   /opt/mapr/spark/spark-3.2.0/bin/spark-submit --master local[*] --name arrow-spark --queue root.default /home/mapr/sparksubmit_basic.py
   ```
   So for building a SparkSubmitOperator in Airflow you need to follow below steps:
   
   

