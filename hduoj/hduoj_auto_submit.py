import time
import json
import requests
import os
from lxml import etree
from prettytable import PrettyTable

VALID_STATUS_CODES = [200, 302]


class HDUOJ(object):
    def __init__(self):
        with open('hduoj_conf.json', 'r') as f:
            self.conf = json.load(f)

        self.headers = {
            'Referer': 'http://acm.hdu.edu.cn/login/error.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Host': 'acm.hdu.edu.cn'
        }
        self.login_url = self.conf['login_url']
        self.submit_url = self.conf['submit_url']
        self.response_url = self.conf['response_url'] + 'user=%s&pid=' % self.conf['login_data']['username']
        self.table = PrettyTable(self.conf['table'])
        self.session = requests.session()

    def login(self):
        login_data = self.conf['login_data']
        try:
            response = self.session.post(self.login_url, data=login_data, headers=self.headers)
            if response.status_code in VALID_STATUS_CODES:
                print('login success')
        except Exception as e:
            print('login error: ', e.args)

    def submit_code(self, pid):
        with open(self.conf['file_name'], 'r') as f:
            text = f.read()
        data = self.conf['submit_data']
        data['usercode'] = text
        data['problemid'] = pid
        try:
            response = self.session.post(self.submit_url, data=data, headers=self.headers)
            if response.status_code in VALID_STATUS_CODES:
                print('submit success')
        except Exception as e:
            print('submit error: ', e.args)

    def get_response(self, pid):
        try:
            res_url = self.response_url + str(pid)
            response = self.session.get(res_url, headers=self.headers)
            if response.status_code in VALID_STATUS_CODES:
                self.get_result(response.text)
                print('get response success')
        except Exception as e:
            print('get response error: ', e.args)

    def get_result(self, text):
        try:
            html = etree.HTML(text)
            result = html.xpath('//*[@id="fixed_table"]/table//tr')
            for item in result[1:]:
                pre_string = etree.tostring(item)
                pre_problem = etree.HTML(pre_string)
                valid_result = pre_problem.xpath('//text()')
                self.table.add_row(valid_result)
        except Exception as e:
            print('get result error: ', e.args)

    def table_set(self):
        column = self.conf['table']
        for i in column:
            self.table.align[i] = 'l'  # is L not number 1
        self.table.padding_width = 1

    def scheduling(self, pid):
        self.login()
        self.submit_code(pid)
        self.get_response(pid)
        while True:
            self.table = PrettyTable(self.conf['table'])
            self.table_set()
            time.sleep(self.conf['interval_time'])
            self.get_response(pid)
            os.system('cls')
            print(self.table)


if __name__ == '__main__':
    auto_submit = HDUOJ()
    problem_id = input('enter you problem ID(such as 1002): ')
    auto_submit.scheduling(int(problem_id))




