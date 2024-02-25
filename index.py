import sqlite3
import json
import os
import functions as fan




db_file_path = 'aiobook22.db'
table_info = fan.get_table_info(db_file_path)
json_output = json.dumps(table_info, indent=2)
table_data = json.loads(json_output)
output_dir = os.path.dirname(__file__)
output_dir = output_dir +'\\table'

for table_info in table_data:
    table_name = table_info['tablename']
    columns = ', '.join(table_info['rows'])
    php_content = f'''<?php
$tablename = '{table_name}';
$columns = '{columns}';

// Handle the action parameter
if (isset($_GET['action'])) {{
    $action = $_GET['action'];
    switch ($action) {{
       case 'create':
            // Construct the INSERT query
            $theinsert = "INSERT INTO `$tablename` (`{columns}`)
                          VALUES ('$value1', '$value2', ...)";
            // Execute the query (you'll need to handle database connection and execution)
            // Example: $db->query($theinsert);
            break;
      case 'read':
            // Construct the SELECT query
            $theselect = "SELECT * FROM `$tablename` WHERE ...";
            // Execute the query and fetch results
            // Example: $result = $db->query($theselect);
            break;
        case 'update':
            // Construct the UPDATE query
            $theupdate = "UPDATE `$tablename` SET ... WHERE ...";
            // Execute the query
            // Example: $db->query($theupdate);
            break;
        case 'delete':
            // Construct the DELETE query
            $thedelete = "DELETE FROM `$tablename` WHERE ...";
            // Execute the query
            // Example: $db->query($thedelete);
            break;
        default:
            echo 'Invalid action specified.';
    }}
}}
?>
'''


    # Write content to a PHP file
    filename = f'{output_dir}/{table_name}.php'
    with open(filename, 'w') as php_file:
     php_file.write(php_content)
     print(f'Created PHP file: {filename}')
#print(json_output)
