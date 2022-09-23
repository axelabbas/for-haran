import requests, os
from bs4 import BeautifulSoup as bs4
import pandas as pd
from prettytable import PrettyTable
from colorama import Fore, Style, init
import threading
import random
import ctypes
init()

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system("clear")
def logo():
    logo = '''
   ___ _                         _____        __       
  / _ \ |__   ___  _ __   ___    \_   \_ __  / _| ___  
 / /_)/ '_ \ / _ \| '_ \ / _ \    / /\/ '_ \| |_ / _ \ 
/ ___/| | | | (_) | | | |  __/ /\/ /_ | | | |  _| (_) |
\/    |_| |_|\___/|_| |_|\___| \____/ |_| |_|_|  \___/ 
    '''
    print(logo)
def auth(token):
    try:
        url = "https://apiforauth.team-api.repl.co/checkToken"

        payload=f'accessToken={token}'
        headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload) 
        return response.json()
    except:
        pass

def numberBook(number,proxy):
    try:
        npa= number[0:3]
        nxx= number[3:6]
        thoublock= number[6:11]
        proxies = {
    'https': proxy,
    'http': proxy,
        }
        url = f'http://www.fonefinder.net/findome.php?npa={npa}&nxx={nxx}&thoublock={thoublock}&usaquerytype=Search+by+Number&cityname='
        try:
            res = requests.get(url, proxies=proxies,timeout=7, allow_redirects=True).text
        except requests.exceptions.ProxyError as e:
            return {"status":'failed',"error":'proxy error'}
        except requests.exceptions.ConnectionError:
            return {"status":'failed',"error":'proxy error'}
        except requests.exceptions.ReadTimeout:
            return {"status":'failed',"error":'proxy error'}
        except ConnectionResetError:
            return {"status":'failed',"error":'proxy error'}
            
        
        if "no records found" in res.lower():
            return {"status":'failed',"error":'no records found'}
        elif "you must input more numeric digits" in res.lower():
            return {"status":'failed',"error":'not a valid number'}
        elif "exceeded 1000 searches today" in res.lower():
            return {"status":'failed',"error":'proxy error'}


        soup = bs4(res,'lxml')
        table = soup.find('table', {"bgcolor":"#FFFFCC"})
        for row in table.find_all('tr')[1:2]:
            data = row.find_all('td')
            row_data = [] 
            for index,td in enumerate(data):
                if index == 4:
                    if td.a:
                        carrier = td.a['href'].split(".net/")[1].split(".php")[0] 
                    else:
                        carrier = "Not Found"
                row_data.append(td.text.strip())
            row_data[-1] = carrier
        return {"status":'success',"table":row_data}
    except AttributeError:
        return {"status":'failed',"error":'proxy error'}
    except Exception as e:
            return {"status":'failed',"error":f'Unkown Error: {e}.. Retrying.'}
nums = open('input/numbers.txt','r').readlines()
proxies = open('input/proxy.txt','r').readlines()
done = 0
doneNums = []
tries = 0
badProxies = []
goodProxies = []
def mainThread():
    global done,tries
    
    while not len(doneNums) > len(nums):
        tries += 1
        ctypes.windll.kernel32.SetConsoleTitleW(f"NumInfo by AXELABBAS || tries: {tries} || success: {done}")
        if len(goodProxies)>0:
            proxy = random.choice(goodProxies)
        else: 
            proxy = random.choice(proxies)
        if proxy in goodProxies and proxy in badProxies:
            goodProxies.remove(proxy)
            continue
        number = random.choice(nums)
        if number in doneNums or proxy in badProxies:
            continue
        num = numberBook(number,proxy)
        if num['status'] == 'failed':
            if num['error'] == 'proxy error':
                    badProxies.append(proxy)
                    continue
            else:
                goodProxies.append(proxy)
                doneNums.append(number)
                continue
        print(Fore.CYAN)
        done +=1
        goodProxies.append(proxy)
        doneNums.append(number)  
        infoList = num['table'] 
        t = PrettyTable(['Area Code', 'Prefix', 'City Name', 'State', 'Company', 'Telco Type','Carrier'])
        t.add_row(infoList)
        carrier = infoList[-1]
        city = infoList[2]
        state = infoList[3]
        teleco = infoList[5]
        print(f"Information About '{number}'")
        print(t)
        if os.path.exists(f"output/{carrier}"):
            if os.path.exists(f"output/{carrier}/Full Capture.txt"):
                with open(f"output/{carrier}/Full Capture.txt",'a') as f:
                    f.write(f"{number}:{carrier}:{teleco}:{state}:{city}"+"\n")
            else:
                with open(f"output/{carrier}/Full Capture.txt",'w') as f:
                    f.write(f"{number}:{carrier}:{teleco}:{state}:{city}"+"\n")
        else:
            os.mkdir(f"output/{carrier}")
            with open(f"output/{carrier}/Full Capture.txt",'w') as f:
                    f.write(f"{number}:{carrier}:{teleco}:{state}:{city}"+"\n")
        if os.path.exists(f"output/{carrier}/Numbers.txt"):
            with open(f"output/{carrier}/Numbers.txt",'a') as f:
                f.write(f"{number}"+"\n")
        else:
            with open(f"output/{carrier}/Numbers.txt",'w') as f:
                f.write(f"{number}"+"\n")

def main():
    clear()
    print(Style.BRIGHT + Fore.CYAN)
    logo()
    print(55*'-')
    print(30*' ',Fore.RED,'coded by: @AXELABBAS',Fore.CYAN)
    print(30*' ',Fore.RED,'authorized to: @Charan_xD\n',Fore.CYAN)
    print(4*"\n")
    token = input('Enter your user token: ')
    clear()
    authent = auth(token)
    data = authent['data']
    if not data:
        print(Fore.RED+"Sorry, bad token") 
        quit()
    username = data[0]['username']
    userToken = data[0]['accessToken']
    print(f"{Fore.GREEN}Login Sucess, Welcome {username}!")
    print(2*"\n")
    print(Fore.CYAN)

    threads = []
    for i in range(15):
        thread1 = threading.Thread(target=mainThread)
        thread1.start()
        threads.append(thread1)
    for thread2 in threads:
        thread2.join()
main()
clear()
print(8*"\n"+Fore.GREEN+"Script done.")