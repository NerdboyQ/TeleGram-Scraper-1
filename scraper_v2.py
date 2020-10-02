from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os, sys, pandas
import configparser
import csv
import time

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"

headers = ["username","id","first_name","last_name","phone","contact", "group"]
def banner():
    print(f"""
{re}╔╦╗{cy}┌─┐┬  ┌─┐{re}╔═╗  ╔═╗{cy}┌─┐┬─┐┌─┐┌─┐┌─┐┬─┐
{re} ║ {cy}├┤ │  ├┤ {re}║ ╦  ╚═╗{cy}│  ├┬┘├─┤├─┘├┤ ├┬┘
{re} ╩ {cy}└─┘┴─┘└─┘{re}╚═╝  ╚═╝{cy}└─┘┴└─┴ ┴┴  └─┘┴└─

            version : 1.0
        youtube.com/theunknon
        """)

cpass = configparser.RawConfigParser()
cpass.read('config.data')

try:
    api_id = cpass['cred']['id']
    api_hash = cpass['cred']['hash']
    phone = cpass['cred']['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    os.system('clear')
    banner()
    print(re+"[!] run python3 setup.py first !!\n")
    sys.exit(1)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    os.system('clear')
    banner()
    client.sign_in(phone, input(gr+'[+] Enter the code: '+re))
 
os.system('clear')
banner()
chats = []
last_date = None
chunk_size = 200
groups=[]
 
result = client(GetDialogsRequest(
             offset_date=last_date,
             offset_id=0,
             offset_peer=InputPeerEmpty(),
             limit=chunk_size,
             hash = 0
         ))
chats.extend(result.chats)
 
for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue
 
print(gr+'[+] Choose a group to scrape members :'+re)
df = pandas.DataFrame()
i=0
#participants = client.get_participants(groups[0],aggressive=True)
#col_headers = list(participants[0].to_dict().keys())
#print(col_headers)
#df = df.assign(**dict.fromkeys(headers,0))
for g in groups:
    print(gr+'['+cy+str(i)+']' + ' - ' + g.title)
    target_group=groups[i]
    print(gr+'[+] Fetching Members...')
    #print(f"t_group: {target_group}")
    time.sleep(1)
    all_participants = []
    all_participants = client.get_participants(target_group,aggressive=True)
    temp_dict = {}
    for user in all_participants:
        temp_dict["group"] = target_group.title.encode
        for h in headers:
            if h != "group":
                temp_dict[h] = user.to_dict()[h]
        #print(temp_dict)
        df = df.append(temp_dict, ignore_index=True)

    i+=1
print(df)
df.to_csv("group_export.csv",index=False)
     
print('')
