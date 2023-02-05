from urllib.request import urlopen
import json
from dotenv import load_dotenv
load_dotenv()
import MySQLdb

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


with open('data/accuracy_libs.json', 'r') as openfile:
  lib_list = json.load(openfile)


for lib_name in lib_list:
  print(lib_name)
  res1 = urlopen(f'https://api.cdnjs.com/libraries/{lib_name}?fields=version')
  latest_version = json.loads(res1.read())['version']

  res2 = urlopen(f'https://api.cdnjs.com/libraries/{lib_name}/{latest_version}?fields=files')
  file_list = json.loads(res2.read())['files']

  js_list = []
  for file in file_list:
    # Only consider minified js files
    if file[-6:] == 'min.js' or file[-4:] == '.mjs':
      js_list.append(file)

  sql = "UPDATE AccuLibs2 SET latest_version = %s, latest_version_files = %s WHERE name = %s;"
  val = (latest_version, json.dumps(js_list), lib_name)
  cursor.execute(sql, val)
  connection.commit()


connection.close()



# res = urlopen('https://api.cdnjs.com/libraries/vue/2.6.11?fields=files')

# print(json.loads(res.read()))