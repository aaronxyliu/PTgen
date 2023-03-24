# Convert data from database to json for extension use

import json
from PlanetscaleConn import connect_to_planetscale

connection = connect_to_planetscale()
cursor = connection.cursor()

# TABLE NAMEs
# SEP_TREE_TABLE = 'SepPT_5_50'
COM_TREE_TABLE = 'ComPT_5_50'
# FILE_TABLE = 'DetectFile'
FILE_TABLE = 'Lodash'

def toJson1():
    cursor.execute(f"SELECT root_name, content FROM {COM_TREE_TABLE};")
    res = cursor.fetchall()

    pt_dict = {}
    for entry in res:
        pt_dict[entry[0]] = json.loads(entry[1])
    with open('data/pts.json', "w") as outfile:
        outfile.write(json.dumps(pt_dict))


    # cursor.execute(f"SELECT jsfile FROM {SEP_TREE_TABLE} ORDER BY id ASC;")
    # res = cursor.fetchall()

    # jsfile_list = []
    # for entry in res:
    #     jsfile_list.append(entry[0])
    # with open('data/jsfile_list.json', "w") as outfile:
    #     outfile.write(json.dumps(jsfile_list))

def toJson2():
    cursor.execute(f"SELECT libname, filename, url, version, in_deps, out_deps, comment, id FROM {FILE_TABLE};")
    res = cursor.fetchall()

    file_dict = {}
    for entry in res:
        if entry[6]:
            # Skip module
            continue
        file_dict[entry[7]] = {
            'libname': entry[0],
            'filename': entry[1],
            'url': entry[2],
            'version': entry[3],
            'in_deps': json.loads(entry[4]) if entry[4] else [],
            'out_deps': json.loads(entry[5]) if entry[5] else [],
        }
    
    with open('data/DetectFile.json', "w") as outfile:
        outfile.write(json.dumps(file_dict))

if __name__ == '__main__':
    toJson2()
    print('Complete')
    
