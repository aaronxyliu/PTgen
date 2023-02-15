file_tag = 'safda@1.22.78@fd.json'

lib_name = file_tag.slice(0, file_tag.indexOf('@'))
file_name = file_tag.slice(file_tag.indexOf('@'), file_tag.length)

console.log(lib_name)
console.log(file_name)