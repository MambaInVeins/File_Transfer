
## ubuntu工具

### UltraEdit

需要下载安装包 http://www.ultraedit.com/downloads/uex.html 下载对应的版本

在终端下执行安装：sudo dpkg -i uex_4.2.0.11_amd64.deb

UE 在处理文档方面能力强，但是从网上下载的只是试用版30天，30天到期后到用户目录下如：/home/user/.idm 文件夹下面，删除uex文件夹，重新打开UE，就又可以试用30天啦！ 

[ubuntu下安装UltraEdit](https://www.cnblogs.com/caidi/p/4065678.html)

### Burpsuite

[爱盘下载](https://down.52pojie.cn/Tools/Network_Analyzer/Burp_Suite_Pro_v1.7.37_Loader_Keygen.zip)

ubuntu中有无java环境 

    java -version

如果没有 

    sudo apt-get install  -y openjdk-8-jre 

激活

    sudo chmod +x burpsuite_pro_v1.7.37.jar  burp-loader-keygen.jar 

    java -Xbootclasspath/p:burp-loader-keygen.jar -jar burpsuite_pro_v1.7.37.jar

复制相关激活码并填写

设置burpsuite别名

    gedit ~/.bashrc

在打开的文件最后添加下面一行

    alias burpsuite="java -Xbootclasspath/p:/home/mamba/Documents/burpsuite/burp-loader-keygen.jar -jar /home/mamba/Documents/burpsuite/burpsuite_pro_v1.7.37.jar"

让bashrc文件立即生效

    source ~/.bashrc

运行burpsuite

    burpsuite

[Ubuntu18.04 安装破解版本的burpsuite1.73 Pro的方法](https://blog.csdn.net/qq_34626094/article/details/113115707)

## Docker镜像

upload-labs靶场，并且将其映射到13000端口上

    docker pull c0ny1/upload-labs
    docker run -d -p 13000:80 c0ny1/upload-labs:latest

DVWA靶场，并且将其映射到13001端口上

    docker pull infoslack/dvwa
    #第一种方法： 这种会启动一个密码随机的mysql服务
    docker run --name dvwa -d -p 13001:80 infoslack/dvwa 
    #第二种方法：这种会以自定义的密码启动mysql服务
    docker run --name dvwa -d -p 80:80 -p 3306:3306 -e MYSQL_PASS="mypass" infoslack/dvwa

pikachu靶场，并且将其映射到13002端口上

    docker pull area39/pikachu:latest
    docker run -d -p 13002:80 area39/pikachu:latest

[docker安装uploads-lad并定时刷新环境](https://blog.csdn.net/qq_19309473/article/details/107202812)

[docker安装dvwa](https://blog.csdn.net/qq_19309473/article/details/107202812)

