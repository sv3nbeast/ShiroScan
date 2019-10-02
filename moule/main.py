#!/usr/bin/env python
# _*_ coding:utf-8 _*_




def scripts(url,command):
    processor = Idea()
    processed = processor.process(url,command)


class Idea(object):
    PLUGINS = {}

    def process(self,url,command,plugins=()):
        if plugins is ():
            for plugin_name in self.PLUGINS.keys():
                try:
                    print("[*]  开始检测模块",plugin_name)
                    self.PLUGINS[plugin_name]().process(url,command)
                except:
                    print ("[-]{} 检测失败，请检查网络连接或目标是否存活".format(plugin_name))
        else:
            for plugin_name in plugins:
                try:
                    print("[*]开始检测 ",self.PLUGINS[plugin_name])
                    self.PLUGINS[plugin_name]().process(url,command)
                except:
                    print ("[-]{}检测失败，请检查网络连接或目标是否存活".format(self.PLUGINS[plugin_name]))
        return

    @classmethod
    def plugin_register(cls, plugin_name):
        def wrapper(plugin):
            cls.PLUGINS.update({plugin_name:plugin})
            return plugin
        return wrapper
