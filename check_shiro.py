import requests
import sys
#from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings()

f=open('ip.txt','r')
lines=f.readlines()
f.close()

header={
    'User-agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0;',
    'Cookie':'rememberMe=xxx'

    }
check="rememberMe"


with open("shiro.txt","w") as f:
    for line in lines:
        try:
            k = requests.get(line,headers=header,verify=False,timeout=10)
            l = str(k.headers)
            if check in l:
                print("[+ "+"存在shiro:"+line)
                f.write(line+"\n")
            else:
               
                print("[- "+"无shiro:"+line)
        except Exception as e:
            pass



print("全部check完毕，请查看当前目录下的shiro.txt")
                

            
