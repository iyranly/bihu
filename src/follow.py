# coding: utf-8
from urllib import request, parse
import ssl
import json
import time

# 关注流程
# 1、遍历热门中的文章列表；
# 2、如果未关注，查看当前收益是否达到moneyCondition，如果达到这关注；
# 3、继续循环，直到没有

# 优点
# 关注到的，都是写文章的，并目前收益还不错的。

# 配置变量
config = {
    # 用户ID
    'userId':'',  # TODO, 你的用户id，PC上在币乎页面，按F12，network页面找到对应的请求，可以找到
    # 登录token
    'accessToken':'', # TODO, 你的token，登录后币乎服务器返回，获取方法与userId相同。
    # 收益，收益多于多少时关注
    'moneyCondition':100 # 可以根据你的实际情况设置阈值条件
}

def datetime_str():  
    format = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(time.time())
    dt = time.strftime(format,value)  
    return dt

# 打印日志信息
def print_info(info):
    log = "[%s]--%s" % (datetime_str(), info)
    print(log)

# 关注某人 
# https://be02.bihu.com/bihube-pc/api/content/follow
def Follow(subjectUserId, userName):
    print_info("正在关注【%s】..." % (userName))
    url = r'https://be02.bihu.com/bihube-pc/api/content/follow'
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Content-Type': r'application/x-www-form-urlencoded;charset=utf-8',
        'Referer': r'https://bihu.com/people/' + subjectUserId,
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    
    data = {
        'userId': config['userId'],
        'accessToken': config['accessToken'],
        'subjectUserId': subjectUserId
    }
    context = ssl._create_unverified_context()
    data = parse.urlencode(data).encode('utf-8')
    req = request.Request(url, headers=headers, data=data)

    rsp = ""
    try:
        rsp = request.urlopen(req, context = context).read()
        rsp = rsp.decode('utf-8')
    except e:
        print_info(str(e.code) + '\r\n' + e.reason);

    print_info("关注【%s】返回：%s" % (userName, rsp))

    return rsp

# 获取热门文章列表，code为板块的名字，pageNum为页序
# 如果code为空，这Referer为https://bihu.com/?category=recommend
# 如果code不为空，则Referer为https://bihu.com/?category=hots&code=BTC
def getHotArtList(pageNum = 1, code = ''):
    print_info("查询第【" + str(pageNum) + "】页热门文章" )
    url = r'https://be02.bihu.com/bihube-pc/api/content/show/hotArtList'
    
    # 去掉空格
    code = code.strip()
    
    # Referer头默认为热门页面
    referer = r'https://bihu.com/?category=recommend' 
    if code =="":
        referer = r'https://bihu.com/?category=hots&code=' + code
    
    # 组装头信息
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Content-Type': r'application/x-www-form-urlencoded;charset=utf-8',
        'Referer': referer,
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    
    data = {
        'userId': config['userId'],
        'accessToken': config['accessToken'],
        'pageNum': pageNum
    }
    
    if len(code) != 0:
        data['code'] = code
    
    context = ssl._create_unverified_context()
    data = parse.urlencode(data).encode('utf-8')
    req = request.Request(url, headers=headers, data=data)
    
    rsp = ""
    try:
        rsp = request.urlopen(req, context = context).read()
        rsp = rsp.decode('utf-8')
    except urllib2.URLError as e:
        print_info(str(e.code) + '\r\n' + e.reason);

    # print_info(rsp)
    return rsp

def parseHotArtList(body):
    data_str = json.loads(body);
    res = data_str['res'];

    # 请求是否成功
    is_succ = False;
    pages = 0;
    log_content_format = '【%s】的文章，点赞量：%d，收益:%s，加为关注 :)'
    if res == 1 and data_str["data"]["size"] > 0:
        pages = data_str["data"]["pages"]
        # 遍历关注对象
        for item in data_str["data"]["list"]:
            if item["follow"] == 0 \
            and item["money"] >= config['moneyCondition']:
                log_content = log_content_format % (item['userName'], item["ups"], item["money"])
                print_info(log_content)
                # 热门里面，如果未关注，且收益大于设定值，关注
                Follow(item["userId"],item['userName'])
                time.sleep(0.5)
    
    if res == 1:
        is_succ  = True;

    return is_succ, pages

def Run():
    # 第一次获取，为了拿到页数，好做循环
    pageIndex = 0
    pages = 1
    is_suc = True
 
    while is_suc and pageIndex < pages:
        pageIndex += 1
        time.sleep(1)
        body = getHotArtList(pageIndex)
        is_suc, pages = parseHotArtList(body)
        
		# 请求太频繁时，进入下面等待，一分钟检测一次
        while (not is_suc):
            print_info(body)
            print_info("60秒后请稍后重试")
            time.sleep(60)
            body = getHotArtList(pageIndex)
            is_suc, pages = parseHotArtList(body)
          
Run()
print_info("程序已退出")