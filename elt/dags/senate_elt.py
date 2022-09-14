import datetime
import pendulum

from airflow import DAG
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.python import PythonOperator

import senate_scraper as scraper

with DAG(
    'senate_scrape_load',
    schedule_interval="@daily",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=5)
) as dag:

    def scrape_senate(**kwargs): # TODO only pull new docs
        records = scraper.scrape_all()
        ti = kwargs['ti']
        ti.xcom_push('senate_records', records)

    def load_senate(**kwargs):
        ti = kwargs['ti']
        records = ti.xcom_pull(task_ids='scrape', key='senate_records')

        postgres_hook = PostgresHook(postgres_conn_id="docker_postgres")
        conn = postgres_hook.get_conn()
        cur = conn.cursor()

        # TODO more efficient insertion
        for line in records.iterrows():
            cur.executemany(f"INSERT INTO senate_disclosures (first_name, last_name, filer_type, report_type, date_received) VALUES ('{line['first_name']}', '{line['last_name']}', '{line['filer_type']}', '{line['report_type']}', '{line['date_received']}');")    
        
        conn.commit()

    create_senate_table_task = PostgresOperator(
        task_id="create senate_table",
        postgres_conn_id="docker_postgres",
        sql="sql/senate_disclosures.sql"
    )
    scrape_senate_task = PythonOperator(
        task_id='scrape_senate',
        python_callable=scrape_senate,
    )
    load_senate_task = PythonOperator(
        task_id='load_senate',
        python_callable=load_senate,
    )

    create_senate_table_task >> scrape_senate_task >> load_senate_task
