# Crawl all jQuery files under each version

from urllib.request import urlopen
import json
import pickle

LIB_NAME = 'jqueryui'

res1 = urlopen(f'https://api.cdnjs.com/libraries/{LIB_NAME}')
jq_info = json.loads(res1.read())

file_list = []
for version in jq_info['versions']:
    res2 = urlopen(f'https://api.cdnjs.com/libraries/{LIB_NAME}/{version}')
    v_info = json.loads(res2.read())
    file_list.append({
        'version': version,
        'files': v_info['files']
    })

    print(f"{version}:    {str(v_info['files'])}")

save_path = 'data/crawler4_res.pkl'
file = open(save_path, 'wb')
pickle.dump(file_list, file)
file.close()

print(f'Results saved to {save_path}')