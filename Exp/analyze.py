### Analyze the global variable number distribution,
### and divide into different files.



import json


zero_set = set()

distribution = [0] * 10
with open('data/result_no_error.json', 'r') as openfile:
    _dict = json.load(openfile)

v_dict =  {}
total_num = 0
for lib in _dict:
    total_num += 1
    v_num = len(_dict[lib])
    if v_num >= 10:
        distribution[9] += 1
    else:
        distribution[v_num] += 1
    if v_num == 0:
        zero_set.add(lib)
    for v in _dict[lib]:
        if v in v_dict:
            v_dict[v] += 1
        else:
            v_dict[v] = 1

print(f'Total: {total_num}')
print(distribution)

with open('data/cdnjs.json', 'r') as openfile:
    lib_list = json.load(openfile)

new_dict = []
new_dict2 = []
new_dict3 = []
new_dict4 = []
index = 0
unique_num = 0
non_unique_num = 0

for lib_info in lib_list['results']:
    lib_info['index'] = index
    if lib_info['name'] in zero_set:
        new_dict.append(lib_info)

    # Check unique variable
    lib_info['unique_v'] = []  
    if lib_info['name'] in _dict:
        lib_info['global_v'] = _dict[lib_info['name']]
        for v in _dict[lib_info['name']]:
            if v_dict[v] == 1:
                lib_info['unique_v'].append(v)
        if len(lib_info['unique_v']) > 0:
            unique_num += 1
            new_dict2.append(lib_info)
        else:
            non_unique_num += 1
            new_dict3.append(lib_info)
        new_dict4.append(lib_info)
    index += 1

print(f"Unique number: {unique_num}")
print(f"Non-unique number: {non_unique_num}")

json_object = json.dumps(new_dict, indent=4)
with open('data/zero_v.json', "w") as outfile:
    outfile.write(json_object)

json_object2 = json.dumps(new_dict2, indent=4)
with open('data/unique_v.json', "w") as outfile:
    outfile.write(json_object2)

json_object3 = json.dumps(new_dict3, indent=4)
with open('data/non_unique_v.json', "w") as outfile:
    outfile.write(json_object3)

json_object4 = json.dumps(new_dict4, indent=4)
with open('data/result_no_error__.json', "w") as outfile:
    outfile.write(json_object4)

## RESULT:
##   Total: 4346
##   [2057, 1623, 266, 131, 51, 31, 29, 21, 14, 123] 
