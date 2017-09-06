# -*- coding: UTF-8 -*-
import random

# http://www.useragentstring.com/pages/useragentstring.php
USER_AGENTS = [
    "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
    "Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14",
    "Mozilla/5.0 (Windows NT 6.0; rv:2.0) Gecko/20100101 Firefox/4.0 Opera 12.14",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0) Opera 12.14",
    "Opera/12.80 (Windows NT 5.1; U; en) Presto/2.10.289 Version/12.02",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2226.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
    "Mozilla/5.0 (X11; Linux i586; rv:31.0) Gecko/20100101 Firefox/31.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20130401 Firefox/31.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
]


# 模拟浏览器爬取代理 http 头信息
def get_http_header():
    return {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'h-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        'Connection': 'keep-alive',
        'User-Agent': random.choice(USER_AGENTS)
    }


# 持久化
# 目前只支持 redis
# 这里只能修改你的 redis 连接字符串
PERSISTENCE = {
    'type': 'redis',
    'url': 'redis://127.0.0.1:6379/1'
}

# 协程并发数
# 爬取下来的代理测试可用性时使用，减少网络 io 的等待时间
COROUTINE_NUM = 50

# 保存多少条代理
# 默认200，如果存储了200条代理并不删除代理就不会再爬取新代理
PROXY_STORE_NUM = 300

# 如果保存的代理条数已到阀值，爬取进程睡眠秒数
# 默认60秒，存储满200条后爬虫进程睡眠60秒，醒来后如果还是满额继续睡眠
PROXY_FULL_SLEEP_SEC = 60

# 已保存的代理每隔多少秒检测一遍可用性
PROXY_STORE_CHECK_SEC = 1200
