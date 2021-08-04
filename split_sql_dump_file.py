import sys
import re
import os

if sys.version_info.major < 3:
    print("ERROR: Python 3 required to run this script")
    exit()

if len(sys.argv) != 3:
    print("Usage: python split_sql_dump_file.py dump.sql output_directory")
    exit()

sql_file_path = sys.argv[1]
output_folder_path = sys.argv[2]
table_name = None
output_file_path = None
tempfile = None
file_end_reached = False
files_updated = list()

environment_variable_info_start = ""
environment_variable_info_end = ""

if not os.path.exists(sql_file_path):
    print("ERROR: {} does not exist.".format(sql_file_path))
    exit()

output_data_folder_path = os.path.join(output_folder_path, "data")
if not os.path.exists(output_data_folder_path):
    os.makedirs(output_data_folder_path)

output_structure_folder_path = os.path.join(output_folder_path, "structure")
if not os.path.exists(output_structure_folder_path):
    os.makedirs(output_structure_folder_path)

with open(sql_file_path, 'rb') as bigfile:
    for line_number, line in enumerate(bigfile):
        line_string = line.decode("utf-8", "ignore")

        if 'Table structure for table' in line_string:
            match = re.match(r"^-- Table structure for table `(?P<table>\w+)`$", line_string)
            if match:
                table_name = match.group('table')
                print(table_name + " - structure")
                output_file_path = "{output_folder_path}/{table_name}.sql".format(
                    output_folder_path=output_structure_folder_path.rstrip('/'), table_name=table_name)
                files_updated.append(output_file_path)

                if tempfile:
                    tempfile.close()
                tempfile = open(output_file_path, 'wb')

                # write environment variable info at the start of the file
                tempfile.write(bytes(environment_variable_info_start, 'utf-8', 'ignore'))

        if 'Dumping data for table' in line_string:
            match = re.match(r"^-- Dumping data for table `(?P<table>\w+)`$", line_string)
            if match:
                table_name = match.group('table')
                print(table_name + " - data")
                output_file_path = "{output_folder_path}/{table_name}.sql".format(
                    output_folder_path=output_data_folder_path.rstrip('/'), table_name=table_name)
                files_updated.append(output_file_path)

                if tempfile:
                    tempfile.close()
                tempfile = open(output_file_path, 'wb')

                # write environment variable info at the start of the file
                tempfile.write(bytes(environment_variable_info_start, 'utf-8', 'ignore'))

        if not table_name:
            environment_variable_info_start = environment_variable_info_start + line_string
            continue

        if '40103 SET TIME_ZONE=@OLD_TIME_ZONE' in line_string:
            file_end_reached = True

        if file_end_reached:
            environment_variable_info_end = environment_variable_info_end + line_string
        else:
            tempfile.write(line)
    tempfile.close()

# updating all files with environment info added at the end of file
print("Appending environment variables at the end of  all files")
for file_path in files_updated:
    with open(file_path, 'a') as tempfile:
        tempfile.write(environment_variable_info_end)



