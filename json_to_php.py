import json
import os





def loadJson(filename):
    try:
        file_contents = open(filename, "r").read()
        data = json.loads(file_contents)
        return data
    except Exception as e:
        print(e)
        
def CreateLoginFile():
    global loginphp
    filename = 'login.php'
    with open(filename, 'w') as Output:
        Output.write(loginphp)
    print("Saved to "+ filename)    
    
def Craft(file_name, output_folder):
    if not os.path.exists(output_folder):
       os.makedirs(output_folder) 
    global head, read_sample,create_sample, update_sample ,delete_sample,tail

    php_template = ""

    table_name = file_name.split(".")[0].strip()

    template_head = f'<?php\ninclude "loginfile.php";\n$tablename = "{table_name}";'
    php_template += template_head
    php_template += head
    
    # get all data fields from json file
    json_data = loadJson(file_name)
    data_fields = json_data.keys()

    # Craft php fields for create
    create = craftCreate(table_name, json_data)

    # Craft php fields for update
    update = craftUpdate(table_name, json_data)

    # Craft php fields for delete
    delete = craftDelete(table_name, json_data)

    # combine everything
    php_template += read_sample
    php_template += create
    php_template += create_sample
    php_template += update
    php_template += update_sample
    php_template += delete
    php_template += delete_sample
    php_template += tail

    # write 
    
    output = file_name.split(".")[0].strip() +'.php'
    file_path = os.path.join(output_folder,output)   
    with open(file_path, 'w') as Output:
        Output.write(php_template)

def craftCreate(tablename, json_data):
    php_code = '\n\tcase "create":\n'
    len_fields = len(json_data.keys())

    # get bind parameter data type
    param = getBindDataTypes(json_data)

    # prepared statement
    process_code = '\n\t\t$stmt = $con->prepare("INSERT INTO `'+tablename+'` ('

    #create form field parameters
    for field in json_data.keys():
        code = '\t\t${0} = $_POST["{1}"];\n'.format(field, field);
        php_code+= code

    # php to process fields
    count = 0
    break_point = len(json_data.keys()) - 1
    for field in json_data.keys():
        if count == break_point:
            process_code += '`'+field+'`'
            break
        else:
            process_code += '`'+field+'`,'
            count += 1

    # Prepare the statement
    values_parameters = ""
    vcount = 0
    for i in range(len_fields):
        if vcount == break_point:
           values_parameters += '? '
        else:
           values_parameters += '?,'
           vcount += 1

    # prepared statement
    process_code += ')  VALUES ('+values_parameters+')");\n'
    process_code += "if ($stmt) {\n"
    php_code += process_code

    # Bind parameters
    bcount = 0
    bind_param = f'\n\t\t$stmt->bind_param("{param}",'
    for field in json_data.keys():
        if bcount == break_point:
           bind_param += f'${field} '
           break
        else:
           bind_param += f'${field},'
    bind_param += ');'
    php_code += bind_param
    return php_code;

# function to make php update code
def craftUpdate(tablename, json_data):
    php_code = '\n\tcase "update":\n'
    php_code+= '\t\t$id = $_POST["id"];\n'
    len_fields = len(json_data.keys())

    # get bind parameter data type
    param = getBindDataTypes(json_data)

    # prepared statement
    process_code = '\n\t\t$stmt = $con->prepare("UPDATE `'+tablename+'` SET '

    #create form field parameters
    for field in json_data.keys():
        code = '\t\t${0} = $_POST["{1}"];\n'.format(field, field);
        php_code+= code

    # php to process fields
    id = ""
    count = 0
    break_point = len(json_data.keys()) -1
    for field in json_data.keys():
        if count == break_point:
            process_code += f'`{field}` = ? '
            break
        else:
            process_code += f'`{field}` = ?,'
            count += 1
    process_code += f'WHERE `id` = ? ");'
    process_code += "if ($stmt) {\n"


    # prepared statement
    php_code += process_code

    # Bind parameters
    bcount = 0
    bind_param = f'\n\t\t$stmt->bind_param("{param}",'
    for field in json_data.keys():
        if bcount == break_point:
            bind_param += f'${field}'
            break
        else:
            bind_param += f'${field},'
            bcount += 1
    bind_param += ',$id);'
    php_code += bind_param

    return php_code;


def craftDelete(tablename, json_data):
    php_code = '\n\tcase "delete":\n'
    php_code+= '\t\t$id = $_POST["id"];\n'


    # prepared statement
    process_code = '\n\t\t$stmt = $con->prepare("Delete `'+tablename+'` SET `status` = 0 WHERE `id` = ?"); '
    
    bind_param = '\n\t\t$stmt->bind_param("i", $id);'
    #create form field parameters
    # for field in json_data.keys():
    #     code = '\t\t${0} = $_POST["{1}"];\n'.format(field, field);
    #     php_code+= code
    process_code += "if ($stmt) {\n"
    php_code += process_code
    php_code += bind_param

    return php_code


def getType(data):
    dataType = str(type(data))
    if 'int' in dataType:
        return "i"
    elif 'str' in dataType:
        return "s"
    elif 'float' in dataType:
        return "d"
    else:
        return "b" # we treat everything else as binary


def getBindDataTypes(json_data):
    param = ""
    for key in json_data.keys():
        param+= getType(json_data.get(key))
    return param



loginphp ="""
<?php

$host= "database_host_here";
$user="user_name_here";
$password="password_here";
$dbname = 'database_name_here';


$con = mysqli_connect($host,$user,$password, $dbname);

        # Check connection
if (mysqli_connect_errno()) {
    echo 'Database connection error: ' . mysqli_connect_error();
            exit();
}

?>"""
head = """
// We check the action passed then give it to switch case

if (isset($_POST["action"])) {
    $action = $_POST["action"];\n
"""

read_sample = """switch ($action) {
    case "readall":
        $cmdsql = "select * from $tablename ";
        $recall = mysqli_query($con, $cmdsql);
        while ($recallissue  = mysqli_fetch_array($recall, MYSQLI_ASSOC)) {
            $row_array[] = $recallissue;
        };

        if (empty($row_array)) {
            echo "No $tablename found or table is empty";
        } else {
            $outputArr = array();
            $outputArr = $row_array;

            echo json_encode($outputArr);
        }

        break;\n
"""

create_sample = """// Execute the statement
            $success = $stmt->execute();

            // Check if the execution was successful
            if (!$success) {
                echo "$tablename => Could not run query: " . mysqli_error($con);
                exit;
            }

            $result_data = array(
                'result' => "success"
            );
            echo json_encode($result_data);

            // Close the statement
            $stmt->close();
             } else {
            echo "Failed to prepare". mysqli_error($con);
        }
            break;\n
"""

update_sample = """// Execute the statement
            $success = $stmt->execute();

            // Check if the execution was successful
            if (!$success) {
                echo "$tablename => Could not run query: " . mysqli_error($con);
                exit;
            }

            $result_data = array(
                'result' => "success"
            );

            // Close the statement
            $stmt->close();

            // Encode the result data as JSON and echo it
            echo json_encode($result_data);
            } else {
            echo "Failed to prepare". mysqli_error($con);
        }

            // End the switch statement
            break;\n
"""

delete_sample = """
           // Execute the statement
            $success = $stmt->execute();

            // Check if the execution was successful
            if (!$success) {
                echo "$tablename => Could not run query: " . mysqli_error($con);
                exit;
            }

            $result_data = array(
                'result' => "success"
            );

            // Encode the result data as JSON and echo it
            echo json_encode($result_data);

            // Close the statement
            $stmt->close();
            } else {
            echo "Failed to prepare". mysqli_error($con);
        }

            // End the switch statement
            break;

        default:
            echo json_encode("No Action Selected");
    }\n
"""

tail = """\n} else {
    echo 'Try Again, Something went wrong';
}
"""


