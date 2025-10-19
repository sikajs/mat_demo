import pandas as pd
import sqlite3
from .base import AbstractDatabaseConnection

class SqliteConnection(AbstractDatabaseConnection):
    def __init__(self, database_file="database.db"):
        self.database_file = database_file

    def connect(self):
        return sqlite3.connect(self.database_file)

    def query(self, sql: str):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            if sql.strip().lower().startswith("select"):  # process select query
                data = cursor.fetchall()  # 不適合大量資料，一次全部進記憶體
                return data
            else:  # proceed DML
                conn.commit()
                return cursor.rowcount
        finally:
            conn.close()

    def init_material(self, csv_file = "semiconductor_materials_400.csv"):
        table_name = "materials"
        df = pd.read_csv(csv_file)
        print(df)
        df.to_sql(table_name, con=self.connect(), if_exists='replace', index=False)