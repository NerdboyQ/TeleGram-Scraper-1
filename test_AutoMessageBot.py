from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os, sys, pandas, openpyxl, telebot, telegram
import configparser
import csv
import time
import datetime as dt

def getTimeStamp():
    d_date = str(dt.datetime.now().date())
    d_time = dt.datetime.now().time()
    d_date += ("_" +str(d_time.hour) +"_" +str(d_time.minute) +"_" +str(d_time.second))
    return d_date

re="\033[1;31m"
gr="\033[1;32m"
cy="\033[1;36m"

headers = ["username","id","access_hash","first_name","last_name","phone", "group"]
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

for g in groups:
    #member_count = client.get_participants(groups[i],aggressive=True)
    print(gr+'['+cy+str(i)+']' + ' - ' + g.title+f"\t({groups[i].to_dict()['participants_count']} member(s))")
    i+=1

g_index = input(gr+"[+] Enter a Number : "+re)
print(gr+f"\nSelected group: {groups[int(g_index)].title}, id: {groups[int(g_index)].id}\n")
token = "1187789063:AAHguQcLblGeuBmp3n0WSVoCYE65EFXlnsA"
bot_id = groups[int(g_index)].id
bot = telebot.TeleBot(token)
bot = telegram.Bot(token)
print(bot.get_me())
bot.sendMessage(bot_id,text="testing the bot")
print("Message sent.")