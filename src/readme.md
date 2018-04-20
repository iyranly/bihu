# 币乎小助手

BY [一休哥](https://bihu.com/people/197646)

#### 4.币乎个人专属二维码的生成（已开源）
---
**代码地址**
币乎个人主页二维码的生成，代码已经上传至[github](https://github.com/iyranly/bihu.git)

**实现原理**：
1、先生成一个无logo的二维码；
2、调用userHomePage接口，获取到主页上的头像相对路径；
3、拼接上固定的字符串，形成一个完整的图片地址；
4、通过这个地址将图片请求下来，贴到二维码上；
5、将二维码显示出来。
6、将二维码保存到桌面上的bihu_logo.png中。

**如何使用该代码生成你的专属二维码**：
1、安装`python`运行环境：[Python 3.6.5](https://www.python.org/ftp/python/3.6.5/python-3.6.5.exe)
2、下载[github](https://github.com/iyranly/bihu.git)下的`src`文件夹下的脚本。
3、打开.py文件，修改`config`中的`homepage`，改成你的主页地址即可
```python
    # 配置变量
    config = {
	    'homepage':**'https://bihu.com/people/197646'**,  # TODO, 你的主页，PC上在币乎主页面，用于显示二维码头像
}
```
5、双击运行Bihu_QRcode.py，即可。

若有问题，可在bihu我的[首页内的文章中](https://bihu.com/people/197646)留言。
