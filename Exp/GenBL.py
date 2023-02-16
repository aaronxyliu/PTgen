###  Generate Blacklist Global Variables
### Make sure no library is loaded.


from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver
import json
import os


save_path = "data/blacklist.json"


service = Service(executable_path="./bin/geckodriver")
driver = webdriver.Firefox(service=service)

driver.get(f"http://127.0.0.1:6543/test/1")
vlist = driver.execute_script('return Object.getOwnPropertyNames(window);')
print(f'{len(vlist)} global variable collected.')

driver.close()

json_object = json.dumps(vlist)
with open(save_path, "w") as outfile:
    outfile.write(json_object)

print(f'Results are saved to "{save_path}" file.')



