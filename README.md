# proxy_list
爬取 IP 代理以供爬虫等业务使用。

个人的练手项目。借鉴了 [qiyeboy](https://github.com/qiyeboy) / [IPProxyPool](https://github.com/qiyeboy/IPProxyPool) 的项目。

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



