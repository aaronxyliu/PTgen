### Generate credit object trees

from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.expected_conditions import text_to_be_present_in_element
import json
from ete3 import Tree
from TreeCredit import CreditCalculator


with open('data/result_no_error__.json', 'r') as openfile:
    lib_list = json.load(openfile)


MAX_DEPTH=5


service = Service(executable_path="./bin/geckodriver")
driver = webdriver.Firefox(service=service)

subtrees_index = {}
subtrees = []

lib_cnt = 0
subtree_cnt = 0

for lib in lib_list:

    try:
        driver.get(f"http://127.0.0.1:6543/test/{lib['index']}")
        vlist = driver.execute_script(f'createObjectTree(depth_limit={MAX_DEPTH});')
        #"//div[@id='obj-tree'][1]"
        WebDriverWait(driver, timeout=3).until(text_to_be_present_in_element((By.ID, "obj-tree"), '{'))
        tree_json = driver.find_element(By.ID, 'obj-tree').text
        tree = json.loads(tree_json)

        CC = CreditCalculator(max_depth=MAX_DEPTH)
        CC.algorithm1(tree)
        CC.minifyTreeSpace(tree)

        for child in tree['c']:
            subtree_name = child['n']
            if subtree_name not in subtrees_index:
                subtrees_index[subtree_name] = []
            subtrees_index[subtree_name].append({'lib': lib['name'], 'lib_index': lib['index'], 'tree_index': subtree_cnt})
            subtrees.append(child)
            subtree_cnt += 1

    except:
       print(f"X {lib_cnt}: Library {lib['name']} error meets.")

    lib_cnt += 1



driver.close()

json_object = json.dumps(subtrees_index, indent=4)
with open('data/subtrees_index.json', "w") as outfile:
    outfile.write(json_object)


# Store subtrees in seperating lines
with open('data/subtrees.json', "w") as outfile:
    outfile.write('[')
    for subtree in subtrees[:-1]:
        outfile.write(json.dumps(subtree) + ',\n')
    outfile.write(json.dumps(subtrees[-1]) + ']')




