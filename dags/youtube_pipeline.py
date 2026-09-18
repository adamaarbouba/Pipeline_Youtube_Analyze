from datetime import timedelta

import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator


default_args = {
    "owner": "dataengineers",
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}


with DAG(
    dag_id="extract_to_staging",
    default_args=default_args,
    start_date=pendulum.datetime(2026, 1, 1, tz="Africa/Casablanca"),
    schedule="0 14 * * *",
    catchup=False,
    max_active_runs=1,
) as extract_to_staging:
    extract_playlist = BashOperator(
        task_id="extract_playlist",
        bash_command="python /opt/airflow/src/extract_youtube.py",
    )

    extract_video_details = BashOperator(
        task_id="extract_video_details",
        bash_command="python /opt/airflow/src/extract_video_details.py",
    )

    merge_data = BashOperator(
        task_id="merge_data",
        bash_command="python /opt/airflow/src/merge_raw.py",
    )

    load_staging = BashOperator(
        task_id="load_staging",
        bash_command="python /opt/airflow/src/load_staging.py",
    )

    trigger_core = TriggerDagRunOperator(
        task_id="trigger_core",
        trigger_dag_id="staging_to_core",
        wait_for_completion=False,
    )

    (
        extract_playlist
        >> extract_video_details
        >> merge_data
        >> load_staging
        >> trigger_core
    )


with DAG(
    dag_id="staging_to_core",
    default_args=default_args,
    start_date=pendulum.datetime(2026, 1, 1, tz="Africa/Casablanca"),
    schedule=None,
    catchup=False,
    max_active_runs=1,
) as staging_to_core:
    BashOperator(
        task_id="load_core",
        bash_command="python /opt/airflow/src/load_core.py",
    )
