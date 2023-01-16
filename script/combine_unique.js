const fs = require('fs');

data = JSON.parse(fs.readFileSync('../data/unique_v.json'));
new_data = {}
for (lib_info of data) {
    for (v of lib_info['global_v']) {
        new_data[v] = lib_info['name']
    }
}
fs.writeFileSync('../data/unique_v_dict.json',  JSON.stringify(new_data))