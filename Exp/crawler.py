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
# CREATE TABLE `AllLibs` (
# 	`name` varchar(255) NOT NULL,
# 	`version_num` int,
# 	`jsfile_num` int,
# 	`description` varchar(512),
# 	`jsfiles` json,
# 	`url` varchar(255),
# 	PRIMARY KEY (`name`)
# )



# cdnjs API manual: https://cdnjs.com/api

# First, get all library list
res1 = urlopen('https://api.cdnjs.com/libraries')
all_libs = json.loads(res1.read())

print(f'''Total library: {all_libs['available']}''')

cnt = 0
start = True
for lib_info in all_libs['results']:
    lib_name = lib_info['name']
    # print(lib_name)
    cnt += 1

    if start:
      try:
        print(f'{cnt}: {lib_name} started.')
        # Get library's all versions
        res2 = urlopen(f'https://api.cdnjs.com/libraries/{lib_name}?fields=description,repository,versions')
        res2_object = json.loads(res2.read())
        version_list = res2_object['versions']
        dscp = res2_object['description']
        url = ''
        if res2_object['repository'] and res2_object['repository']['url']:
          url = res2_object['repository']['url']


        file_collection = []

        version_num = 0
        file_num = 0
        for version in version_list:
            if version[0] == '0':
                # Skip experimental versions
                continue
            
            version_num += 1
            
            js_list = []
            res3 = urlopen(f'https://api.cdnjs.com/libraries/{lib_name}/{version}?fields=files')
            file_list = json.loads(res3.read())['files']

            for file in file_list:
                # Only consider minified js files
                if file[-6:] == 'min.js' or file[-4:] == '.mjs':
                    js_list.append(file)
                    file_num += 1
            
            file_collection.append((version, js_list))
            

        json_str = json.dumps(file_collection)

        sql = "INSERT INTO AllLibs VALUES (%s, %s, %s, %s, %s, %s);"
        val = (lib_name, version_num, file_num, dscp, json_str, url)
        cursor.execute(sql, val)
        connection.commit()
        print(f'{cnt}: {lib_name} finished. {version_num} versions and {file_num} JS files in total.')

      except:
        # Save error to the log
        with open('data/error_lib.log', "w") as outfile:
          outfile.write(lib_name)

    # if lib_name == 'survey-jquery':
    #   start = True




connection.close()



# res = urlopen('https://api.cdnjs.com/libraries/vue/2.6.11?fields=files')

# print(json.loads(res.read()))