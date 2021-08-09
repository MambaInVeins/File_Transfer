https://blog.csdn.net/weixin_48184612/article/details/114577427


## 安装

pwndbg

    $ git clone https://github.com/pwndbg/pwndbg 
    $ cd pwndbg
    $ ./setup.sh

peda

    $ git clone https://github.com/longld/peda

gef

    $ git clone https://github.com/hugsy/gef

peda-heap

    $ git clone https://github.com/Mipu94/peda-heap


## 配置

首先需要把脚本中的/home/mamba/Documents/替换成你的插件保存位置，并且把/home/mamba/.gdbinit语句中的ams更改为你的系统用户名。

$ sudo rm ~/.gdbinit
$ sudo chmod 777 /home/mamba/.gdbinit


脚本如下：

    #!/bin/bash
    read -p $'请选择将要使用的gdb插件.\n[1]pwndbg\n[2]gef\n[3]peda\n[4]pead-heap\n>> ' plugin
    if ((plugin==1))
    then 
        echo "source /home/ams/Documents/pwndbg/gdbinit.py" > /home/ams/.gdbinit
    elif ((plugin==2))
    then 
        echo "source /home/ams/Documents/gef/gef.py" > /home/ams/.gdbinit
    elif ((plugin==3))
    then
        echo "source /home/ams/Documents/peda/peda.py" > /home/ams/.gdbinit
    elif ((plugin==4))
    then
        echo "source /home/ams/Documents/peda-heap/peda.py" > /home/ams/.gdbinit
    else
        echo $'WRONG!\n'
    fi

