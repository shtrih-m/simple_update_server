# python-requests.org
import requests
import json


def check_answer_code(code):
    if code != 200:
        raise Exception('\n'.join(['Error ' + str(code), r.text]))


def print_dict(dict):
    for i in dict.keys():
        print(str(i) + ":", dict[i])


def print_answer(answer):
    print('Status code:', answer.status_code)
    print('Encoding:', answer.encoding)
    print('Headers:')
    print_dict(r.headers)
    print('Body:')
    print(r.text)
    js = r.json()
    print('json:')
    print_dict(js)


print("=========== GET test ===========")
r = requests.get('http://127.0.0.1:8888/version')
check_answer_code(r.status_code)
print_answer(r)

print("=========== POST test ===========")
payload = {"build_date": "19.12.2017"}
headers = {'content-type': 'application/json'}
r = requests.post('http://127.0.0.1:8888/check_firmware', json=payload, headers=headers)
check_answer_code(r.status_code)
print_answer(r)