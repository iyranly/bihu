### 币乎小助手

BY [一休哥](https://bihu.com/people/197646)

#### 币乎取消关注小助手
**运行效果图**：

![取消关注运行效果图](https://bihu2001.oss-cn-shanghai.aliyuncs.com/img/e168d5b9260bd21b4ca39fd78bcb800b.gif?x-oss-process=style/size_lg)

**使用说明**：
- 安装`python`运行环境：[Python 3.6.5](https://www.python.org/ftp/python/3.6.5/python-3.6.5.exe)
- 下载`src`文件夹下的脚本。
- 在电脑端登录币乎，浏览器上按键盘F12，抓包，`network`下，看getUserFollowList请求的参数，拿到`userId`，和`accessToken`。
![image](https://bihu2001.oss-cn-shanghai.aliyuncs.com/img/28746efe93791033372a1718621fa77e.png?x-oss-process=style/size_lg)

- 打开.py文件，修改`config`，将拿到的`userId`和`accessToken`填入:
```
# 配置变量
config = {
    # 用户ID
    'userId':'你的userId填到这里',  # TODO, 你的用户id，PC上在币乎页面，按F12，network页面找到对应的请求，可以找到
    # 登录token
    'accessToken':'你的token填到这里' # TODO, 你的token，登录后币乎服务器返回，获取方法与userId相同。
}
```
- 双击运行.py

若有问题，可在bihu我的[首页内的文章中](https://bihu.com/people/197646)留言。
