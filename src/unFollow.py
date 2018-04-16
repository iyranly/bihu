# coding: utf-8
from urllib import request, parse
import ssl
import json
import time

# 配置变量
config = {
    # 用户ID
    'userId':'',  # TODO, 你的用户id，PC上在币乎页面，按F12，network页面找到对应的请求，可以找到
    # 登录token
    'accessToken':'', # TODO, 你的token，登录后币乎服务器返回，获取方法与userId相同。
	# 粉丝条件，粉丝少于多少个时，取消关注
    'fansCondition':100 # 可以根据你的实际情况设置阈值条件
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

# 取消关注某人    
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

# 获取关注列表，pageNum为页序    
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
    log_content_format = '【%s】的粉丝数：%d，头像是:%s'
    if res == 1 and data_str["data"]["size"] > 0:
        pages = data_str["data"]["pages"]
        # 遍历关注对象
        for item in data_str["data"]["list"]:
            if item["userName"].startswith("币友_") \
            or item["userIcon"] == "img/bihu_user_default_icon.png"\
            or item["fans"] < config['fansCondition']:
                log_content = log_content_format % (item['userName'], item["fans"], item["userIcon"])
                print_info(log_content)
                # 昵称以币友_开始，userIcon为默认，且粉丝数小于配置的，取消关注
                unFollow(item["userId"],item['userName'])
    
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
        body = getUserFollowList(pageIndex)
        is_suc, pages = parse_follow_list(body)
        
		# 请求太频繁时，进入下面等待，一分钟检测一次
        while (not is_suc):
            print_info(body)
            print_info("60秒后请稍后重试")
            time.sleep(60)
            body = getUserFollowList(pageIndex)
            is_suc, pages = parse_follow_list(body)
            
Run()
print_info("程序已退出")