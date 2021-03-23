centos如何给用户提权到root


方法一：打开终端 输入 sudo -i 然后输入当前用户的密码；

方法二：打开终端输入su root 或su - ,然后输入root用户密码；


其中方法一可能会报错：

当我们使用sudo命令切换用户的时候可能会遇到提示以下错误：xxx is not in the sudoers file. This incident will be reported，xxx是你当前的用户名，究其原因是用户没有加入到sudo的配置文件里。

解决办法：

    首需要切换到root身份
    $su -
    (注意有- ，这和su是不同的，在用命令"su"的时候只是切换到root，但没有把root的环境变量传过去，还是当前用户的环境变量，用"su -"命令将环境变量也一起带过去，就象和root登录一样)

    然后
    $visudo     //切记，此处没有vi和sudo之间没有空格

    1、移动光标，找到
    ## Allow root to run any commands anywhere
    root ALL=(ALL) ALL，
    2、按a，进入append模式
    3、在下面添加一行
    xxx ALL=(ALL) ALL 其中xxx是你要加入的用户名称
    4、按Esc
    5、输入“:w”(保存文件)
    6、输入“:q”(退出)

    这样就把自己加入了sudo组，可以使用sudo命令了。  


