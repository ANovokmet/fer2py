# fer2py

Python wrapper (?) za Fer2 zasnovan na bibliotekama requests i BeautifulSoup4. Svodi se na parsiranje html-a. Dost je šturo, radim na tome.

## Korištenje

Kopiraj si kod ili .py datoteke. Prije tog si nabavi requests i BeautifulSoup4.

## Primjeri

Ulogiravanje:
``` python
from fer2py import Fer2

forum = Fer2()
forum.logIn('1234','malipiso93')
# ažurira security token
forum.getSecurityToken() 
```

Uporaba:
``` python
for thread in forum.getThreads(predmetnidio=True, includeinfo=False):
  print(thread['title'])
```

Tipična uporaba:
``` python
# 1:ferovac, 2:ferovka
for user in forum.getUsers(gender=2, page=1): 
  forum.giveGift(user["userid"], public_message="bi li htjela imati ružnog dečka", gift=238)
```

Drugi primjer:
``` python
for user in forum.getBirthdayUsers():
  info = forum.getUser(user["userid"])
  if info["Spol"] == 'ferovka':
    forum.sendPrivateMessage([user["username"]], "Hej", message="za tvoj rođendan te vodim na kavu")
```

Šta je ovo:
``` python
# neko random ime
users = forum.ajaxDoUserSearch("iva")
# uzrokuje povećanje jednog broja za 1000
for i in range(0, 1000):
  forum.hitProfile(users[0]["userid"])
  
forum.sendProfileMessage(self, users[0]["userid"], "primjeti me")
```

Burza hvalaova:
``` python
for post in forum.getPostsByUser(9323):
  #hvala=thanks, grr=groan, lol=lol
  forum.doActionPost(post['postid'], 'thanks')
  
for post in forum.getThreadPosts(17653, page=2902):
  forum.doActionPost(post['postid'], 'thanks', remove=True)
```


