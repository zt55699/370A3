DROP TABLE IF EXISTS StudentContact;
DROP TABLE IF EXISTS TeacherContact; 
DROP TABLE IF EXISTS WorksheetHistory;
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Teachers;
DROP TABLE IF EXISTS Worksheets;

CREATE TABLE Students (
        studentID INTEGER PRIMARY KEY,
        mathOlympiads BOOLEAN NOT NULL,
        language VARCHAR(255) NOT NULL,
        level VARCHAR(255) NOT NULL,
        country VARCHAR(255) NOT NULL);

CREATE TABLE Teachers(
        employeeID INTEGER PRIMARY KEY,
        language VARCHAR(255) NOT NULL,
        expertise VARCHAR(255) NOT NULL,
        availability VARCHAR(2048) NOT NULL);

CREATE TABLE Worksheets(
        title VARCHAR(255) PRIMARY KEY,
        author VARCHAR(255),
        level VARCHAR(255) NOT NULL,
        url VARCHAR(255) UNIQUE,
        subject VARCHAR(255) NOT NULL);

CREATE TABLE WorksheetHistory(
        studentID INTEGER NOT NULL,
        employeeID INTEGER NOT NULL,
        title VARCHAR(255) NOT NULL,
        mark NUMERIC(3,2) NOT NULL, 
        comment VARCHAR(2048),
        PRIMARY KEY(studentID, title),
        FOREIGN KEY (studentID) REFERENCES Students(studentID) ON DELETE CASCADE,
        FOREIGN KEY (employeeID) REFERENCES Teachers(employeeID) ON DELETE CASCADE,
        FOREIGN KEY (title) REFERENCES Worksheets(title) ON DELETE CASCADE);

CREATE TABLE StudentContact ( 
        id INTEGER PRIMARY KEY,
        name VARCHAR NOT NULL,
        email VARCHAR(255) NOT NULL,
        skype VARCHAR(255),
        phone VARCHAR(25),
        FOREIGN KEY (id) REFERENCES Students(studentID) ON DELETE CASCADE);

CREATE TABLE TeacherContact ( 
        id INTEGER PRIMARY KEY,
        name VARCHAR NOT NULL,
        email VARCHAR(255) NOT NULL,
        skype VARCHAR(255),
        phone VARCHAR(25),
        FOREIGN KEY (id) REFERENCES Teachers(employeeID) ON DELETE CASCADE);




