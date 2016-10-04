__author__ = 'Ante'
from bs4 import BeautifulSoup
from hashlib import md5
import requests, re

class Fer2(object):
    def __init__(self):
        self._session = requests.session()
        self._security_token = ''
        print('initiated')

    def logIn(self, username, password):

        m = md5()
        m.update(password.encode('utf-8'))
        md5password = m.hexdigest()

        data = {
            'vb_login_username' : username,
            'vb_login_password' : '',
            's' : '',
            'securitytoken' : 'guest',
            'do' : 'login',
            'vb_login_md5password' : md5password,
            'vb_login_md5password_utf' : md5password
        }

        res = self._session.post('http://www.fer2.net/login.php?do=login', data=data)
        if res.status_code == 200:
            print(res.text)
            print(res.headers['content-type'])
            print('logged in')
        else:
            print('error '+str(res.status_code))

    def getSecurityToken(self):
        if self._security_token == '':
            res = self._session.get('http://www.fer2.net')

            m = re.findall("var SECURITYTOKEN = \"([0-9a-f]*-[0-9a-f]*)\"", res.text)
            if(m is not None):
                self._security_token = m[0]

        return self._security_token