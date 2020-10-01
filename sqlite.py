import pandas as pd
from sqlalchemy import create_engine
from collectors import get_merged_data

def push_data(df, table):
    engine = create_engine('sqlite:///C:\\Users\\CA015FO\\basketball\\data\\nba_data.db')
    df.to_sql(table, con=engine, if_exists='replace', index=False)
    return None

def get_data(table):
    return pd.read_sql_table(table, 'sqlite:///C:\\Users\\CA015FO\\basketball\\data\\nba_data.db')