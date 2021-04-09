centos离线安装gdb

## 下载并解压gdb安装包

打开页面http://ftp.gnu.org/gnu/gdb/

选择合适的安装包，在这里，我下载的gdb-7.0.1a.tar.gz

解压缩包，输入命令：tar xzvf gdb-7.0.1a.tar.gz

## 编译gdb

进入解压缩出来的目录gdb-7.0.1

输入命令: ./configure

输入命令：make

输入命令：make install

如果没有报错，此时gdb便编译好了。到/gdb-7.0.1/gdb/目录中，执行./gdb -v，可以查看到gdb的版本。若要让gdb可在任意目录下启动，创建链接到PATH设置的路径里去，或者把它的路径设置到PATH里去。
    
## 踩坑记录

make时可能报错error：no termcap library found

解决办法

1.首先网上下载termcap源码包

    wget http://ftp.gnu.org/gnu/termcap/termcap-1.3.1.tar.gz

2.解压

     tar -zxv -f   termcap-1.3.1.tar.gz
     
3.进入termcap文件夹,编译termcap

    cd termcap-1.3.1
    ./configure 
    make
    sudo make install

4.再重新安装gdb成功。 


