import sys
import os
from os import listdir
from os.path import isfile, join


def main():
    if sys.version_info.major < 3:
        print("ERROR: Python 3 required to run this script")
        exit()

    if len(sys.argv) != 2:
        print("Usage: python import_dump.py dump_directory")
        exit()

    file_directory = sys.argv[1]

    mysql_user = input("Enter mysql user: ")
    mysql_password = input("Enter mysql password: ")
    mysql_db = input("Enter mysql database: ")

    import_dump(file_directory, mysql_user, mysql_password, mysql_db)


def import_dump(file_directory, mysql_user, mysql_password, mysql_db):
    files = [f for f in listdir(file_directory) if isfile(join(file_directory, f))]

    # sorted files based on size
    sorted_files = sorted(files, key=lambda x: os.stat(os.path.join(file_directory, x)).st_size)

    for item in sorted_files:
        file_path = os.path.join(file_directory, item)
        command = "pv {file_path} | mysql -u{mysql_user} -p{mysql_password} {mysql_db}".format(
            file_path=file_path,
            mysql_user=mysql_user,
            mysql_password=mysql_password,
            mysql_db=mysql_db
        )
        print(item)
        os.system(command)


if __name__ == '__main__':
    main()