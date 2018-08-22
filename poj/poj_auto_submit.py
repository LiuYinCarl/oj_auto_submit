import requests
import json
import time
import os
from lxml import etree
import base64
from prettytable import PrettyTable

VALID_STATUS_CODES = [200, 302]


class POJ(object):
    def __init__(self):
        with open('poj_conf.json', 'r') as f:
            self.conf = json.load(f)

        self.headers = {
            'Referer': 'http://poj.org/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Host': 'poj.org'
        }
        self.login_url = self.conf['login_url']
        self.submit_url = self.conf['submit_url']
        self.response_url = self.conf['response_url'] + self.conf['post_data']['user_id1']
        self.session = requests.session()
        self.table = PrettyTable(self.conf['table'])

    def decode(self, code):
        byte_string = code.encode(encoding='utf-8')
        encode_str = base64.b64encode(byte_string)
        return encode_str

    def login(self):
        post_data = self.conf['post_data']
        try:
            response = self.session.post(self.login_url, data=post_data, headers=self.headers)
            if response.status_code in VALID_STATUS_CODES:
                print('login success')
        except Exception as e:
            print('login error: ', e.args)

    def submit_code(self, pid):
        with open(self.conf['file_name'], 'r') as f:
            text = f.read()
            text = self.decode(text)
        data = self.conf['submit_data']
        data['source'] = text
        data['problem_id'] = pid
        try:
            response = self.session.post(self.submit_url, data=data, headers=self.headers)
            if response.status_code in VALID_STATUS_CODES:
                print('submit success')
        except Exception as e:
            print('submit error: ', e.args)

    def table_set(self):
        column = self.conf['table']
        for i in column:
            self.table.align[i] = 'l'  # is L not number 1
        self.table.padding_width = 1

    def check_result(self, data):
        try:
            if len(data) != 9:
                data.insert(4, 'No Data')
                data.insert(5, 'No Data')
            self.table.add_row(data)
        except Exception as e:
            print('check result error: ', e.args)

    def get_result(self, text, pid):
        try:
            html = etree.HTML(text)
            result = html.xpath('//tr[@align = "center"]/td[3]/a[text() = %d]/../..' % pid)
            for item in result:
                pre_string = etree.tostring(item)
                pre_problem = etree.HTML(pre_string)
                valid_result = pre_problem.xpath('//text()')[:-1]
                self.check_result(valid_result)
        except Exception as e:
            print('get result error: ', e.args)

    def get_response(self, pid):
        try:
            response = self.session.get(self.response_url, headers=self.headers)
            if response.status_code in VALID_STATUS_CODES:
                self.get_result(response.text, pid)
                print('get response success')
        except Exception as e:
            print('get response error: ', e.args)

    def scheduling(self, pid):
        self.login()
        self.submit_code(pid)
        while True:
            self.table = PrettyTable(self.conf['table'])
            self.table_set()
            time.sleep(self.conf['interval_time'])
            self.get_response(pid)
            os.system('cls')
            print(self.table)


if __name__ == '__main__':
    auto_submit = POJ()
    problem_id = input('enter you problem ID(such as 1002): ')
    auto_submit.scheduling(int(problem_id))
