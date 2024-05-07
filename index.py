import os
import sys

from php_functions import Craft, CreateLoginFile
from sql_to_php import convert_db_to_json 

try:
 command = sys.argv[1]
except:
 command = 3 

if command=='db':
  for file in os.listdir(os.curdir):
    if file.endswith(".db"):
        x = file.split(".")[0].strip()
        output_folder = "sql_to_json" # Replace with your SQLite database file name
        convert_db_to_json(file,output_folder)
        print("Saved to "+ output_folder)
  
elif command =='json':
  CreateLoginFile()
  for file in os.listdir(os.curdir):
    if file.endswith(".json"):
        output_folder = "json_to_php"
        Craft(file,output_folder)
        print("Saved to "+ output_folder)

else :
   print('Invalid Command')        