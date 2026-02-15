# Author: Adam Ibrahimkhel

import sqlite3
import os


def get_db():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(base_dir, 'data_src', 'processed', 'space_insurance.db')
    conn = sqlite3.connect(db_path)
    return conn