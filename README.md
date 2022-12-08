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
   

