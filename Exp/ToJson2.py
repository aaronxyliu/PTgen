# Convert data from database to json for extension use

import json
import pickle


# open a file, where you stored the pickled data
file = open('data/crawler4_res.pkl', 'rb')

# dump information to that file
data = pickle.load(file)

# close the file
file.close()


def toJson2():

    file_dict = {}
    cnt = 1
    for v_info in data:
        file_dict[cnt] = {
            'libname': 'jQuery',
            'filename': 'jquery.min.js',
            'url': f"https://cdnjs.cloudflare.com/ajax/libs/jquery/{v_info['version']}/jquery.min.js",
            'version': v_info['version'],
            'in_deps': [],
            'out_deps': [],
        }
        cnt += 1
    
    with open('data/DetectFile.json', "w") as outfile:
        outfile.write(json.dumps(file_dict))

if __name__ == '__main__':
    toJson2()
    print('Complete')
    
