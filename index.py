import json
import os
import sys

from json_to_dartclass import generate_dart_class
from json_to_php import Craft, CreateLoginFile
from sql_to_php import convert_db_to_json 

# if len(sys.argv) != 2:
#   print("Usage: python script.py <db,json,dart>")
#   exit
        

try:
 command = sys.argv[1]
except:
 command = '2' 


if command=='db':
  for file in os.listdir(os.curdir):
    if file.endswith(".db"):
        x = file.split(".")[0].strip()
        output_folder = "sql_to_json" # Replace with your SQLite database file name
        convert_db_to_json(file,output_folder)
        print("Saved to "+ output_folder)
  
elif command =='php':
  CreateLoginFile()
  for file in os.listdir(os.curdir):
    if file.endswith(".json"):
        output_folder = "json_to_php"
        Craft(file,output_folder)
        print("Saved to "+ output_folder)
elif command == 'dart':
  for file in os.listdir(os.curdir):
    if file.endswith(".json"):
      class_name = file.split(".")[0].capitalize()
      with open(file, "r") as file:
            json_data = json.load(file)
      dart_class = generate_dart_class(class_name, json_data)      

             
else :
   print("Usage: python script.py <db,php,dart>")
   print("db [for db to json]\php [for json to php]\ndart [for json to dart]")       