from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
import os
import MySQLdb

def connect_to_planetscale():
    # Connect to the database
    connection = MySQLdb.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USERNAME"),
        passwd=os.getenv("DB_PASSWORD"),
        db=os.getenv("DB_NAME"),
        autocommit=True,
        ssl_mode="VERIFY_IDENTITY",
        # See https://planetscale.com/docs/concepts/secure-connections#ca-root-configuration
        # to determine the path to your operating systems certificate file.
        ssl={ "ca": "/etc/ssl/cert.pem" }
    )
    return connection

# try:
#     # Create a cursor to interact with the database
#     cursor = connection.cursor()

#     # Execute "SHOW TABLES" query
#     cursor.execute("SHOW TABLES")

#     # Fetch all the rows
#     tables = cursor.fetchall()

#     # Print out the tables
#     print("Tables in the database:")
#     for table in tables:
#         print(table[0])

# except MySQLdb.Error as e:
#     print("MySQL Error:", e)

# finally:
#     # Close the cursor and connection
#     cursor.close()
#     connection.close()


