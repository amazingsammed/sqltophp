import sqlite3
import json
import os

def convert_db_to_json(db_file,output_folder):
    # Connect to the database
    if not os.path.exists(output_folder):
       os.makedirs(output_folder) 
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Get list of tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()


    # Convert each table to JSON
    for table in tables:
        table_name = table[0]
        if not table_name =='sqlite_user':
         cursor.execute(f"SELECT * FROM {table_name} limit 1;")
         rows = cursor.fetchall()
         for row in rows:
            row_dict = {}
            for i, col in enumerate(cursor.description):
                row_dict[col[0]] = row[i] 
            file_path = os.path.join(output_folder,f"{table_name}.json")    

            try :
             with open(file_path, "w") as json_file:
                json.dump(row_dict, json_file, indent=5)
            except :
               print(row_dict + "ERROR in Dictionary")      
    conn.close()

# Example usage:
