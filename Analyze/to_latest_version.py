# Extract latest version of JS libs

from dotenv import load_dotenv
load_dotenv()
import MySQLdb
import json

connection = MySQLdb.connect(
  host= 'us-east.connect.psdb.cloud',
  user='yain51suytl8vm1cm4b2',
  passwd= 'pscale_pw_pEiVDtydTJqIpuJ68NRKenF0ncp6jjYipJkfxFDIHDN',
  db= 'js-lib-detect-trees',
  ssl_mode = "VERIFY_IDENTITY",
  ssl      = {
    #"ca": "/etc/ssl/cert.pem"   # For Mac
    "ca": "/etc/ssl/certs/ca-certificates.crt"  # For Linux
  }
)

cursor = connection.cursor()
cursor.execute("SELECT name FROM AllLibs;")
libnames = cursor.fetchall()

cnt = 0
for entry in libnames:
    libname = entry[0]
    
    cursor.execute(f"SELECT jsfiles FROM AllLibs WHERE name = '{libname}';")
    json_str= cursor.fetchone()[0]
    file_collection = json.loads(json_str)

    latest_files = []
    for i in range(len(file_collection)-1, -1, -1):
      files = file_collection[i][1]
      if len(files) > 0:
        latest_files = files
        break
    
    sql = "UPDATE AllLibs SET latest_version_files = %s, latest_version_file_number = %s WHERE name = %s;"
    val = (json.dumps(latest_files), len(latest_files), libname)
    cursor.execute(sql, val)
    connection.commit()

    cnt += 1
    print(f'{cnt}: {libname} updated.')
    

connection.close()
# CREATE TABLE jslibs_lastest (
# 	name VARCHAR(255) NOT NULL,
# 	version VARCHAR(255),
# 	file_num INT,
# 	file_list JSON, 
#   PRIMARY KEY (name)
# );