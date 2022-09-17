import datetime
import json
import pendulum
import pandas as pd

from io import BytesIO, StringIO

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
        records = ti.xcom_pull(task_ids='scrape_senate', key='senate_records')

        records = pd.read_csv(StringIO(records))
        postgres_hook = PostgresHook(postgres_conn_id="docker_postgres")
        conn = postgres_hook.get_conn()
        cur = conn.cursor()

        # TODO more efficient insertion
        for line in records.iterrows():
            line = line[1]
            cur.execute(f"INSERT INTO congress.senate_disclosures (first_name, last_name, filer_type, report_type, date_received) VALUES ('{line['First Name (Middle)']}', '{line['Last Name (Suffix)']}', '{line['Office (Filer Type)']}', '{line['Report Type']}', '{line['Date Received/Filed']}');")
        
        conn.commit()

    create_senate_table_task = PostgresOperator(
        task_id="create_senate_table",
        postgres_conn_id="docker_postgres",
        sql="schemas/sql/senate_disclosures.sql"
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
