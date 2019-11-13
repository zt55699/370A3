import csv
from enum import Enum

def read_input_file(file_name:str) -> list:
    with open(file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        list_of_tuples_input = []
        for row in reader:
            temp_li = []
            for element in row:
                temp_li.append(element)
            list_of_tuples_input.append(tuple(temp_li))


    return list_of_tuples_input


def main():
    table_list = ["Students","Teachers","Worksheets","StudentContact","TeacherContact","WorksheetHistory"]
    s = "DROP TABLE"
    t = ";"
    for table in table_list:
        temp = '{0} {1}{2}'.format(s,table,t)
        print(temp)
        # cursor.execute(temp)

if __name__ == "__main__":
    main()
