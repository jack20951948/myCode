import requests
import webbrowser
param = {"wd": "莫烦Python"}
r = requests.get('http://www.baidu.com/s', params=param)
print(r.url)
# webbrowser.open(r.url)

data = {"firstname": "Che-Chia", "lastname": "Chang"}
Header = {
'Host': 'pythonscraping.com',
'Content-Type': 'application/x-www-form-urlencoded',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
}
r = requests.post('https://pythonscraping.com/files/processing.php', data=data ,headers=Header)
print(r.text)
# webbrowser.open(r.url)

# file = {'uploadFile': open('./image.png', 'rb')}
# r = requests.post('http://pythonscraping.com/files/processing2.php', files=file)
# print(r.text)

payload = {'username': 'Morvan', 'password': 'password'}
r = requests.post('http://pythonscraping.com/pages/cookies/welcome.php', data=payload)
print(r.cookies.get_dict())
r = requests.get('http://pythonscraping.com/pages/cookies/profile.php', cookies=r.cookies)
print(r.text)

# session = requests.Session()
# payload = {'username': 'Morvan', 'password': 'password'}
# r = session.post('http://pythonscraping.com/pages/cookies/welcome.php', data=payload)
# print(r.cookies.get_dict())
# r = session.get("http://pythonscraping.com/pages/cookies/profile.php")
# print(r.text)