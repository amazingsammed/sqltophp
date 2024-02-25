import sqlite3
import json
import os

def get_table_info(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = [v[0] for v in cursor.fetchall() if v[0] != "sqlite_sequence"]

    table_info_list = []
    for table_name in table_names:
        cursor = conn.execute(f"PRAGMA table_info({table_name});")
        column_names = [row[1] for row in cursor.fetchall()]
        table_info_list.append({"tablename": table_name, "rows": column_names})

    conn.close()
    return table_info_list