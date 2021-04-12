# 杀死 Defunct process

有个问题困扰了我相当长一段时间：某个服务在重启或者关闭的时候，旧的服务进程有时候会进入Defunct状态，但是监听端口仍然被其绑定。此时kill -9 对此进程完全无效。旧进程维持Defunct状态的时间不一定，有时1-2分钟，有时要十几分钟，之后进程会自动消失。这时候才能启动新的服务程序，之前会由于端口冲突无法进行端口绑定。
     
”Defunct processes are processes that have become corrupted in such a way the no long can communicate (not really the right word, more like signal each other) with their parent or child process. So kill the parent or child and 99% of the time (around here at least) the defunct process will go away! No parent or child, you're out of luck, or look for a stuck automount.“
     
这个总结还是比较全的。提到杀死父进程、子进程、还有看看mount问题。

什么是看看mount问题呢？可以参考这个链接：[一个杀不死的小强，kill进程无效的原因](https://blog.51cto.com/liuqunying/1716678)，在2.6.33.1内核之前的一个NFS bug可能会导致此问题。

然后根据我的实际经验，其实还有一个办法：将所有与服务端口建立TCP连接的进程都关闭掉，这时候原服务进程也有可能（90%）马上就退出了。

总结一下，kill defunct process的步骤大概如下：
1）杀掉父进程。ps -ef | grep defunct ，前三列分别是UID、PID、PPID（这就是进程他爹啦）。把进程他爹杀杀杀。
2）杀掉子进程。ps -ef --forest。把子进程杀杀杀。
3）也许是nfs的问题，look into it。
4）如果这个进程是个内部服务，可以尝试将所有与该服务有建立TCP连接的进程都关闭掉。netstat -tnp | grep 端口号。最后一列是pid，杀杀杀。我要说明一下，这个方法我并没有找到理论支持，但在CentOS5.4环境下，它很多次帮我解决了问题。
5）如果到了这一步defunct进程还健在，It's very unlucky. 有两个艰难的选择：1、重启服务器； 2、等待，一般不到20分钟这个defunct进程会自动消失。