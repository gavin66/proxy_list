# proxy_list
爬取 IP 代理以供爬虫等业务使用。

Python 新手，代码不规范请见谅。此项目也是练手的，借鉴了 [qiyeboy](https://github.com/qiyeboy) / [IPProxyPool](https://github.com/qiyeboy/IPProxyPool) 的项目。

需要免费代理的可以试试，如果对您有帮助，希望给个 Star ⭐，谢谢！😁😘🎁🎉



## 特性

* 爬取、验证、存储、Web API 多进程分工合作。

* 验证代理有效性时使用协程来减少网络 IO 的等待时间。

* 持久化（目前使用 Redis）爬取下来的代理。

* 提供 Web API，随时提取与删除代理。

  ​

## 使用

**使用 Python3.6 开发的项目，没有对其他版本 Python 测试**

克隆源码

```sh
git clone git@github.com:gavin66/proxy_list.git
```

安装依赖

```sh
pip install -r requirements.txt
```

运行脚本

```sh
python run.py
```



### Web API

[查看文档](https://htmlpreview.github.io/?https://github.com/gavin66/proxy_list/blob/master/doc/web_api.html)

文档截图
![3](https://github.com/gavin66/proxy_list/blob/master/doc/p3.png?raw=true)

直接获取一个速度最快的代理
![1](https://github.com/gavin66/proxy_list/blob/master/doc/p1.png?raw=true)

获取 https 的匿名代理，取前5个速度最快的
![2](https://github.com/gavin66/proxy_list/blob/master/doc/p2.png?raw=true)




