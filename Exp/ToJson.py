# Convert data from database to json for extension use

import json
from PlanetscaleConn import connect_to_planetscale

connection = connect_to_planetscale()
cursor = connection.cursor()

# TABLE NAMEs
SEP_TREE_TABLE = 'SepPT1'
COM_TREE_TABLE = 'ComPT1'
FILE_TABLE = 'DetectFile'

def toJson1():
    cursor.execute(f"SELECT root_name, content FROM {COM_TREE_TABLE};")
    res = cursor.fetchall()

    pt_dict = {}
    for entry in res:
        pt_dict[entry[0]] = json.loads(entry[1])
    with open('data/pt.json', "w") as outfile:
        outfile.write(json.dumps(pt_dict))


    cursor.execute(f"SELECT jsfile FROM {SEP_TREE_TABLE} ORDER BY id ASC;")
    res = cursor.fetchall()

    jsfile_list = []
    for entry in res:
        jsfile_list.append(entry[0])
    with open('data/jsfile_list.json', "w") as outfile:
        outfile.write(json.dumps(jsfile_list))

def toJson2():
    cursor.execute(f"SELECT libname, filename, url, version, deps, comment, id FROM {FILE_TABLE};")
    res = cursor.fetchall()

    file_dict = {}
    for entry in res:
        if entry[4] or entry[5]:
            # Skip deps and module
            continue
        file_dict[entry[6]] = {
            'libname': entry[0],
            'filename': entry[1],
            'url': entry[2],
            'version': entry[3],
        }
    
    with open('data/DetectFile.json', "w") as outfile:
        outfile.write(json.dumps(file_dict))


toJson2()
    
