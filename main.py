import requests
from bs4 import BeautifulSoup
from hashlib import md5

m = md5()
m.update("".encode("utf-8"))
md5password = m.hexdigest()


baseurl = "http://www.fer2.net/"

session = requests.session();

def getUsers(pp=100,page=1,sort='username',order='asc'):
    res = session.get("http://www.fer2.net/memberlist.php?&pp={0}&order={1}&sort={2}&page={3}".format(pp,order,sort,page))

    soup = BeautifulSoup(res.text, 'html.parser')
    print(soup.get_text())

    users = []

    for usertd in soup.find_all('td', {'class' : "alt1Active"}):
        a = usertd.find('a')

        user = {
            'profile' : a.get('href'),
            'userid' : int(a.get('href').split("?u=")[1]),
            'username' : a.text
        }

        users.append(user)

    return users

def getUsers(username='',sort='',order='',pp=100,gender=0,year=0, name='', page=0):
    data = {
        's':'',
        'securitytoken':'1475588278-31fa3803968b304823625e1ee647aeacd210adef',
        'do':'getall',
        'ausername':username,
        #'homepage':'stranica',
        'field22':name,
        'field17':year, #godina 0-sve 1-PRVA 2-DRUGA 3-TREĆA 4-ČETVRTA 5-PETA 6-ALUMNI
        'field8': gender, #spol: 0-oba, 1-ferovac, 2-ferovka
        # nobody gonna use this
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
        'sort':sort,
        'order':order,
        'pp':pp,
        'page':page
    }

    res = session.post("http://www.fer2.net/memberlist.php?do=getall", data=data)

    soup = BeautifulSoup(res.text, 'html.parser')
    users = []

    for usertd in soup.find_all('td', {'class' : "alt1Active"}):
        a = usertd.find('a')

        user = {
            'profile' : a.get('href'),
            'userid' : int(a.get('href').split("?u=")[1]),
            'username' : a.text
        }

        users.append(user)

    return users

def getUser(userid=None,profile=None):
    url = baseurl
    if profile is not None:
        url += profile
    elif userid is not None:
        url += "member.php?u="+ str(userid)+"&simple=1"
    else:
        raise Exception('no profile specified')

    res = session.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    print(soup.get_text())
    userdata = {}
    dl = soup.find('dl', { 'class' : 'list_no_decoration profilefield_list'})
    for dt, dd in zip(dl.find_all('dt'), dl.find_all('dd')):
        userdata[dt.text] = dd.text

    return userdata

def giveGift(recipientid,gift=238,public_message="",private=0,message=""):
    data={
        'gift' : gift,
        'public_message' : public_message,
        'private' : private,
        'message' : message,
        'wysiwyg' : 0,
        's' : '',
        'recipientid' : recipientid,
        #'sbutton' : 'Po%9Aalji+poklon'
    }

    res = session.post("http://www.fer2.net/gifts.php?do=insert", data=data)

    soup = BeautifulSoup(res.text, 'html.parser')
    print(soup.get_text())

def sendPrivateMessage(recipients, title, message="",):
    data={
        'recipients' : '; '.join(recipients),
        'bccrecipients' : '',
        'title' : title,
        'message' : message,
        'wysiwyg' : 0,
        'iconid' : '',#13,
        's' : '',
        'securitytoken' : '1475584984-e3b1df675e0acdf4989d4a98071ee78139672a1f',
        'do' : 'insertpm',
        'pmid' : '',
        'forward' : '',
        #'sbutton' : 'Po%9Aalji+poruku'
        'savecopy' : 1,
        'parseurl' : 1
    }

    res = session.post("http://www.fer2.net/private.php?do=insertpm&pmid=", data=data)

    soup = BeautifulSoup(res.text, 'html.parser')
    print(soup.get_text())

def sendProfileMessage(userid, message):

    data = {
        'ajax': 1,
        'wysiwyg': 0,
        'styleid': 0,
        'fromquickcomment': 1,
        's':'',
        'securitytoken':'1475587251-a27931af98d60a92ca754131b91c347332ec4c02',
        'do':'message',
        'u':userid,
        'u2':'',
        'loggedinuser':9993,
        'parseurl':1,
        #'lastcomment':1474612848,
        'allow_ajax_qc':1,
        'fromconverse':'',
        'message': message
    }

    res = session.post("http://www.fer2.net/visitormessage.php?do=message", data=data)
    print(res.text)

def ajaxDoUserSearch(fragment):

    data = {
        'do' : 'usersearch',
        'securitytoken': '1475584984-e3b1df675e0acdf4989d4a98071ee78139672a1f',
        'fragment' : fragment
    }

    res = session.post("http://www.fer2.net/ajax.php?do=usersearch", data=data)

    soup = BeautifulSoup(res.text, 'html.parser')

    users = []
    for user in soup.find_all('user'):
        userdata = {
            'userid' : user.get('userid'),
            'username' : user.text
        }
        users.append(userdata)
    return users

data = {
    'vb_login_username' : '1234',
    'vb_login_password' : '',
    's' : '',
    'do' : 'login',
    'vb_login_md5password' : md5password,
    'vb_login_md5password_utf' : md5password
}

res = session.post("http://www.fer2.net/login.php?do=login", data=data)

soup = BeautifulSoup(res.text, 'html.parser')
#print(soup.get_text())
#print(getUsers())
#print(getUser(userid=9920))
#giveGift(9993, public_message="radi liovo")
#sendPrivateMessage(["1234"],"test",message="test")
#print(ajaxDoUserSearch("###"))

#sendProfileMessage(9920, 'ttest')

print(getUsers(username='a',page=0))