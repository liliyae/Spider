## 使用模拟器+fiddler+爬虫获取快手短视频

一次爬取的操作如下：

1、电脑端下载安装fiddler（https://www.telerik.com/download/fiddler/fiddler4），移动端下载软件快手极速版

2、下载安卓模拟器（注意安卓版本不要用最新的，最好4.0以下，高版本的安卓系统不支持以下安全证书）

3、配置fiddler，将手机or平板和电脑处于同一局域网下（连同一个wifi，或者同时连另一台设备的热点），手机端进行网络配置（教程在这里-> https://www.cnblogs.com/yyhh/p/5140852.html），
打开fiddler，手机端打开软件

4、这时fiddler抓到很多包，为了筛选出带有视频的包，你可以这么配置一下，配置好了选择Actions中的Run filterset now就可以了。

![image](https://user-images.githubusercontent.com/58354216/129336148-310ee19f-d8be-444e-b1c0-1f876fa779bc.png)

5、配置fiddler，得到上面这些包的路径
配置方法为，选择Rules，选择customize rules，搜索函数OnBeforeRequest
 
在这个函数的末尾添加下面这段代码：（记得ctrl+s保存）
```C
if (oSession.fullUrl.Contains("/feed/hot"))        
{            
		var fso;            
		var file;            
		fso = new ActiveXObject("Scripting.FileSystemObject");            
		file = fso.OpenTextFile ("D:\\scratch\\kuaishou3.1\\1.txt",8 ,true, true); //文件保存路径，可自定义            
		file.writeLine(oSession.GetRequestBodyAsString());            
		file.close();        
}
```

6、进入视频页面，发现你的fiddler中抓到了一些视频数据包。
 
7、点开任意一个视频数据包，将下面的蓝色链接复制，粘贴到kuaishou.py中。（只需要复制一次就好，因为每个人的账号不同，另外，这个是有时效性的，第二天需要再复制一次）注意只有蓝色链接，黑色字体不要~
 ![image](https://user-images.githubusercontent.com/58354216/129336633-0de959d8-ce5b-4479-8d88-016216ab39ce.png)


8、现在可以利用模拟器自动在这个页面不断滑动，获取链接。

9、不断滑动，当链接达到一定数量后，再开始爬取。

10、okay! 一次爬取就完成了. 这是针对移动端APP的爬取方式~
