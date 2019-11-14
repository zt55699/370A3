import psycopg2
from enum import Enum
from reader import read_input_file


class Table(Enum):
    STUDENTS = 0
    TEACHERS = 1
    WORKSHEETS = 2
    STUDENTCONTACT = 3
    TEACHERCONTACT = 4
    WORKSHEETHISTORY = 5


def build_db(connection:object) -> None:
    cursor = connection.cursor()
    # print(connection.get_dsn_parameters(), "\n")

    # cursor.execute("SELECT version();")
    # record = cursor.fetchone()
    # print("You are connected to - ", record, "\n")
    table_create_list = []
    

    student_table = """CREATE TABLE Students (
        studentID INTEGER PRIMARY KEY,
        mathOlympiads BOOLEAN NOT NULL,
        language VARCHAR(255) NOT NULL,
        level VARCHAR(255) NOT NULL,
        country VARCHAR(255) NOT NULL);"""
    table_create_list.append(student_table)

    teachers_table = """CREATE TABLE Teachers(
        employeeID INTEGER PRIMARY KEY,
        language VARCHAR(255) NOT NULL,
        expertise VARCHAR(255) NOT NULL,
        availability VARCHAR(2048) NOT NULL);"""
    table_create_list.append(teachers_table)

    ### added url 
    ### need an id for worksheet that would be the primary key? 
    worksheet_table = """CREATE TABLE Worksheets(
        title VARCHAR(255) PRIMARY KEY,
        author VARCHAR(255),
        level VARCHAR(255) NOT NULL,
        url VARCHAR(255) UNIQUE,
        subject VARCHAR(255) NOT NULL);"""
    table_create_list.append(worksheet_table)

    worksheethistory_table = """CREATE TABLE WorksheetHistory(
        studentID INTEGER NOT NULL,
        employeeID INTEGER NOT NULL,
        title VARCHAR(255) NOT NULL,
        mark NUMERIC(3,2) NOT NULL, 
        comment VARCHAR(2048),
        PRIMARY KEY(studentID, title),
        FOREIGN KEY (studentID) REFERENCES Students(studentID) ON DELETE CASCADE,
        FOREIGN KEY (employeeID) REFERENCES Teachers(employeeID) ON DELETE CASCADE,
        FOREIGN KEY (title) REFERENCES Worksheets(title) ON DELETE CASCADE);"""
    table_create_list.append(worksheethistory_table)

    student_contact = """CREATE TABLE StudentContact ( 
        id INTEGER PRIMARY KEY,
        name VARCHAR NOT NULL,
        email VARCHAR(255) NOT NULL,
        skype VARCHAR(255),
        phone VARCHAR(25),
        FOREIGN KEY (id) REFERENCES Students(studentID) ON DELETE CASCADE);"""
    table_create_list.append(student_contact)

    teacher_contact = """CREATE TABLE TeacherContact ( 
        id INTEGER PRIMARY KEY,
        name VARCHAR NOT NULL,
        email VARCHAR(255) NOT NULL,
        skype VARCHAR(255),
        phone VARCHAR(25),
        FOREIGN KEY (id) REFERENCES Teachers(employeeID) ON DELETE CASCADE);"""
    table_create_list.append(teacher_contact)

    for table in table_create_list:
        cursor.execute(table)
        connection.commit()


def add_to_table(connection:object, info:list, table:int) -> None:

    cursor = connection.cursor()

    if table == Table.STUDENTS.value:
        for info_tuple in info:
            cursor.execute("""
                INSERT INTO Students (studentID, mathOlympiads, language, level, country)
                VALUES (%s, %s, %s, %s, %s);
                """,info_tuple)
            connection.commit()

    elif table == Table.TEACHERS.value:
        for info_tuple in info:
            cursor.execute("""
                INSERT INTO Teachers (employeeID, language, expertise, availability)
                VALUES (%s, %s, %s, %s);
                """,info_tuple)
            connection.commit()

    elif table == Table.WORKSHEETS.value:
        for info_tuple in info:
            cursor.execute("""
                INSERT INTO Worksheets (title, author, level, url, subject)
                VALUES (%s, %s, %s, %s, %s);
                """,info_tuple)
            connection.commit()

    elif table == Table.STUDENTCONTACT.value:
        for info_tuple in info:
            cursor.execute("""
                INSERT INTO StudentContact (id, name, email, skype, phone) 
                VALUES (%s, %s, %s, %s, %s);
                """,info_tuple)
            connection.commit()
    elif table == Table.TEACHERCONTACT.value:
        for info_tuple in info:
            cursor.execute("""
                INSERT INTO TeacherContact (id, name, email, skype, phone)
                VALUES (%s, %s, %s, %s, %s);
                """,info_tuple)
            connection.commit()
    else: 
        for info_tuple in info:
            cursor.execute("""
                INSERT INTO WorksheetHistory (studentID, employeeID, title, mark, comment)
                VALUES (%s, %s, %s, %s, %s);
                """,info_tuple)
            connection.commit()
      

def add_to_db(connection:object) -> None:
    
    input_file = ("Students.csv", "Teachers.csv", "Worksheets.csv", "StudentContact.csv", "TeacherContact.csv", "WorksheetHistory.csv")
    
    while(True):
        #this could be a loop too 
        print("List of commands for adding information to the tables:")
        print("Enter 0 to insert information into the Students table")
        print("Enter 1 to insert information into the Teachers table")
        print("Enter 2 to insert information into the Worksheets table")
        print("Enter 3 to insert information into the StudentContact table")
        print("Enter 4 to insert information into the TeacherContact table")
        print("Enter 5 to insert information into the WorksheetHistory table")
        print("Enter 6 to insert information into all the tables")
        print("Enter 7 to go back")
        print("")

        user_input = input()
        
        if user_input == '7':
            break

        elif user_input == '6':
            for table_number in range(6):
                add_to_table(connection, read_input_file(input_file[table_number]), table_number)
            break

        elif '0' <= user_input <= '5':
            table_number = int(user_input)
            add_to_table(connection, read_input_file(input_file[table_number]), table_number)
            break

        else:
            print("Input invalid, please try again.\n")


def drop_tables(connection:object) -> None:
    cursor = connection.cursor()
    table_list = ["StudentContact","TeacherContact","WorksheetHistory","Students","Teachers","Worksheets"]
    s = "DROP TABLE IF EXISTS"
    t = ";"
    for table in table_list:
        temp = '{0} {1}{2}'.format(s,table,t)
        # print(temp)
        cursor.execute(temp)
    connection.commit()


def get_table(cursor:object) -> str:
    cursor.execute("""SELECT table_name
        FROM information_schema.tables
        WHERE table_type='BASE TABLE'
        AND table_schema='public';""")
    
    print("These are the tables:")
    count = 0
    table_names = [x[0] for x in cursor.fetchall()]
    for table in table_names:
        print("Press {0} for {1}".format(count,table),end=" \n")
        count += 1
    
    t = input()
    table = table_names[int(t)] 
    return table


def get_attribute(cursor:object, table:str, flag:int = 0) -> str or list:
    """
    if flag == 1 then we return the whole LIST
            == 0 then we return the chosen STRING
    """
    cursor.execute("""SELECT column_name
        from information_schema.columns 
        where table_name = '{0}';""".format(table))
    
    print("These are the attributes:")
    count = 0
    attribute_names = [x[0] for x in cursor.fetchall()]
    if flag == 1:
        return attribute_names
    else:
        for attribute in attribute_names:
            print("Press {0} for {1}".format(count,attribute),end=" \n")
            count += 1
        a = input()
        attribute = attribute_names[int(a)]

    return attribute


def update_tables(connection:object) -> None:
    
    cursor = connection.cursor()
    print("Pick the table that you want to update:")
    table = get_table(cursor)
    print("Pick the attribute you want to update:")
    attribute = get_attribute(cursor, table)
    
    print("Please enter the name of the attribute in the table you want to use WHERE on (if the attribute is Name type Ben)")
    attribute_in_table = input()
    print("Please enter what you want to change: (attribute = 'something')")
    user_query = input()
    cursor.execute("""UPDATE {0}
        SET {1}
        WHERE
            {2} = '{3}';
        """.format(table, user_query, attribute, attribute_in_table))

    connection.commit()


def delete_from_db(connection:object) -> None:

    print("Follow the instructions to delete from the table")
    cursor = connection.cursor()
    table = get_table(cursor)
    attribute = get_attribute(cursor, table)
    print("Please enter the value of the attribute in the table to be deleted")
    user_del = input()
    cursor.execute("""DELETE FROM {0}
        WHERE {1} = '{2}';
        """.format(table, attribute, user_del))

    connection.commit()


def insert_db(connection:object) -> None:

    cursor = connection.cursor()
    table = get_table(cursor)
    attributes = get_attribute(cursor, table, 1)
    attributes_str = "(" 
    for attribute in attributes:
        print(attribute, end = " ")
        attributes_str += (attribute + ",")
    attributes_str = attributes_str.rstrip(',') + ")"
    print("")
    print("Enter the values you want to insert based on the format above, use a $ to represent a null value")
    user_in = input()
    values = tuple(['' if x is '$' else x for x in user_in.split()])
    cursor.execute("""INSERT INTO {0} {1}
        VALUES {2};
        """.format(table, attributes_str, values))
    
    

    connection.commit()


def main():
    """
    user = your netlinkid
    password = your password, default is V00 number 
    host = as listed
    port as listed
    database = your netlinkid or "five_guys"
    """
    # user = "alecyang" 
    # password = "Apple1337"
    # host = "studentdb1.csc.uvic.ca"
    # port = "5432"
    # database = "five_guys"
    info = read_input_file("db.config")[0]
    print(info)
    try:
        connection = psycopg2.connect(user=info[0],
                                      password=info[1],
                                      host=info[2],
                                      port=info[3],
                                      database=info[4])
        
        # check what command is, if it is None or not one of the commands then repeat
        print("Welcome to this helper program for the five_guys' PostgreSQL Database project.")
        while (True):  # only break if we get the break input
            print("List of commands:")
            print("Enter b to build the database")
            print("Enter 1 to load data into the database")
            print("Enter 2 to insert data using data into the database")
            print("Enter 3 to delete data from the database")
            print("Enter 4 to update a table in the database")
            print("Enter 5 to drop tables")
            print("Enter 0 to exit this program")
            print("")
            command = input()
            if command == '0':
                print("Exiting")
                break
            elif command == '1':
                add_to_db(connection)
            elif command == '2':
                insert_db(connection)
            elif command == '3':
                delete_from_db(connection)
            elif command == '4':
                update_tables(connection)
            elif command == '5':
                drop_tables(connection)
            elif command == 'b':
                build_db(connection)
            else:
                print("Input invalid, please try again.")
    
    except (psycopg2.Error) as error:
        print("Error while connecting to PostgreSql", error)
        
    except (Exception) as error:
        print("program error", error)
        
    finally:
        # this closes the db connection
        if (connection):
            connection.close()
            print("PostgreSQL connection is closed")


if __name__ == "__main__":
    main()
