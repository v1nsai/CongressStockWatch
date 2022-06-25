import datetime
import pendulum

from airflow.decorators import dag, task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.plugins_manager import senate_scraper

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
        postgres_conn_id="postgres_conn",
        sql="sql/senate_disclosures.sql"
    )

    @task
    def load_new_disclosures():        
        senate_disclosures = senate_scraper.get_current_disclosures()

        postgres_hook = PostgresHook(postgres_conn_id="postgres_conn")
        conn = postgres_hook.get_conn()
        cur = conn.cursor()
        cur.executemany("""INSERT INTO bar(file_date, transaction_date, issuer, reporter, transaction_type, transaction_hash, amount, ownership) VALUES (%(file_date)s, %(transaction_date)s, %(issuer)s, %(reporter)s, %(transaction_type)s, %(transaction_hash)s, %(amount)s, %(ownership)s)""", senate_disclosures)        
        conn.commit()

    create_senate_disclosures_table >> load_new_disclosures()

dag = Etl()
