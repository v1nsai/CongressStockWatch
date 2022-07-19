import datetime
import pendulum

from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator

import senate_scraper as scraper

@dag(
    'senate_scrape_load',
    schedule_interval="@daily",
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    dagrun_timeout=datetime.timedelta(minutes=5),
)
def Etl():
    
    create_senate_disclosures_table = PostgresOperator(
        task_id="create_senate_disclosures_table",
        postgres_conn_id="docker_postgres",
        sql="sql/senate_disclosures.sql"
    )

    @task
    def load_new_disclosures():
        recent_filings = scraper.scrape_first_page()

        postgres_hook = PostgresHook(postgres_conn_id="docker_postgres")
        conn = postgres_hook.get_conn()
        cur = conn.cursor()
        cur.executemany("""INSERT INTO senate_disclosures (file_date, transaction_date, issuer, reporter, transaction_type, transaction_hash, amount, ownership) VALUES (%(file_date)s, %(transaction_date)s, %(issuer)s, %(reporter)s, %(transaction_type)s, %(transaction_hash)s, %(amount)s, %(ownership)s)""", senate_disclosures)        
        conn.commit()

    create_senate_disclosures_table >> load_new_disclosures()

dag = Etl()
