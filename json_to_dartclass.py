import json
import sys
import os

def generate_dart_class(class_name, json_data, allow_null=False):
    output_folder ="models"
    if not os.path.exists(output_folder):
       os.makedirs(output_folder) 
    dart_class = "class {} {{\n".format(class_name)

    for key, value in json_data.items():
        value_type = "dynamic" if allow_null else _get_dart_type(value)
        dart_class += "  {} {};\n".format(value_type, key)


    dart_class += "\n  {}({{\n".format(class_name)

    for key, value in json_data.items():
        dart_class += "    required this.{},\n".format(key)
    dart_class = dart_class[:-2]
    dart_class += "});\n\n" 
    

    dart_class += " factory {}.fromMap(Map<String, dynamic> map) {{\n".format(class_name)
    dart_class += f"   return {class_name} (\n"

    for key, value in json_data.items():
        value_type = "dynamic" if allow_null else _get_dart_type(value)
        dart_class += f"    {key} : map['{key}'] as {value_type},\n"

    # dart_class += "    {}\n".format("    ".join([
    #     "{} = map['{}'] as ,".format(key, key) for key in json_data.keys()
    # ]))

    dart_class = dart_class[:-2]
    dart_class += ");\n}\n\n"

    dart_class += "  Map<String, dynamic> toMap() {\n"
    dart_class += "    return {\n"
    dart_class += "      {}\n".format(",\n      ".join([
        "'{}': {}".format(key, "this." + key) for key in json_data.keys()
    ]))
    dart_class += "    };\n"
    dart_class += "  }\n}\n"
    file_path = os.path.join(output_folder,f"{class_name}.dart")    

    try :
      with open(file_path, "w") as file:
         file.write(dart_class)
    except :
      print("ERROR in creating file")  
    # return dart_class

def _get_dart_type(value):
    if isinstance(value, bool):
        return "bool"
    elif isinstance(value, int):
        return "int"
    elif isinstance(value, float):
        return "double"
    elif isinstance(value, str):
        return "String"
    elif isinstance(value, list):
        return "List<dynamic>"
    elif isinstance(value, dict):
        return "Map<String, dynamic>"
    else:
        return "dynamic"


    # if len(sys.argv) != 2:
    #     print("Usage: python script.py <json_file>")
    #     return

    # json_file = sys.argv[1]
# json_file = "customer.json"
# class_name = json_file.split(".")[0].capitalize()

# try:
#    with open(json_file, "r") as file:
#             json_data = json.load(file)
# except FileNotFoundError:
#    print("File not found.")
# except json.JSONDecodeError:
#    print("Invalid JSON format.")


# generate_dart_class(class_name, json_data)


