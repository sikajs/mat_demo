import pandas as pd
from sqlalchemy import create_engine, text
from .base import AbstractDatabaseConnection

class PostgresqlConnection(AbstractDatabaseConnection):
    def __init__(self, user: str, password: str, host="localhost", dbname="demo_development"):
        conn_str = "postgresql+psycopg2://{user}:{password}@{host}:5432/{dbname}".format(
                        user=user, password=password, host=host, dbname=dbname)
        self.engine = create_engine(conn_str)

    def connect(self):
        return self.engine.connect()

    def query(self, sql: str, params=None):
        try:
            with self.connect() as conn:
                result = conn.execute(text(sql), params or {})
                if sql.lstrip().lower().startswith("select"):  # process select query
                    data = result.fetchall()
                    return data
                else:  # proceed DML
                    conn.commit()
                    return result.rowcount
        except Exception as e:
            print(e)

    def init_material(self, csv_file = "semiconductor_materials_400.csv"):
        table_name = "materials"
        df = pd.read_csv(csv_file)
        print(df)
        df.to_sql(table_name, con=self.engine, if_exists='replace', index=False)