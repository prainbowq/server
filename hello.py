import requests
import base64
import json

bytes_list = []
with open('imgs.txt') as file:
    print('get: ')
    i = 1
    for line in file.readlines():
        url = f'https://worldskills.org{line[:-1]}'
        response = requests.get(url)
        bytes_list.append(response.content)
        print(i)
        i += 1
base64_list = []
print('b64encode: ')
i = 1
for bytes in bytes_list:
    base64_list.append(base64.b64encode(bytes).decode())
    print(i)
    i += 1

date_list = []
with open('dates.txt') as file:
    for line in file.readlines():
        date_list.append(line[:-1])

title_list = []
with open('titles.txt') as file:
    for line in file.readlines():
        title_list.append(line[:-1])

desc_list = []
with open('des.txt') as file:
    for line in file.readlines():
        desc_list.append(line[:-1])

dict_list = []
for i in range(len(bytes_list)):
    dict_list.append({})
    dict_list[i]['date'] = date_list[i]
    dict_list[i]['title'] = title_list[i]
    dict_list[i]['content'] = desc_list[i]
    dict_list[i]['image'] = base64_list[i]
with open('result.json', 'w') as file:
    json.dump(dict_list, file, indent=4)
