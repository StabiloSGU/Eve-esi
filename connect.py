import webbrowser
import socket
import requests
#auth

auth_link = 'https://login.eveonline.com/oauth/authorize?response_type=code&redirect_uri=%CALLBACK LINK%&client_id=%CLIENT ID%&scope=esi-characters.read_standings.v1'

webbrowser.open_new(auth_link)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((%CALLBACK ADDRESS%, %CALLBACK PORT%)) #if local app
s.listen(1)

conn, addr = s.accept()
print("connected to ",str(addr))
data = conn.recv(1024)
print("recieved code!")
code = str(data)[21:86]
conn.send(bytes('HTTP/1.0 200 OK\n', 'utf-8'))
conn.send(bytes('Content-Type: text/html\n', 'utf-8'))
conn.send(bytes('\n', 'utf-8'))
conn.send(bytes("""\
        <html>
        <body>
        <h1>Connected</h1>
        You can close this tab
        </body>
        </html>
        """, 'utf-8'))
conn.close()

#access token

headers = {
    "Content-Type" : "application/x-www-form-urlencoded",
    "Authorization" : "Basic %YOUR CODE HERE%"
    }

data = {
    "grant_type":"authorization_code",
    "code": code
    }

r = requests.post("https://login.eveonline.com/oauth/token", headers = headers, data=data)
token = r.json()

if r.status_code != 200:
    print("oh frak")
else:
    print("token recieved")

#get info
headers = {
    "Authorization" : "Bearer "+token['access_token']
    }
r = requests.get("https://esi.tech.ccp.is/verify/", headers = headers)
if r.status_code != 200:
    print("oh frak")
else:
    print("data recieved")
result = r.json()
