### Generate object tree



from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import json
from ete3 import Tree
import os


def generateTree(driver, node, variable, depth=0):
    if depth >= 5:
        return
    v_info = driver.execute_script(f'return analyzeVariable({variable});')
    if 'value' in v_info:
        node.add_feature('value', v_info['value'])
    node.add_feature('type', v_info['type'])
    for v in v_info['children']:
        child_node = node.add_child(name=v)
        generateTree(driver, child_node, f'{variable}["{v}"]', depth+1)


with open('data/origin.json', 'r') as openfile:
    origin_vlist = json.load(openfile)

with open('data/result_no_error__.json', 'r') as openfile:
    lib_list = json.load(openfile)





service = Service(executable_path="./bin/geckodriver")
driver = webdriver.Firefox(service=service)

cnt = 0

for lib in lib_list: 
    if cnt >= 20:
        break
    driver.get(f"http://127.0.0.1:6543/test/{lib['index']}")
    vlist = driver.execute_script('return Object.keys(window);')
    unique_global = [i for i in vlist if i not in origin_vlist]

    t = Tree() # Creates an empty tree
    for v in unique_global:   
        child_node = t.add_child(name=v)
        generateTree(driver, child_node, f'window["{v}"]')

    # except:
    #     print(f"X {cnt}: Library {lib['name']} error meets.")

    cnt += 1

    print(t.get_ascii(show_internal=True))



driver.close()

# json_object = json.dumps(lib_list, indent=4)
# with open(save_path, "w") as outfile:
#     outfile.write(json_object)


# save_path = "data/result_tree.log"
# t_str = t.write(features=["type", "value"],format=1)
# with open(save_path, "w") as outfile:
#      outfile.write(t_str)

# print(len(t_str))
# print(f'Results are saved to "{save_path}" file.')



