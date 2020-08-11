linux 网卡 device not managed 错误

问题描述

今天我用VM虚拟机打开Kali Linux 2020（基于Debian的Linux发行版）的时候，Ethernet Network网卡打叉，并显示如下错误提示：

    device not managed

既然出现了上面这种状态，肯定是不能上网的，我用命令：ping baidu.com 都ping不通。
 
解决方法

解决这个“device not managed ”的问题也很简单，也不仅仅只适用于Kali Linux（Debian），Ubuntu系统也会遇到同样适用。

1、编辑 /etc/NetworkManager/NetworkManager.con

    vim /etc/NetworkManager/NetworkManager.conf

将其中的 managed=false 改为 managed=true

2、重启 network-manager service

    sudo service network-manager restart



