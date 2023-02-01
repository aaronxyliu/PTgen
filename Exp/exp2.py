### Check whether JavaScript error exists when loading the library.


from selenium.webdriver.firefox.service import Service
from selenium import webdriver
import json
import os

with open('data/origin.json', 'r') as openfile:
    origin_vlist = json.load(openfile)

with open('data/zero_v.json', 'r') as openfile:
    lib_list = json.load(openfile)

save_path = "data/result_.json"
_dict = {}


service = Service(executable_path="./bin/geckodriver")
driver = webdriver.Firefox(service=service)

error_cnt = 0
for lib_info in lib_list:
    lib_name = lib_info['name']
    try:
        driver.get(f"http://127.0.0.1:6543/test/{i}")
        vlist = driver.execute_script('return Object.keys(window);')
        # driver.close()

        
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



