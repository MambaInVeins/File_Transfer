
怎么把一个命令设为全局可见的呢？ 

比方说在linux里，我们可以在任何目录下输入route命令什么的。但是我安装了一个软件，比如是xl2tpd,这个命令只有在它的安装目录/root/xl2tp/这个目录下可见，我想把它设为像route那那样的形式，全局可见，有什么办法么？

要么把它拷贝或者创建链接到PATH设置的路径里去，要么把它的路径设置到PATH里去 

1.
ln -s /root/xl2tp/xl2tpd  /usr/sbin/xl2tpd


2.修改root的~/.bash_profile文件 
追加
export PATH=$PATH:/root/xl2tp
然后执行source ~/.bash_profile 