from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()
import os
import MySQLdb

def connect_to_planetscale():
    # Connect to the database
    connection = MySQLdb.connect(
    host=os.getenv("DATABASE_HOST"),
    user=os.getenv("DATABASE_USERNAME"),
    passwd=os.getenv("DATABASE_PASSWORD"),
    db=os.getenv("DATABASE"),
    autocommit=True,
    ssl_mode="VERIFY_IDENTITY",
    # See https://planetscale.com/docs/concepts/secure-connections#ca-root-configuration
    # to determine the path to your operating systems certificate file.
    ssl={ "ca": "/etc/ssl/cert.pem" }
    )
    return connection

