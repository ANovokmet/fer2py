__author__ = 'Ante'
from bs4 import BeautifulSoup
from hashlib import md5
import requests, re, datetime

baseurl = "http://www.fer2.net/"

class Fer2(object):


    def __init__(self):
        self._session = requests.session()
        self._security_token = ''
        self._allowed_actions = ['groan','lol','thanks']
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

    def getUsers(self, pp=100, page=1, sort='username', order='asc'):
        res = self._session.get(
            "http://www.fer2.net/memberlist.php?&pp={0}&order={1}&sort={2}&page={3}".format(pp, order, sort, page))

        soup = BeautifulSoup(res.text, 'html.parser')
        users = []

        for usertd in soup.find_all('td', {'class': "alt1Active"}):
            a = usertd.find('a')

            user = {
                'profile': a.get('href'),
                'userid': int(a.get('href').split("?u=")[1]),
                'username': a.text
            }

            users.append(user)

        return users

    def getUsers(self, username='', sort='', order='', pp=100, gender=0, year=0, name='', page=0):
        data = {
            's': '',
            'securitytoken': self._security_token,
            'do': 'getall',
            'ausername': username,
            'field22': name,
            'field17': year,  # godina 0-sve 1-PRVA 2-DRUGA 3-TREĆA 4-ČETVRTA 5-PETA 6-ALUMNI
            'field8': gender,  # spol: 0-oba, 1-ferovac, 2-ferovka
            'sort': sort,
            'order': order,
            'pp': pp,
            'page': page
            # nobody gonna use these
            # 'homepage':'stranica',
            # 'field2':'lokacija', #interesi
            # 'field3':'interesi', #lokacija
            # 'icq':'icq',
            # 'aim':'aim',
            # 'msn':'msn',
            # 'yahoo':'yahoo',
            # 'skype':'skype',
            # 'postslower':0,
            # 'postsupper':500,
            # 'joindateafter':'2015-12-01', #gggg-mm-dd ss:mm:ss
            # 'joindatebefore':'2016-12-01',
            # 'lastpostafter':'2015-12-01',
            # 'lastpostbefore':'2016-12-01',
        }

        res = self._session.post("http://www.fer2.net/memberlist.php?do=getall", data=data)

        soup = BeautifulSoup(res.text, 'html.parser')

        users = []

        for usertd in soup.find_all('td', {'class': "alt1Active"}):
            a = usertd.find('a')

            user = {
                'profile': a.get('href'),
                'userid': int(a.get('href').split("?u=")[1]),
                'username': a.text
            }

            users.append(user)

        return users

    def getUser(self, userid=None, profile=None):
        url = baseurl
        if profile is not None:
            url += profile
        elif userid is not None:
            url += "member.php?u=" + str(userid) + "&simple=1"
        else:
            raise Exception('no profile specified')

        res = self._session.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        userdata = {}
        dl = soup.find('dl', {'class': 'list_no_decoration profilefield_list'})
        for dt, dd in zip(dl.find_all('dt'), dl.find_all('dd')):
            userdata[dt.text] = dd.text

        return userdata

    def giveGift(self, recipientid, gift=238, public_message="", private=0, message=""):
        data = {
            'gift': gift,
            'public_message': public_message,
            'private': private,
            'message': message,
            'wysiwyg': 0,
            's': '',
            'recipientid': recipientid,
            # 'sbutton' : 'Po%9Aalji+poklon'
        }

        res = self._session.post("http://www.fer2.net/gifts.php?do=insert", data=data)

    def sendPrivateMessage(self, recipients, title, message="", ):
        data = {
            'recipients': '; '.join(recipients),
            'bccrecipients': '',
            'title': title,
            'message': message,
            'wysiwyg': 0,
            'iconid': '',  # 13,
            's': '',
            'securitytoken': self._security_token,
            'do': 'insertpm',
            'pmid': '',
            'forward': '',
            # 'sbutton' : 'Po%9Aalji+poruku'
            'savecopy': 1,
            'parseurl': 1
        }

        res = self._session.post("http://www.fer2.net/private.php?do=insertpm&pmid=", data=data)

    def sendProfileMessage(self, userid, message):

        data = {
            'ajax': 1,
            'wysiwyg': 0,
            'styleid': 0,
            'fromquickcomment': 1,
            's': '',
            'securitytoken': self._security_token,
            'do': 'message',
            'u': userid,
            'u2': '',
            #'loggedinuser': 9993,
            'parseurl': 1,
            # 'lastcomment':1474612848,
            'allow_ajax_qc': 1,
            'fromconverse': '',
            'message': message
        }

        res = self._session.post("http://www.fer2.net/visitormessage.php?do=message", data=data)

    def ajaxDoUserSearch(self, fragment):

        data = {
            'do': 'usersearch',
            'securitytoken': self._security_token,
            'fragment': fragment
        }

        res = self._session.post("http://www.fer2.net/ajax.php?do=usersearch", data=data)

        soup = BeautifulSoup(res.text, 'html.parser')

        users = []
        for user in soup.find_all('user'):
            userdata = {
                'userid': user.get('userid'),
                'username': user.text
            }
            users.append(userdata)
        return users

    def getBirthdayUsers(self):

        now = datetime.datetime.now()
        res = self._session.get("http://www.fer2.net/calendar.php?month={}&year={}".format(now.month,now.year))
        soup = BeautifulSoup(res.text, 'html.parser')

        users = []
        fragment = soup.find('td', { 'title' : 'Danas'})

        for userlink in fragment.find_all('a'):
            profile = userlink.get('href')
            user = {
                'userid' : profile.split("?u=")[1],
                'profile' : profile,
                'username' : userlink.text
            }
            users.append(user)
        return users



    def doActionThread(self, threadid, page, action, remove=False, ajaxpost=False):
        if action not in self._allowed_actions:
            raise Exception('action not allowed')

        html = self._session.get('http://www.fer2.net/showthread.php?t='+str(threadid)+'&page='+str(page))
        soup = BeautifulSoup(html.text, 'html.parser')

        #securitytoken = soup.find('input', {'name':'securitytoken'}).get('value')
        if not remove:
            do = "post_"+action+"_add"
        else:
            do = "post_"+action+"_remove_user"

        for link in soup.find_all('a'):
            link = str(link.get('href'))
            if(do in link):
                if not ajaxpost:
                    self._session.get(baseurl+link)
                else:
                    parts = link.split('?')
                    if not remove:
                        payload = getPayload(parts[1])
                    else:
                        payload = getPayload(parts[1], self._security_token)

                    self._session.post(baseurl+parts[0], data=payload)

    #groan lol thanks
    def doActionPost(self, postid, action, remove=False):
        if action not in self._allowed_actions:
            raise Exception('action not allowed')

        if not remove:
            do = "post_"+action+"_add"
        else:
            do = "post_"+action+"_remove_user"

        data = {
            'do': do,
            'using_ajax':'1',
            'p': str(postid),
            'securitytoken': self._security_token
        }

        res = self._session.post('http://www.fer2.net/post_'+action+'.php', data=data)

    def hitProfile(self, userid):
        res = self._session.head('http://www.fer2.net/member.php?u='+str(userid))

def getPayload(paramsString, security_token = None):

    parts1 = paramsString.split("&securitytoken=")
    parts2 = parts1[0].split("&p=")
    parts3 = parts2[0].split("do=")

    if(security_token==None):
        security_token = parts1[1]
    p = parts2[1]
    do = parts3[1]

    payload ={
        'do':do,
        'using_ajax':'1',
        'p':p,
        'securitytoken':security_token
    }
    return payload
