from dotenv import load_dotenv
load_dotenv()
import os
import MySQLdb

def connect_to_planetscale():
    connection = MySQLdb.connect(
        host= os.getenv("DB_HOST"),
        user=os.getenv("DB_USERNAME"),
        passwd= os.getenv("DB_PASSWORD"),
        db= os.getenv("DB_NAME"),
        autocommit = True,
        ssl_mode = "VERIFY_IDENTITY",
        ssl      = {
            "ca": "/etc/ssl/cert.pem"
        }
    )
    return connection
