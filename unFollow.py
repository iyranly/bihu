# coding: utf-8
from urllib import request, parse
import ssl
import json
import time

# 配置变量
config = {
    # 用户ID
    'userId':'',       # TODO
    # 登录token
    'accessToken':''   # TODO
}

def datetime_str():  
    format = '%Y-%m-%d %H:%M:%S'  
    value = time.localtime(time.time())
    dt = time.strftime(format,value)  
    return dt

def print_info(info):
    log = "[%s]--%s" % (datetime_str(), info)
    print(log)

# 获取关注列表    
def unFollow(subjectUserId, userName):
    print_info("取消关注【%s】..." % (userName))
    url = r'https://be02.bihu.com/bihube-pc/api/content/unFollow'
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Content-Type': r'application/x-www-form-urlencoded;charset=utf-8',
        'Referer': r'https://bihu.com/people/' + config['userId'] + r'/index=2',
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
    except urllib2.URLError as e:
        print_info(str(e.code) + '\r\n' + e.reason);

    print_info("取消关注【%s】返回：%s" % (userName, rsp))

    return rsp

# 获取关注列表    
def getUserFollowList(pageNum):
    print_info("查询第【" + str(pageNum) + "】页关注列表" )
    url = r'https://be02.bihu.com/bihube-pc/api/content/show/getUserFollowList'
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Content-Type': r'application/x-www-form-urlencoded;charset=utf-8',
        'Referer': r'https://bihu.com/people/' + config['userId'] + r'/index=2',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    
    data = {
        'queryUserId': config['userId'],
        'userId': config['userId'],
        'accessToken': config['accessToken'],
        'pageNum': pageNum
    }
    context = ssl._create_unverified_context()
    data = parse.urlencode(data).encode('utf-8')
    req = request.Request(url, headers=headers, data=data)

    rsp = ""
    try:
        rsp = request.urlopen(req, context = context).read()
        rsp = rsp.decode('utf-8')
    except urllib2.URLError as e:
        print_info(str(e.code) + '\r\n' + e.reason);

    return rsp

def parse_follow_list(body):
    data_str = json.loads(body);
    res = data_str['res'];

    # 请求是否成功
    is_succ = False;
    pages = 0;
    log_content_format = '【%s】的头像是:%s'
    if res == 1 and data_str["data"]["size"] > 0:
        pages = data_str["data"]["pages"]
        # 遍历关注对象
        for item in data_str["data"]["list"]:
            if item["userName"].startswith("币友_") or item["userIcon"] == "img/bihu_user_default_icon.png":
                #print(item)
                log_content = log_content_format % (item['userName'], item["userIcon"])
                print_info(log_content)
                # 取消关注
                unFollow(item["userId"],item['userName'])
    
    if res == 1:
        is_succ  = True;

    return is_succ, pages

def Run():
    # 第一次获取
    pageIndex = 1
    body = getUserFollowList(pageIndex)
    is_suc, pages = parse_follow_list(body)
    while is_suc and pageIndex < pages:
        pageIndex += 1
        time.sleep(10)
        body = getUserFollowList(pageIndex)
        is_suc, pages = parse_follow_list(body)

    if (not is_suc):
        print_info(body)
        print_info("请稍后重试")
        
Run()
print_info("程序已退出")