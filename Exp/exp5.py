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

def SameDict(d1, d2):
    for k, v in d1.items():
        if not k in d2:
            return False
        if d2[k] != v:
            return False
    return True


def combine (t, pt, lib_id, file_name):
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
        for d_item in node_pt['d']:
            if SameDict(d_item['d'], node_t['d']):
                # Type and Value equal
                find_d_item = True
                d_item['Ls'].append({'L': lib_id, 'F': file_name, 'x': node_t['x']})
                break                  
        
        if not find_d_item:
            node_pt['d'].append({'d': node_t['d'], 'Ls': [{'L': lib_id, 'F': file_name, 'x': node_t['x']}]})
        
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




MAX_DEPTH=5
MAX_NODE=500


service = Service(executable_path="./bin/geckodriver")
driver = webdriver.Firefox(service=service)


cursor.execute("SELECT name, latest_version, latest_version_files, id FROM AccuLibs2;")
res = cursor.fetchall()


lib_cnt = 0

for entry in res:
    lib_name = entry[0]
    version = entry[1]
    jsfiles = json.loads(entry[2])
    id = entry[3]
    lib_cnt += 1

    valid_files = []
    for jsfile in jsfiles:

        
        jsfile_tag = f'{lib_name}@{version}@{jsfile}'.replace('/','@')

        # if jsfile_tag == 'processing.js@1.6.6@processing.min.js':
        #     start = True
        # if not start:
        #     continue
        driver.get(f"http://127.0.0.1:6543/test/{jsfile_tag}")

        error_div = driver.find_element(By.ID, 'js-errors')
        if error_div.text:
            # Failed to load the library
            print(f"X {lib_cnt}: {jsfile_tag} >> {error_div.text}")
            continue

        # 127.0.0.1:6543/test/tween.js@18.6.4@tween.umd.min.js
        vlist = driver.execute_script(f'createObjectTree({MAX_DEPTH}, {MAX_NODE}, false);')
        #"//div[@id='obj-tree'][1]"
        WebDriverWait(driver, timeout=3).until(text_to_be_present_in_element((By.ID, "obj-tree"), '{'))
        tree_json = driver.find_element(By.ID, 'obj-tree').text
        tree = json.loads(tree_json)

        CC = CreditCalculator(max_depth=MAX_DEPTH)
        CC.algorithm1(tree)
        CC.minifyTreeSpace(tree)

        for subtree in tree['c']:
            subtree_name = subtree['n']
            cursor.execute(f"SELECT content FROM PTrees1 WHERE root_name = '{subtree_name}';")
            res = cursor.fetchone()
            
            if res:
                pt = json.loads(res[0])
                combine(subtree, pt, id, jsfile)
                sql = "UPDATE PTrees1 SET content = %s WHERE root_name = %s;"
                val = (json.dumps(pt), subtree_name)
                cursor.execute(sql, val)
                connection.commit()
            else:
                pt = {'n': subtree_name, 'd': [], 'c': []}
                combine(subtree, pt, id, jsfile)
                sql = "INSERT INTO PTrees1 (root_name, content) VALUES (%s, %s);"
                val = (subtree_name, json.dumps(pt))
                cursor.execute(sql, val)
                connection.commit()

        print(f"{lib_cnt}: {jsfile_tag} updated.")

        valid_files.append(jsfile)
    
    sql = "UPDATE AccuLibs2 SET valid_files = %s WHERE name = %s;"
    val = (json.dumps(valid_files), lib_name)
    cursor.execute(sql, val)
    connection.commit()

   


    # except:
    #    print(f"X {lib_cnt}: Library {lib['name']} error meets.")

    



driver.close()
connection.close()




