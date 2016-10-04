__author__ = 'Ante'
import requests
from hashlib import md5

from fer2py import Fer2

base_url = 'http://www.fer2.net/'

headers ={
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, sdch',
'Accept-Language':'hr-HR,hr;q=0.8,en-US;q=0.6,en;q=0.4',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'bblastvisit=1452218549; bblastactivity=0; bbuserid=9920; bbpassword=c14c46ffd3652d0dcabd066a8418817f; bbexttMbqMinisiteRedirectFlag=2; vbulletin_userlist_hide_avatars_buddylist=0; bborderhash=1709f48ee79b989f5afc1b59a579adb0; bbsessionhash=958d6a2db55b71de6f114fb2731a55df; __utmt=1; bbthread_lastview=18363b4e9cab74491d4f0d2b81cf61a3d64272a8a-4-%7Bi-67196_i-1464338343_i-56230_i-1464336572_i-65910_i-1464342244_i-67821_i-1464342342_%7D; __utma=121151519.615703757.1452218550.1464295293.1464342243.1166; __utmb=121151519.8.10.1464342243; __utmc=121151519; __utmz=121151519.1463334586.1067.5.utmcsr=facebook.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
'Host':'www.fer2.net',
'Referer':'http://www.fer2.net/member.php?u=9920',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
}

forum = Fer2()
forum.logIn('1234',                                                                              '')
print(forum.getSecurityToken())
exit(0)
