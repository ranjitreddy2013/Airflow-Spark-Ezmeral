import airflow
from datetime import timedelta
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator 
from airflow.utils.dates import days_ago

import os
import sys

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

spark_job = ("spark-submit --class com.tch.deidentification.DeidentifyPHIApplication"
             "--master yarn "
             "/home/mapr/tch-deidentification-application/target/tch-deidentification-1.0-jar-with-dependencies.jar")

dag_spark = DAG(
        dag_id = "tch-deidentify-job",
        default_args=default_args,
        # schedule_interval='0 0 * * *',
        schedule_interval='@once',
        dagrun_timeout=timedelta(minutes=60),
        description='TCH deidentify job in airflow',
        start_date = airflow.utils.dates.days_ago(1)
)

spark_submit_local = SparkSubmitOperator(
	task_id='spark_tch_task',
	conn_id= 'spark_local',
        java_class='com.tch.deidentification.DeidentifyPHIApplication',
        application='local:///home/mapr/tch-deidentification-application/target/tch-deidentification-1.0-jar-with-dependencies.jar',
        name='tch-airflow-spark',
        application_args=["/user/mapr/pedsnet","pedsnet","maprfs:///user/mapr/omop/raw","maprfs:///user/mapr/omop/deidentified"],
	dag=dag_spark
)

spark_submit_local

if __name__ == "__main__":
   dag_spark.cli()
