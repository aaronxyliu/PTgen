### Generate credit object trees

from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import text_to_be_present_in_element
import json
from PlanetscaleConn import connect_to_planetscale
from TreeCredit import CreditCalculator


connection = connect_to_planetscale()
cursor = connection.cursor()

service = Service(executable_path="./bin/geckodriver")
driver = webdriver.Firefox(service=service)

# TABLE NAMEs
LIB_TABLE = 'DetectFile'
SEP_TREE_TABLE = 'SepPT_full'

MAX_DEPTH=100
MAX_NODE=10000

BLACK_LIST = []


def errMsg(msg):
    return f'\033[1;31mERROR: {msg}\033[0m'


def generatePT(file_index):
    driver.get(f"http://127.0.0.1:6543/test/{file_index}")

    error_div = driver.find_element(By.ID, 'js-errors')
    if error_div.text:
        # Failed to load the library
        print(f"    {errMsg(f'{file_index} >> {error_div.text}')}")
        return None, 0, 0, 0

    # 127.0.0.1:6543/test/tween.js@18.6.4@tween.umd.min.js
    driver.execute_script(f'createObjectTree({MAX_DEPTH}, {MAX_NODE}, false);')
    WebDriverWait(driver, timeout=10).until(text_to_be_present_in_element((By.ID, "obj-tree"), '{'))
    tree_json = driver.find_element(By.ID, 'obj-tree').text
    tree = json.loads(tree_json)
    circle_num = int(driver.find_element(By.ID, 'circle-num').text)

    # Remove Global Varabile in Blacklist
    del_index = []
    for i in range(len(tree['children'])):
        if tree['children'][i]['name'] in BLACK_LIST:
            del_index.append(i)
    offset = 0
    for index in del_index:
        del tree['children'][index - offset]
        offset += 1

    CC = CreditCalculator(max_depth=MAX_DEPTH)
    size, depth = CC.algorithm1(tree)
    CC.minifyTreeSpace(tree)

    return tree, size, depth, circle_num


def updateOne(file_index):
    pt, size, depth, circle_num = generatePT(file_index)

    if pt:
        # Add pt to SepTreeTABLE dataTABLE
        globalV = []
        for subtree in pt['c']:
            globalV.append(subtree['n'])

        # If entry already exists, delete first
        cursor.execute(f"SELECT size FROM {SEP_TREE_TABLE} WHERE file_id = '{file_index}';")
        res = cursor.fetchone()
        if res:  
            cursor.execute(f"DELETE FROM {SEP_TREE_TABLE} WHERE file_id = '{file_index}';")
            connection.commit()

        # Create new entry in SEP_TREE_TABLE
        sql = f'''INSERT INTO {SEP_TREE_TABLE} 
                (pTree, size, depth, globalV, globalV_num, circle_num, file_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s);'''
        val = (json.dumps(pt), size, depth, json.dumps(globalV), len(globalV), circle_num, int(file_index))
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
    updateAll(41)
    driver.close()
    connection.close()




