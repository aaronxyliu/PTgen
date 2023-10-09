from database_conn import connect_to_planetscale



connection = connect_to_planetscale()



try:
    # Create a cursor to interact with the database
    cursor = connection.cursor()

    # Execute "SHOW TABLES" query
    cursor.execute("SHOW TABLES")

    # Fetch all the rows
    tables = cursor.fetchall()

    # Print out the tables
    print("Tables in the database:")
    for table in tables:
        print(table[0])

except MySQLdb.Error as e:
    print("MySQL Error:", e)

finally:
    # Close the cursor and connection
    cursor.close()
    connection.close()


