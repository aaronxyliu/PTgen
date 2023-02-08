### Generate credit object trees

from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import text_to_be_present_in_element
import json
from ete3 import Tree
from TreeCredit import CreditCalculator
from dotenv import load_dotenv
load_dotenv()
import MySQLdb
import json

# Connect to PlantScale Database
connection = MySQLdb.connect(
  host= 'us-east.connect.psdb.cloud',
  user='yain51suytl8vm1cm4b2',
  passwd= 'pscale_pw_pEiVDtydTJqIpuJ68NRKenF0ncp6jjYipJkfxFDIHDN',
  db= 'js-lib-detect-trees',
  ssl_mode = "VERIFY_IDENTITY",
  ssl      = {
    #"ca": "/etc/ssl/cert.pem"   # For Mac
    "ca": "/etc/ssl/certs/ca-certificates.crt"  # For Linux
  }
)
cursor = connection.cursor()

service = Service(executable_path="./bin/geckodriver")
driver = webdriver.Firefox(service=service)

# DATABASE NAMEs
LIB_BASE = 'AccuLibs2'
SEP_TREE_BASE = 'SepPT1'

MAX_DEPTH=5
MAX_NODE=500

BLACK_LIST = []


def errMsg(msg):
    return f'\033[1;31mERROR: {msg}\033[0m'


def generatePT(jsfile_tag):
    driver.get(f"http://127.0.0.1:6543/test/{jsfile_tag}")

    error_div = driver.find_element(By.ID, 'js-errors')
    if error_div.text:
        # Failed to load the library
        print(f"    {errMsg(f'{jsfile_tag} >> {error_div.text}')}")
        return None, 0, 0, 0

    # 127.0.0.1:6543/test/tween.js@18.6.4@tween.umd.min.js
    driver.execute_script(f'createObjectTree({MAX_DEPTH}, {MAX_NODE}, false);')
    WebDriverWait(driver, timeout=3).until(text_to_be_present_in_element((By.ID, "obj-tree"), '{'))
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


def updateOne(lib_name, filename):
    cursor.execute(f"SELECT latest_version, latest_version_files, id, valid_files FROM {LIB_BASE} WHERE name = '{lib_name}';")
    res = cursor.fetchone()
    if not res:
        print(f"{lib_name} doesn't not exist in {LIB_BASE} database.")
        return
    version = res[0]
    jsfiles = json.loads(res[1])
    # id = res[2]
    valid_files = []
    if res[3]:
        valid_files = json.loads(res[3])

    if filename not in jsfiles:
        print(f"    {filename} doesn't exist.")
        return
    
    if valid_files and filename in valid_files:
        print(f'    {filename} already in valid_files.')
        return
    
    jsfile_tag = f'{lib_name}@{version}@{filename}'.replace('/','@')
    pt, size, depth, circle_num = generatePT(jsfile_tag)

    if pt:
        # Add pt to SepTreeBase database
        globalV = []
        for subtree in pt['c']:
            globalV.append(subtree['n'])

        # If entry already exists, delete first
        cursor.execute(f"SELECT size FROM {SEP_TREE_BASE} WHERE jsfile = '{jsfile_tag}';")
        res = cursor.fetchone()
        if res:  
            cursor.execute(f"DELETE FROM {SEP_TREE_BASE} WHERE jsfile = '{jsfile_tag}';")
            connection.commit()

        # Create new entry in SEP_TREE_BASE
        sql = f"INSERT INTO {SEP_TREE_BASE} (jsfile, pTree, size, depth, globalV, globalV_num, circle_num) VALUES (%s, %s, %s, %s, %s, %s, %s);"
        val = (jsfile_tag, json.dumps(pt), size, depth, json.dumps(globalV), len(globalV), circle_num)
        cursor.execute(sql, val)
        connection.commit()
        print(f'    {jsfile_tag} entry added to {SEP_TREE_BASE}.')

        # Update valid_file field in LIB_BASE
        valid_files.append(filename)
        sql = f"UPDATE {LIB_BASE} SET valid_files = %s WHERE name = %s;"
        val = (json.dumps(valid_files), lib_name)
        cursor.execute(sql, val)
        connection.commit()
    


def updateAll():

    cursor.execute(f"SELECT name, latest_version_files FROM {LIB_BASE};")
    res = cursor.fetchall()

    cnt = 0

    for entry in res:
        lib_name = entry[0]
        jsfiles = json.loads(entry[1])
        cnt += 1
        print(f"\033[1;35m============ {cnt}: {lib_name} ============\033[0m")

        for jsfile in jsfiles:
            print(f'  \033[1;32m{jsfile}:\033[0m')
            updateOne(lib_name, jsfile)


def resetValidFiles():
    cursor.execute(f"UPDATE {LIB_BASE} SET valid_files = '[]'")
    connection.commit()
        

            

            

if __name__ == '__main__':
    resetValidFiles()
    updateAll()
    driver.close()
    connection.close()




