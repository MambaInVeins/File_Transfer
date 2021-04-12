MikroTik RouterOS软路由常用命令

MikroTik RouterOS是一种路由操作系统，是基于Linux核心开发，兼容x86 PC的路由软件,并通过该软件将标准的PC电脑变成专业路由器，在软件RouterOS 软路由图的开发和应用上不断的更新和发展，软件经历了多次更新和改进，使其功能在不断增强和完善。特别在无线、认证、策略路由、带宽控制和防火墙过滤等功能上有着非常突出的功能，其极高的性价比，受到许多网络人士的青睐。


在没有条件购买和实用硬件路由器或者交换的时候，这款软路由可以作为一项参考。

    主页地址：https://mikrotik.com/

    wiki文档：https://wiki.mikrotik.com/wiki/Main_Page
    好了，有什么本文档没有详细叙述的命令或者实用经验，大家可以通过官网和wiki来下载OS和阅读相关的文章 

一、登录方式

    1、winbox：这款官方的工具提供客户端的方式登录RouterOS的系统界面，这样对于一个小白用户或者有网络基础的童鞋都可以很明白的使用
    2、web：RouterOS提供80端口的访问方式来像winbox一样来登录管理RouterOS
    3、ssh：RouterOS提供标准的22端口来访问RouterOS，通过命令行的方式管理RouterOS。这是很多linux和网络工程师比较喜欢的一种管理界面。

二、ssh登录操作

    1、routeros默认使用的用户名是admin，密码为空
    2、ssh端口号是默认的22端口
    3、端口号可以更改 

三、常用命令

修改用户密码

    [admin@MikroTik]>/user                               #进入操作路径

    [admin@MikroTik]/user>print                           #显示RouterOS用户

    [admin@MikroTik]/user>set admin password=123456        #修改admin用户密码为123456

    [admin@MikroTik] /user> /                              #返回根目录

在当前用户下修改密码

    [admin@MikroTik]>password                             #修改本目录用户密码

备份命令

    [admin@MikroTik]>/system backup                           #进入操作路径

    [admin@MikroTik] /system backup>save name=testbackup         #备份名为testbackup

    [admin@MikroTik] /system backup>load name=testbackup         #载入备份testbackup

    [admin@MikroTik]>file print                                                                   #查看备份情况

导出指令

    [admin@MikroTik]>ip address print                          #查看IP

    [admin@MikroTik]>/ip address                              #进入IP操作路径

    [admin@MikroTik]/ip address>export file=address  #导出一个名为address的IP地址配置参数

    [admin@MikroTik]>export compact                          #查看IP地址配置参数

系统重启与关机

    [admin@MikroTik]>system reboot                         #系统重启

    [admin@MikroTik]>system shutdown                      #系统关机

修改RouterOS主机名

    [admin@MikroTik]>system identity print                     #查看RouterOS主机名

    [admin@MikroTik]>system identity set name=MyRouterOS  #修改RouterOS主机名为MyRouterOS

系统资源管理

    [admin@MikroTik] > /system resource                        #操作路径

    [admin@MikroTik] /system resource> print              #查看CPU占用率\内存\硬盘等使用情况

    [admin@MikroTik] /system resource> monitor           #查看CPU和空闲内存使用情况

开通ssh远程

    [admin@MikroTik] > ip service print                                             #查看服务

    [admin@MikroTik] > ip service enable ssh                                  #开启SSH服务

    [admin@MikroTik] > ip service disable ssh                                 #关闭SSH服务

    [admin@MikroTik] > ip service set ssh port=22 address=10.8.9.11   #允许10.8.9.11访问SSH访问，其它IP都均被拒绝

Interface接口基本操作

    [admin@MikroTik] > interface print                                              #显示接口状态

    [admin@MikroTik] > interface enable ether1            #启动ether1网卡

    [admin@MikroTik] > interface print stats               #显示接口状态+静态流量

    [admin@MikroTik] > interface monitor-traffic ether1     #监测网卡动态流量

    [admin@MikroTik] > interface ethernet print detail                #显示网卡参数

IP配置与ARP

    [admin@MikroTik] > ip address add address=192.168.10.1/24 interface=ether2   #添加IP地址到ether2接口上

    [admin@MikroTik] > ip address print                                           #显示IP地址

    [admin@MikroTik] > ip arp print                                                    #显示arp信息

    [admin@MikroTik] > ip arp add address=192.168.10.100 interface=00:23:24:2e:78:3e   #添加静态IP与ARP

    [admin@MikroTik] >/interface ethernet set ether2 arp=reply-only  #设置ether2接口非静态的ARP条目将无法与路由进行通信

防火墙过滤(firewall Filte)----域名过滤

    [admin@MikroTik]>ip firewall filter add action=drop chain=forward content=www.jd.com

防火墙过滤(firewall Filte)----端口映射将内网主机192.168.10.200的3389端口映射到外网的9999端口

    [admin@MikroTik] > ip firewall nat add chain=dstnat protocol=tcp dst-port=9999 in-interface=WAN action=dst-nat to-addresses=192.168.10.200 to-ports=3389

四、什么是 NPK 文件

NPK 扩展名指的是用于输送和安装更新的MikroTik路由器软件包文件。该路由器的MikroTik操作系统软件的信息存储在这些文件。此信息包括IP地址，IP服务，以太网接口，电子邮件设置，串行端口和本地用户管理，桥配置，以及信息包和系统资源管理。这些文件保存在一个压缩的二进制包格式。