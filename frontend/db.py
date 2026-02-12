import sqlite3

def get_db():
    conn = sqlite3.connect('data_src/processed/space_insurance.db')
    return conn

