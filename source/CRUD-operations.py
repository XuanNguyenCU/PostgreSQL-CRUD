import psycopg2, datetime


# Read
def getAllStudents(table):
    """
    Retrieves and displays all records from the 'students' table.
    """

    table.execute("SELECT * FROM students")
    print("student_id, first_name, last_name, email, enrollment_date")

    for record in table:
        print(", ".join(map(str, record)))

    print()


# Create
def addStudent(connection, cursor):
    """
    Inserts a new student record into the 'students' table.
    """

    first_name = input("Enter their First Name: ")
    last_name = input("Enter their Last Name: ")
    email = input("Enter their email: ")
    enrollment_date = input("Enter their Enrollment Date (in this format 2023-01-31): ")

    try:
        cursor.execute("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s)",
                       (first_name, last_name, email, datetime.date.fromisoformat(enrollment_date)))
        
        connection.commit()
        print(f"Successfully created new student: {first_name} {last_name}\n")

    except Exception as added_failed:
        print("ERROR! Failed to create new student: " + str(added_failed))


# Update
def updateStudentEmail(connection, cursor):
    """
    Updates the email address for a student with the specified student_id.
    """

    student_id = input("Enter the ID of the desired student: ")
    new_email = input("Enter the student's new email address: ")

    try:
        cursor.execute("""
        UPDATE students
        SET email = (%s)
        WHERE student_id = (%s) """, 
        
        (new_email, student_id))
        connection.commit()

        if cursor.statusmessage.split()[1] == '0':
            print(f"Failed to find student with ID: {student_id}\n")

        else:
            print(f"Successfully updated student with ID: {student_id}\n")

    except Exception as update_failed:
        print("ERROR! Failed to update student: " + str(update_failed))


# Delete
def deleteStudent(connection, cursor):
    """
    Deletes the record of the student with the specified student_id.
    """

    student_id = input("Enter the ID of the student that will get deleted: ")

    try:
        cursor.execute("DELETE FROM students WHERE student_id = (%s)", (student_id,))
        
        connection.commit()

        if cursor.statusmessage.split()[1] == "0":
            print(f"Failed to find student with ID: {student_id}\n")

        else:
            print(f"Successfully deleted student with ID: {student_id}\n")

    except Exception as deleted_failed:
        print("ERROR! Failed to delete student: " + str(deleted_failed))


def main():
    database = input("Enter the database name: ")
    username = input("Enter the user name: ")
    password = input("Enter the password: ")

    with psycopg2.connect(dbname=database, user=username, password=password) as connection:

        print(
        """
        Select one of the following options:

            1. Get all students / Prints the entire 'students' table
            2. Add a new student
            3. Update the email of a current student
            4. Delete a student
            Press 'Q' or 'quit' to exit the program.
        """)

        with connection.cursor() as cursor:
            while True:
                result = input("> ")
                result_lower = result.lower()

                if result_lower == "1":
                    getAllStudents(cursor)

                elif result_lower == "2":
                    addStudent(connection, cursor)

                elif result_lower == "3":
                    updateStudentEmail(connection, cursor)

                elif result_lower == "4":
                    deleteStudent(connection, cursor)

                elif result_lower in ["q", "quit"]:
                    break

                else:
                    print("Invalid option, please try again.")

        print("Disconnected successfully.")
        

# main guard
if __name__ == "__main__":
    main()
