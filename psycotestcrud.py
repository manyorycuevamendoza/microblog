import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(user="postgres", password="UTEC", database="postgres", host="localhost", port="5432")


    cursor = connection.cursor()
    # Executing a SQL query to insert data into  table
    cursor.execute("SELECT * from class")
    record = cursor.fetchall()
    print("Result ", record)

    insert_query = """ INSERT INTO class (name, id, code, room) VALUES ('Programacion I', '5', 'CS1111', 'M801')"""
    cursor.execute(insert_query)
    connection.commit()
    print("1 Record inserted successfully")
    # Fetch result
    cursor.execute("SELECT * from class")
    record = cursor.fetchall()
    print("Result ", record)

    # Executing a SQL query to update table
    update_query = """Update class set room = 'A803' where id = 5"""
    cursor.execute(update_query)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record updated successfully ")
    # Fetch result
    cursor.execute("SELECT * from class")
    print("Result ", cursor.fetchall())

    # Executing a SQL query to delete table
    delete_query = """Delete from class where id = 5"""
    cursor.execute(delete_query)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record deleted successfully ")
    # Fetch result
    cursor.execute("SELECT * from class")
    print("Result ", cursor.fetchall())


except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")