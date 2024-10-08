### Generate credit object trees

from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import text_to_be_present_in_element
import json
from database_conn import connect_to_planetscale
from TreeCredit import CreditCalculator


### =================
### Username: oxc4nocsf36d3y3n66t5
### Password: pscale_pw_tR7bje9m71xCckmZLy9q4eoQAdd2hYzgVqBB2sI4rCr

connection = connect_to_planetscale()
cursor = connection.cursor()

service = Service(executable_path="./bin/chromedriver")
driver = webdriver.Chrome()
# driver = webdriver.Chrome(service=service)

# TABLE NAMEs
SEP_TREE_TABLE = 'jqueryui_version'

MAX_DEPTH=4
MAX_NODE=1000

TRIM_DEPTH = MAX_DEPTH                                                                          
TRIM_NODE = MAX_NODE

BLACK_LIST = []
# password: ain-2023-10-05-f4fczz

def errMsg(msg):
    return f'\033[1;31mERROR: {msg}\033[0m'


def generatePT(file_index, route):
    driver.get(f"http://127.0.0.1:6543/{route}/{file_index}")

    error_div = driver.find_element(By.ID, 'js-errors')
    if error_div.text:
        # Failed to load the library
        print(f"    {errMsg(f'{file_index} >> {error_div.text}')}")
        return None, 0, 0, ''
        

    driver.execute_script(f'createObjectTree({MAX_DEPTH}, {MAX_NODE}, true);')

    WebDriverWait(driver, timeout=20).until(text_to_be_present_in_element((By.ID, "obj-tree"), '{'))
    version = driver.find_element(By.ID, 'version').text
    tree_json = driver.find_element(By.ID, 'obj-tree').text
    tree = json.loads(tree_json)
    circle_num = int(driver.find_element(By.ID, 'circle-num').text)
    size = int(driver.find_element(By.ID, 'tree-size').text)
    # depth = int(driver.find_element(By.ID, 'tree-depth').text)

    # Remove Global Varabile in Blacklist
    del_index = []
    for i in range(len(tree['children'])):
        if tree['children'][i]['name'] in BLACK_LIST:
            del_index.append(i)
    offset = 0
    for index in del_index:
        del tree['children'][index - offset]
        offset += 1


    return tree, size, circle_num, version


def treeDiff(tree1, tree2):
    # Return tree2 - tree1
    if tree1 == None or tree2 == None:
        return None
    
    diff_tree = {'name': 'window', 'dict': {}, 'children': []}
    q1 = []
    q2 = []
    q3 = []
    q1.append(tree1)
    q2.append(tree2)
    q3.append([])

    while len(q2): 
        node1 = q1.pop(0)
        node2 = q2.pop(0)
        path = q3.pop(0)

        for child_node2 in node2['children']:
            find_same_child = False

            for child_node1 in node1['children']:
                if child_node1['name'] == child_node2['name']:
                    find_same_child = True
                    q1.append(child_node1)
                    q2.append(child_node2)
                    q3.append(path[:])
                    q3[len(q3) - 1].append(child_node1['name'])
                    break

            if not find_same_child:
                child_node2['path'] = path[:]
                diff_tree['children'].append(child_node2)
    
    return diff_tree

def SameDict(d1, d2):
    for k, v in d1.items():
        if not k in d2:
            return False
        if d2[k] != v:
            return False
    return True

def elimRandom(tree1, tree2):
    # Eliminate random nodes - remove nodes that different in two trees.
    if tree1 == None or tree2 == None:
        return None
    ret_tree = {'name': 'window', 'dict': {}, 'children': []}
    elim_num = 0
    
    q1 = []
    q2 = []
    q3 = []
    q1.append(tree1)
    q2.append(tree2)
    q3.append(ret_tree)

    while len(q3): 
        node1 = q1.pop(0)
        node2 = q2.pop(0)
        node3 = q3.pop(0)

        for child_node1 in node1['children']:
            find_same = False
            for child_node2 in node2['children']:
                if child_node1['name'] == child_node2['name'] and SameDict(child_node1['dict'], child_node2['dict']):
                    # Identical nodes
                    find_same = True
                    q1.append(child_node1)
                    q2.append(child_node2)
                    new_node = {'name': child_node2['name'], 'dict': child_node1['dict'], 'children': []}
                    node3['children'].append(new_node)
                    q3.append(new_node)
                    break

            if not find_same:
                elim_num += 1
    
    return ret_tree, elim_num

def limitGlobalV(tree, vlist):
    ret_tree = {'name': 'window', 'dict': {}, 'children': []}
    for child in tree['children']:
        if child['name'] in vlist:
            ret_tree['children'].append(child)
    return ret_tree
    


def updateOne(file_index, limit_globalV=[]):
    pt1, size1, circle_num1, version = generatePT(file_index, 'deps')
    pt2, size2, circle_num2, _ = generatePT(file_index, 'test')
    pt3, size3, circle_num3, _ = generatePT(file_index, 'test')

    if pt1 and pt2 and pt3:
        pt_stable, random_num = elimRandom(pt2, pt3)
        if limit_globalV != None and len(limit_globalV) > 0:
            pt_stable = limitGlobalV(pt_stable, limit_globalV)
        pt = treeDiff(pt1, pt_stable)
        CC = CreditCalculator(TRIM_DEPTH, TRIM_NODE, MAX_DEPTH)
        size, depth = CC.algorithm1(pt)
        pt = CC.expand(pt)
        CC.minifyTreeSpace(pt)

        # Add pt to SepTreeTABLE dataTABLE
        globalV = []
        for subtree in pt['c']:
            globalV.append(subtree['n'])
        

        # Create table if not exist
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS `{SEP_TREE_TABLE}` (
            `pTree` json DEFAULT NULL,
            `globalV_num` int DEFAULT NULL,
            `globalV` json DEFAULT NULL,
            `size` int DEFAULT NULL,
            `circle_num` int DEFAULT NULL,
            `depth` int DEFAULT NULL,
            `file_id` bigint unsigned NOT NULL,
            `random_num` int DEFAULT NULL,
            `version` varchar(100) DEFAULT NULL,
            UNIQUE KEY `id` (`file_id`)
            );''')
        connection.commit()


        # If entry already exists, delete first
        cursor.execute(f"SELECT size FROM {SEP_TREE_TABLE} WHERE file_id = '{file_index}';")
        res = cursor.fetchone()
        if res:  
            cursor.execute(f"DELETE FROM {SEP_TREE_TABLE} WHERE file_id = '{file_index}';")
            connection.commit()

        # Create new entry in SEP_TREE_TABLE
        sql = f'''INSERT INTO {SEP_TREE_TABLE} 
                (pTree, size, depth, globalV, globalV_num, circle_num, file_id, random_num, version) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);'''
        val = (json.dumps(pt), size, depth, json.dumps(globalV), len(globalV), circle_num2 - circle_num1, int(file_index), random_num, str(version))
        cursor.execute(sql, val)
        connection.commit()
        print(f'    {file_index} entry added to {SEP_TREE_TABLE}.')
    


def updateAll(start_id = 0):

    with open('data/DetectFile.json', 'r') as openfile:
        file_list = json.load(openfile)

    start = False
    for file_index in file_list:
        if int(file_index) >= start_id:
            start = True
        if not start:
            continue

        lib_name = file_list[file_index]['libname']
        file_name = file_list[file_index]['filename']

        print(f'  \033[1;32m{file_index} {lib_name} {file_name}:\033[0m')
        updateOne(file_index)

            

            

if __name__ == '__main__':
    # updateOne(17)
    updateAll()
    driver.close()
    connection.close()




