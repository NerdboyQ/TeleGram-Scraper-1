from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import os, sys, pandas, openpyxl
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
print('')
print("""
    To scrape all groups, enter '*'
    To cancel scraping, enter 'x' or 'c'.
""")
g_index = input(gr+"[+] Enter a Number : "+re)
if g_index == "c" or g_index == "x" or g_index == "":
    print("\nScraper cancelled.\n")

elif g_index == "*":
    i=0
    #participants = client.get_participants(groups[0],aggressive=True)
    #col_headers = list(participants[0].to_dict().keys())
    #print(col_headers)
    #df = df.assign(**dict.fromkeys(headers,0))
    for g in groups:
        print(gr+'['+cy+str(i)+']' + ' - ' + g.title)
        target_group=groups[i]
        print(gr+f"[+] Fetching Members...:\n {target_group.title}")
        '''time.sleep(1)
        all_participants = []
        all_participants = client.get_participants(target_group,aggressive=True)
        temp_dict = {}
        for user in all_participants:
            temp_dict["group"] = target_group.title
            for h in headers:
                if h != "group":
                    temp_dict[h] = user.to_dict()[h]
            #print(temp_dict)
            df = df.append(temp_dict, ignore_index=True)
            #break'''

        i+=1
        #break
    print(df)
    #xl_file = f"group_export{getTimeStamp()}.xlsx"
    xl_file = f"input_members.xlsx"
    df.to_excel(xl_file,index=False)
    df.to_csv(xl_file.replace("xlsx","csv"),index=False)
    if len(df.columns) > 0:
        wb = openpyxl.load_workbook(xl_file)
        ws = wb.worksheets[0]
        tbl = openpyxl.worksheet.table.Table(displayName="groups",ref=f"A1:{chr(len(df.columns)+64)}{len(df['group'])+1}")
        style = openpyxl.worksheet.table.TableStyleInfo(name="TableStyleMedium9",showFirstColumn=False,showLastColumn=False,showRowStripes=True,showColumnStripes=False)
        tbl.tableStyleInfo = style
        ws.add_table(tbl)
        wb.save(xl_file)
else:
    print(gr+'['+cy+str(i)+']' + ' - ' + g.title)
    target_group=groups[int(g_index)]
    print(gr+'[+] Fetching Members...')
    print(f"t_group: {target_group.title}")
    time.sleep(1)
    all_participants = []
    all_participants = client.get_participants(target_group,aggressive=True)
    temp_dict = {}
    for user in all_participants:
        temp_dict["group"] = target_group.title
        for h in headers:
            if h != "group":
                temp_dict[h] = user.to_dict()[h]
        #print(temp_dict)
        df = df.append(temp_dict, ignore_index=True)

    i+=1
    print(df)
    #xl_file = f"group_export{getTimeStamp()}.xlsx"
    xl_file = f"input_members.xlsx"
    df.to_excel(xl_file,index=False)
    df.to_csv(xl_file.replace("xlsx","csv"),index=False)
    if len(df.columns) > 0:
        wb = openpyxl.load_workbook(xl_file)
        ws = wb.worksheets[0]
        tbl = openpyxl.worksheet.table.Table(displayName="groups",ref=f"A1:{chr(len(df.columns)+64)}{len(df['group'])+1}")
        style = openpyxl.worksheet.table.TableStyleInfo(name="TableStyleMedium9",showFirstColumn=False,showLastColumn=False,showRowStripes=True,showColumnStripes=False)
        tbl.tableStyleInfo = style
        ws.add_table(tbl)
        wb.save(xl_file)
