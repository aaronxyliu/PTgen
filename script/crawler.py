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
    "ca": "/etc/ssl/cert.pem"
  }
)

# cdnjs API manual: https://cdnjs.com/api

# First, get all library list
res1 = urlopen('https://api.cdnjs.com/libraries')
all_libs = json.loads(res1.read())

print(f'''Total library: {all_libs['available']}''')

for lib_info in all_libs['results']:
    lib_name = lib_info['name']
    # Get library's all versions
    res2 = urlopen(f'https://api.cdnjs.com/libraries/{lib_name}?fields=versions')
    version_list = json.loads(res2.read())['versions']


    files_dict = {}
    for version in version_list:
        if version[0] == '0':
            # Skip experimental versions
            continue
        
        files_dict[version] = []
        res3 = urlopen(f'https://api.cdnjs.com/libraries/{lib_name}/{version}?fields=files')
        file_list = json.loads(res3.read())['files']

        for file in file_list:
            # Only consider minified js files
            if file[-6:] == 'min.js' or file[-4:] == '.mjs':
                files_dict[version].append(file)
    
    json_str = json.dumps(files_dict)




# res = urlopen('https://api.cdnjs.com/libraries/vue/2.6.11?fields=files')

# print(json.loads(res.read()))