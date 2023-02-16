### Combine pTree with same root name together 

import json
from PlanetscaleConn import connect_to_planetscale

# Connect to PlanetScale dataTABLE
connection = connect_to_planetscale()
cursor = connection.cursor()

# TABLE NAMEs
SEP_TREE_TABLE = 'SepPT_5_50'
COM_TREE_TABLE = 'ComPT_5_50'


def SameDict(d1, d2):
    for k, v in d1.items():
        if not k in d2:
            return False
        if d2[k] != v:
            return False
    return True


def combine (t, pt, file_id):
    # Combine t into exisiting pt
    if t == None or pt == None:
        return
    q = []
    qc = []
    q.append(t)
    qc.append(pt)

    while len(q): 
        node_t = q.pop(0)
        node_pt = qc.pop(0)

        if node_t['n'] != node_pt['n']:
            print('Error when BFS.')
            exit(0)

        find_d_item = False
        file_tag_obj = {'F': file_id - 1, 'x': node_t['x']}   # Serial id starts from 1
        for d_item in node_pt['d']:
            if SameDict(d_item['d'], node_t['d']):
                # Type and Value equal
                find_d_item = True
                d_item['Ls'].append(file_tag_obj)
                break                  
        
        if not find_d_item:
            node_pt['d'].append({'d': node_t['d'], 'Ls': [file_tag_obj]})
        
        for child_t in node_t['c']:
            q.append(child_t)
            find_same_child = False

            for child_pt in node_pt['c']:
                if child_pt['n'] == child_t['n']:
                    find_same_child = True
                    qc.append(child_pt)
                    break

            if not find_same_child:
                new_node = {'n': child_t['n'], 'd': [], 'c': []}
                node_pt['c'].append(new_node)
                qc.append(new_node)
    


def combineAll():
    # First clear the COMP_TREE_TABLE
    cursor.execute(f"TRUNCATE TABLE {COM_TREE_TABLE};")
    connection.commit()

    # Extract all pTree from SEP_TREE_TABLE
    cursor.execute(f"SELECT file_id, pTree FROM {SEP_TREE_TABLE};")
    res = cursor.fetchall()

    for entry in res:
        id = entry[0]
        tree = json.loads(entry[1])
        
        for subtree in tree['c']:
            subtree_name = subtree['n']
            cursor.execute(f"SELECT content FROM {COM_TREE_TABLE} WHERE root_name = '{subtree_name}';")
            res = cursor.fetchone()
            
            if res:
                pt = json.loads(res[0])
                combine(subtree, pt, id)
                sql = f"UPDATE {COM_TREE_TABLE} SET content = %s WHERE root_name = %s;"
                val = (json.dumps(pt), subtree_name)
                cursor.execute(sql, val)
                connection.commit()
            else:
                pt = {'n': subtree_name, 'd': [], 'c': []}
                combine(subtree, pt, id)
                sql = f"INSERT INTO {COM_TREE_TABLE} (root_name, content) VALUES (%s, %s);"
                val = (subtree_name, json.dumps(pt))
                cursor.execute(sql, val)
                connection.commit()
        
        print(f'{id}: combination finished.')
        

            

            

if __name__ == '__main__':
    combineAll()
    connection.close()




