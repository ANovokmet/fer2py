# fer2py

Python wrapper (?) za Fer2 zasnovan na bibliotekama requests i BeautifulSoup4. Svodi se na parsiranje html-a.

## Korištenje

Kopiraj si kod ili .py datoteke.

## Primjeri

Ulogiravanje:
``` python
from fer2py import Fer2

forum = Fer2()
forum.logIn('1234','malipiso93')
# ažurira security token
forum.getSecurityToken() 
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
