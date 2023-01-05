###  Detect global variables of libraries loaded from cdnjs.json.
###  Results are stored into a <lib_name, [v1, v2, ...]> pair dict.
###  Program will jump if the lib is already in the dict.


from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import json
import os


with open('data/origin.json', 'r') as openfile:
    origin_vlist = json.load(openfile)

with open('data/cdnjs.json', 'r') as openfile:
    lib_list = json.load(openfile)

save_path = "data/result_no_error.json"
_dict = {}
# Read from existing result file if exists
if os.path.exists(save_path):
    with open(save_path, "r") as openfile:
        _dict = json.load(openfile)


service = Service(executable_path="./bin/geckodriver")
driver = webdriver.Firefox(service=service)

error_cnt = 0
lib_num = len(lib_list['results'])
for i in range(0,lib_num):
    lib_name = lib_list['results'][i]['name']
    lib_path = lib_list['results'][i]['latest']
    if lib_name in _dict:
        continue
    if not lib_path or lib_path[-3:] != '.js':
        continue

    try:   
        driver.get(f"http://127.0.0.1:6543/test/{i}")
        vlist = driver.execute_script('return Object.keys(window);')
        error_div = driver.find_element(By.ID, 'js-errors')
        if error_div.text:
            print(f"X {i}: {error_div.text}")
        else:    
            _dict[lib_name] = [i for i in vlist if i not in origin_vlist]
            print(f"{i}: Library {lib_name} finishes testing.")

    except:
        error_cnt += 1
        print(f"X {i}: Library {lib_name} error meets.")

driver.close()

json_object = json.dumps(_dict, indent=4)
with open(save_path, "w") as outfile:
    outfile.write(json_object)

print(f'{error_cnt} errors occur in total.')
print(f'Results are saved to "{save_path}" file.')



