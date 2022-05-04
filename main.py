# -*- coding: UTF-8 -*-
import requests,json,sys,time,os,random
from multiprocessing import Pool

'''
Office365 account authorization required：
files:	Files.Read.All、Files.ReadWrite.All、Sites.Read.All、Sites.ReadWrite.All
user:	User.Read.All、User.ReadWrite.All、Directory.Read.All、Directory.ReadWrite.All
mail:  Mail.Read、Mail.ReadWrite、MailboxSettings.Read、MailboxSettings.ReadWrite

Author:interestingcn01@gmail.com
Github:https://github.com/interestingcn/365E5_subscription 
'''

appName = '365E5_subscription'

# define your application id and secret
appSecret = ''
appId = ''

# Lines 20 to 25 are used to automatically write the secret informations. Do not write any code





# Lines 20 to 25 are used to automatically write the secret informations. Do not write any code

tokenFilePath = sys.path[0]+'/token.txt'

def welcome():
    msg = '''  ____    __ _____ ______ _____            _                   _       _   _             
 |___ \  / /| ____|  ____| ____|          | |                 (_)     | | (_)            
   __) |/ /_| |__ | |__  | |__   ___ _   _| |__  ___  ___ _ __ _ _ __ | |_ _  ___  _ __  
  |__ <| '_ \___ \|  __| |___ \ / __| | | | '_ \/ __|/ __| '__| | '_ \| __| |/ _ \| '_ \ 
  ___) | (_) |__) | |____ ___) |\__ \ |_| | |_) \__ \ (__| |  | | |_) | |_| | (_) | | | |
 |____/ \___/____/|______|____/ |___/\__,_|_.__/|___/\___|_|  |_| .__/ \__|_|\___/|_| |_|
                            ______                              | |                      
                           |______|Anterestingcn01@gmail.com    |_|   
--------------------------------------------------------------------------------------------                  
'''
    print(msg)


# Unified information output interface
def displayMsg(msg='',workname='Default'):
    now = time.asctime( time.localtime(time.time()) )
    print(f'{now} - {workname}: ' + msg)

# Update Token informations
def updateToken(refresh_token):
    headers={'Content-Type':'application/x-www-form-urlencoded'}
    data={'grant_type': 'refresh_token',
          'refresh_token': refresh_token,
          'client_id':appId,
          'client_secret':appSecret,
          'redirect_uri':'http://localhost:53682/'
         }
    html = requests.post('https://login.microsoftonline.com/common/oauth2/v2.0/token',data=data,headers=headers)
    jsontxt = json.loads(html.text)
    try:
        refresh_token = jsontxt['refresh_token']
        access_token = jsontxt['access_token']
    except:
        print(html.text)
        exit()
    with open(tokenFilePath, 'w+') as f:
        f.write(refresh_token)
    return access_token


# Active API
def activate(apiUrl,access_token):
    proxies = {"https": "127.0.0.1:4780"}
    headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.81",
    'Cache-Control': 'max-age=0',
    'Authorization':access_token,
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Content-Type':'application/json'
    }

    # Error retries
    attempts = 0
    success = False
    while attempts <= 5 and not success:
        try:
            request = requests.get(apiUrl, headers=headers, proxies=None, timeout=8)
            success = True
            if request.status_code == 200:
                displayMsg('[OK] - ' + apiUrl,'[PID:' + str(os.getpid()).rjust(5,'0') + ']')
                return True
            else:
                displayMsg('[FAILED] - ' + apiUrl,'[PID:' + str(os.getpid()).rjust(5,'0') + ']')
                return False
        except:
            attempts += 1
            time.sleep(2)
            if attempts >= 5:
                displayMsg('[FAILED NET] - ' + apiUrl)
                return False

# Main 
def main():
    if os.path.exists(tokenFilePath):    
        pass
    else:
        displayMsg('[Failed] - Missing information: refreshToken')
        with open(tokenFilePath,'w') as file:
            file.write('')
        exit()
    try:
        with open(tokenFilePath,'r') as file:
            refresh_token = file.read()
    except:
        displayMsg('[Failed] - can not open token file')
        exit()

    access_token = updateToken(refresh_token)

    # API List
    apiList = ['https://graph.microsoft.com/v1.0/me/drive/root',
               'https://graph.microsoft.com/v1.0/me/drive',
               'https://graph.microsoft.com/v1.0/drive/root',
               'https://graph.microsoft.com/v1.0/users',
               'https://graph.microsoft.com/v1.0/me/messages',
               'https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules',
               'https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta',
               'https://graph.microsoft.com/v1.0/me/drive/root/children',
               'https://graph.microsoft.com/v1.0/me/mailFolders',
               'https://graph.microsoft.com/v1.0/me/outlook/masterCategories'
               ]

    # Target API address pool 
    apiPool = []
    while len(apiPool) < 30:
        apiPool.append(random.choice(apiList)) 
    p = Pool(10)
    for apiUrl in apiPool:
        p.apply_async(activate, args=(apiUrl,access_token))
    p.close()
    displayMsg('[INFO] - Task start')
    p.join()
    displayMsg('[INFO] - Task end')


if __name__ == "__main__":
    welcome()
    main()