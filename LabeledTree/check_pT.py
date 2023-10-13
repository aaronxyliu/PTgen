# Minify pTree size for each version

from tree import *
import json
from database_conn import connect_to_planetscale
import time

# TABLE NAMEs
# INPUT_TABLE = 'jq_version'
# OUTPUT_TABLE = 'jq_version_m'

INPUT_TABLE = 'jqueryui_version'


connection = connect_to_planetscale()
cursor = connection.cursor()


def Json2LT(root, par_v=None):
    '''
    Convert JSON object to the labeled tree data structure defined in tree.py

    Parameters:
        root - the root of the JSON tree
        par_v - parent vertex in "Vertex" type

    Output:
        root of the new tree in "Vertex" type
    '''
    if not root:
        return None
    v = Vertex(root['n'], root['d'])
    if par_v:
        par_v.addc(v)
    for child in root['c']:
        Json2LT(child, v)
    return v


def LT2Json(root, par_v=None):
    '''
    Convert the labeled tree back to JSON object

    Parameters:
        root - the root of the labeled tree
        par_v - parent vertex in JSON object type

    Output:
        root of the new tree in JSON object type
    '''
    if not root:
        return None
    assert(isinstance(root, Vertex))
    v_obj = {
        'n': root.name,
        'd': root.label,
        'c':[]
    }
    if par_v:
        par_v['c'].append(v_obj)
    for child in root.children:
        LT2Json(child, v_obj)
    return v_obj



if __name__ == '__main__':
    G = Gamma()
    cursor.execute(f"SELECT `pTree` FROM {INPUT_TABLE} WHERE `version`='1.10.0';")
    res = cursor.fetchone()

    pTree1 = LabeledTree(Json2LT(json.loads(res[0])), 'T1')
    
    cursor.execute(f"SELECT `pTree` FROM {INPUT_TABLE} WHERE `version`='1.8.16';")
    res = cursor.fetchone()

    pTree2 = LabeledTree(Json2LT(json.loads(res[0])), 'T2')

    if pTree1 == pTree2:
        print('yes')
    else:
        print('false')
    exit(0)

   