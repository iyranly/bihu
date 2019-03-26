# coding: utf-8
from PIL import Image
import qrcode
import requests
from urllib import request, parse
import ssl
import json
import time
import winreg   # winreg.OpenKey

# 配置变量
config = {
    # 用户ID
    'homepage':'https://bihu.com/people/197646',  # TODO, 你的主页，PC上在币乎主页面，用于显示二维码头像
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

# 获取桌面路径    
def get_desktop():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders',)
    return winreg.QueryValueEx(key, "Desktop")[0]

# 返回：https://bihu2001.oss-cn-shanghai.aliyuncs.com/img/41c68e8af64b42cd18bd9139d90b502c.jpg?x-oss-process=style/size_head    
def getUserLogo(homeUrl):
    print_info("正在加载首页：" + homeUrl)
    url = r'https://be02.bihu.com/bihube-pc/api/content/show/userHomePage'
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Content-Type': r'application/x-www-form-urlencoded;charset=utf-8',
        'Referer': homeUrl,
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    
    data = {
        'queryUserId': homeUrl.split('/')[-1]
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

    data = json.loads(rsp)
    if data['res'] == 1:
        print_info("已拿到头像地址：" + data['data']['userIcon'] )
        logoUrl = 'https://bihu2001.oss-cn-shanghai.aliyuncs.com/'+ data['data']['userIcon'] + '?x-oss-process=style/size_head'
        return logoUrl
    
    return ""

def GenerateBihuQRCode(data):
    # 构造一个二维码对象，填充数据
    qr = qrcode.QRCode(version=5,error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=8,border=4)
    qr.add_data(data)
    qr.make(fit=True)

    # 获得Image实例并把颜色模式转换为RGBA
    img = qr.make_image()
    img = img.convert("RGBA")

    # 获取主页的头像地址
    logoUrl = getUserLogo(config['homepage']);
    
    # 如果获取到，则加上头像：
    if logoUrl:
        print_info("加载头像...")
        icon = Image.open(requests.get(logoUrl, stream=True).raw)
        print_info("加载头像成功...")

        # 计算logo的尺寸
        img_w,img_h = img.size
        factor = 4
        size_w = int(img_w / factor)
        size_h = int(img_h / factor)

        # 比较并重新设置logo文件的尺寸
        icon_w,icon_h = icon.size
        if icon_w > size_w:
            icon_w = size_w
        if icon_h > size_h:
            icon_h = size_h
        icon = icon.resize((icon_w,icon_h),Image.ANTIALIAS)

        # 计算logo的位置，并复制到二维码图像中
        w = int((img_w - icon_w)/2)
        h = int((img_h - icon_h)/2)
        icon = icon.convert("RGBA")
        img.paste(icon,(w,h),icon)
    
    return img

def Run():
    # 生成币乎二维码
    img = GenerateBihuQRCode(config['homepage'])

    # 保存二维码到桌面
    save_path = get_desktop() + '/bihu_logo.png';
    img.save(save_path)
    print_info('二维码已保存到桌面：' + '/bihu_logo.png')
    
    # 显示二维码图片
    img.show()
    print_info('这是你的币乎二维码:)，请惠存')
    
Run()