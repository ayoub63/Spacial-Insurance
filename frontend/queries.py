import sqlite3
import pandas as pd
import streamlit as st

db_path = 'data_src\processed\space_insurance.db'

def query_df(sql):
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

def has_column(table, col):
    df = query_df(f"PRAGMA table_info({table});")
    return col in df["name"].tolist()

