# Minify pTree size for each version

from tree import *
import json
from database_conn import connect_to_planetscale
import time

# TABLE NAMEs
INPUT_TABLE = 'jq_version'
OUTPUT_TABLE = 'jq_version_m'


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
    cursor.execute(f"SELECT `pTree`, `version` FROM {INPUT_TABLE};")
    res = cursor.fetchall()

    # Read pTrees from dataset
    for entry in res:
        pTree = Json2LT(json.loads(entry[0]))
        G.addt(LabeledTree(pTree, str(entry[1])))

    T1 = time.time()    # Timer starts

    # Minification
    G.get_equivalence()
    G.get_trees_metas()

    print('Get equivalence finished.')

    G.tree_size_reduction()
    G.get_mtrees_metas()

    print('Tree size reduction finished.')

    G.strict_supertree_set_minify()
    T2 = time.time()    # Timer ends

    print('Strict supertree set minification finished.')

    # Save minified pTrees to dataset
    for i in range(len(G.trees)):
        assert(len(G.trees) == len(G.mtrees))
        mTree = G.mtrees[i].root
        version = G.mtrees[i].name
        Sm = G.trees[i].Sm
        version_list = G.trees[i].eq_name_list

        mTree = LT2Json(mTree)

        sql = f'''INSERT INTO {OUTPUT_TABLE} 
                (pTree, size, depth, version, file_id, Sm, version_list) 
                VALUES (%s, %s, %s, %s, %s, %s, %s);'''
        val = (json.dumps(mTree), 0, 0, version, i + 1, json.dumps(list(Sm)), json.dumps(version_list))
        cursor.execute(sql, val)
        connection.commit()
        print(f'   Version {version} entry added to {OUTPUT_TABLE}.')
    
    print(f'Tree minification completed. Time spent: {(T2 - T1)} seconds.')