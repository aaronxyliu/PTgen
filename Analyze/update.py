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
    "ca": "/etc/ssl/cert.pem"   # For Mac
    #"ca": "/etc/ssl/certs/ca-certificates.crt"  # For Linux
  }
)

cursor = connection.cursor()

def update_lib_file_no():
  cursor.execute(f"SELECT libname FROM DetectLib;")
  libs = cursor.fetchall()
  for entry in libs:
      libname = entry[0]
      cursor.execute(f"SELECT count(*) FROM DetectFile WHERE libname='{libname}';")
      res = cursor.fetchone()
      cursor.execute(f"UPDATE DetectLib SET file_no={res[0]} WHERE libname='{libname}';")
      connection.commit()

def sum_lib_file_no():
  cnt = 0
  cursor.execute(f"SELECT file_no FROM DetectLib;")
  libs = cursor.fetchall()
  for entry in libs:
    cnt += entry[0]
  print(cnt)

if __name__ == '__main__':
  sum_lib_file_no()


connection.close()

# CREATE TABLE Top100Libs SELECT * FROM AllLibs WHERE github_star >= 26219
