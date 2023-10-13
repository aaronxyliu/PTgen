# Convert data from database to json for extension use

import json
import pickle


# open a file, where you stored the pickled data
file = open('data/crawler4_res.pkl', 'rb')

# dump information to that file
data = pickle.load(file)

# close the file
file.close()


def toJson2_jQuery():
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

def toJson2_LoDash():
    file_dict = {}
    cnt = 1
    FILE_NAME = 'lodash.min.js'
    LIB_NAME = 'lodash.js'
    for v_info in data:
        if FILE_NAME not in v_info['files']:
            print(f"file is not found in {v_info['version']}")
            continue
        file_dict[cnt] = {
            'libname': 'LoDash',
            'filename': FILE_NAME,
            'url': f"https://cdnjs.cloudflare.com/ajax/libs/{LIB_NAME}/{v_info['version']}/{FILE_NAME}",
            'version': v_info['version'],
            'in_deps': [],
            'out_deps': [],
        }
        cnt += 1
    with open('data/DetectFile.json', "w") as outfile:
        outfile.write(json.dumps(file_dict))

def toJson2_Underscore():
    file_dict = {}
    cnt = 1
    FILE_NAMES = ['underscore-min.js', 'underscore-esm-min.js']
    LIB_NAME = 'underscore.js'
    for v_info in data:
        fname_found = False
        for fname in FILE_NAMES:
            if fname in v_info['files']:
                file_dict[cnt] = {
                    'libname': LIB_NAME,
                    'filename': fname,
                    'url': f"https://cdnjs.cloudflare.com/ajax/libs/{LIB_NAME}/{v_info['version']}/{fname}",
                    'version': v_info['version'],
                    'in_deps': [],
                    'out_deps': [],
                }
                fname_found = True
                cnt += 1
                break
        if not fname_found:
            print(f"file is not found in {v_info['version']}")

    with open('data/DetectFile.json', "w") as outfile:
        outfile.write(json.dumps(file_dict))

def toJson2_corejs():
    file_dict = {}
    cnt = 1
    FILE_NAMES = ['core.min.js', 'minified.js']
    LIB_NAME = 'core-js'
    for v_info in data:
        fname_found = False
        for fname in FILE_NAMES:
            if fname in v_info['files']:
                file_dict[cnt] = {
                    'libname': LIB_NAME,
                    'filename': fname,
                    'url': f"https://cdnjs.cloudflare.com/ajax/libs/{LIB_NAME}/{v_info['version']}/{fname}",
                    'version': v_info['version'],
                    'in_deps': [],
                    'out_deps': [],
                }
                fname_found = True
                cnt += 1
                break
        if not fname_found:
            print(f"file is not found in {v_info['version']}")

    with open('data/DetectFile.json', "w") as outfile:
        outfile.write(json.dumps(file_dict))

def toJson2_requirejs():
    file_dict = {}
    cnt = 1
    FILE_NAMES = ['require.min.js']
    LIB_NAME = 'require.js'
    for v_info in data:
        fname_found = False
        for fname in FILE_NAMES:
            if fname in v_info['files']:
                file_dict[cnt] = {
                    'libname': LIB_NAME,
                    'filename': fname,
                    'url': f"https://cdnjs.cloudflare.com/ajax/libs/{LIB_NAME}/{v_info['version']}/{fname}",
                    'version': v_info['version'],
                    'in_deps': [],
                    'out_deps': [],
                }
                fname_found = True
                cnt += 1
                break
        if not fname_found:
            print(f"file is not found in {v_info['version']}")

    with open('data/DetectFile.json', "w") as outfile:
        outfile.write(json.dumps(file_dict))

def toJson2_momentjs():
    file_dict = {}
    cnt = 1
    FILE_NAMES = ['moment.min.js']
    LIB_NAME = 'moment.js'
    for v_info in data:
        fname_found = False
        for fname in FILE_NAMES:
            if fname in v_info['files']:
                file_dict[cnt] = {
                    'libname': LIB_NAME,
                    'filename': fname,
                    'url': f"https://cdnjs.cloudflare.com/ajax/libs/{LIB_NAME}/{v_info['version']}/{fname}",
                    'version': v_info['version'],
                    'in_deps': [],
                    'out_deps': [],
                }
                fname_found = True
                cnt += 1
                break
        if not fname_found:
            print(f"file is not found in {v_info['version']}")

    with open('data/DetectFile.json', "w") as outfile:
        outfile.write(json.dumps(file_dict))

def toJson2_hammerjs():
    file_dict = {}
    cnt = 1
    FILE_NAMES = ['hammer.min.js']
    LIB_NAME = 'hammer.js'
    for v_info in data:
        fname_found = False
        for fname in FILE_NAMES:
            if fname in v_info['files']:
                file_dict[cnt] = {
                    'libname': LIB_NAME,
                    'filename': fname,
                    'url': f"https://cdnjs.cloudflare.com/ajax/libs/{LIB_NAME}/{v_info['version']}/{fname}",
                    'version': v_info['version'],
                    'in_deps': [],
                    'out_deps': [],
                }
                fname_found = True
                cnt += 1
                break
        if not fname_found:
            print(f"file is not found in {v_info['version']}")

    with open('data/DetectFile.json', "w") as outfile:
        outfile.write(json.dumps(file_dict))

def toJson2_jqui():
    file_dict = {}
    cnt = 1
    FILE_NAMES = ['jquery-ui.min.js']
    LIB_NAME = 'jqueryui'
    for v_info in data:
        fname_found = False
        for fname in FILE_NAMES:
            if fname in v_info['files']:
                file_dict[cnt] = {
                    'libname': LIB_NAME,
                    'filename': fname,
                    'url': f"https://cdnjs.cloudflare.com/ajax/libs/{LIB_NAME}/{v_info['version']}/{fname}",
                    'version': v_info['version'],
                    'in_deps': [],
                    'out_deps': ['https://cdnjs.cloudflare.com/ajax/libs/jquery/1.8.0/jquery.min.js'],
                }
                fname_found = True
                cnt += 1
                break
        if not fname_found:
            print(f"file is not found in {v_info['version']}")

    with open('data/DetectFile.json', "w") as outfile:
        outfile.write(json.dumps(file_dict))

if __name__ == '__main__':
    toJson2_jqui()
    print('Complete')
    
