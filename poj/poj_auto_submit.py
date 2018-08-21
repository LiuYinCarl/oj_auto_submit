import requests
from lxml import etree
import base64

VALID_STATUS_CODES = [200, 302]

class POJ(object):
    def __init__(self):
        self.headers = {
            'Referer': 'http://poj.org/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Host': 'poj.org'
        }
        self.login_url = 'http://poj.org/login'
        self.submit_url = 'http://poj.org/submit'
        self.response_url = 'http://poj.org/status?user_id=bearcarl'
        self.session = requests.session()
        self.response = None

    def decode(self, code):
        byte_string = code.encode(encoding='utf-8')
        encode_str = base64.b64encode(byte_string)
        return encode_str

    def login(self):
        post_data = {
            'user_id1': 'bearcarl',
            'password1': 'a7873215321',
            'B1':'login',
            'url': '/problemlist'
        }
        try:
            response = self.session.post(self.login_url, data=post_data, headers=self.headers)
            if response.status_code in VALID_STATUS_CODES:
                print('login success')
        except Exception as e:
            print('login error: ', e.args)

    def submit_code(self):
        with open('E:/VSproject/TSOJ/TSOJ/TSOJ/code.cpp', 'r') as f:
            text = f.read()
            text = self.decode(text)
        data = {
            'problem_id': '1000',
            # 0 G++ 1 GCC 2 JAVA 3 PASCAL 4 C++ 5 C 6 FORTRAN
            'language': '2',
            'source': text,
            'submit': 'Submit',
            'encoded': '1'
        }
        try:
            response = self.session.post(self.submit_url, data=data,heasers=self.headers)
            if response.status_code in VALID_STATUS_CODES:
                print('submit success')
        except Exception as e:
            print('submit error: ', e.args)

    def get_result(self, text):
        html = etree.HTML(text)
        result =


    def get_response(self):
        try:
            response = self.session.get(self.response_url, headers=self.headers)
            if response.status_code in VALID_STATUS_CODES:
                print('get response success')
                self.get_result(response.text)
        except Exception as e:
            print('get response error: ', e.args)








if __name__ == '__main__':
    test = POJ()
    # test.login()
    test.submit_code()

