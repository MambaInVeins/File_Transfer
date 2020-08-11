linux 系统中 /etc/passwd 和 /etc/shadow文件详解

在linux操作系统中， /etc/passwd文件中的每个用户都有一个对应的记录行,记录着这个用户的一下基本属性。该文件对所有用户可读。

而/etc/shadow文件正如他的名字一样，他是passwd文件的一个影子，/etc/shadow文件中的记录行与/etc/passwd中的一一对应，它由pwconv命令根据/etc/passwd中的数据自动产生。但是/etc/shadow文件只有系统管理员才能够进行修改和查看。

## /etc/passwd文件介绍

首先，我们通过命令行cat /etc/passwd进行查看/etc/passwd文件内容：

    root:x:0:0:root:/root:/bin/bash
    daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
    bin:x:2:2:bin:/bin:/usr/sbin/nologin
    sys:x:3:3:sys:/dev:/usr/sbin/nologin
    sync:x:4:65534:sync:/bin:/bin/sync
    games:x:5:60:games:/usr/games:/usr/sbin/nologin
    man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
    lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
    mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
    news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
    uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
    proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
    www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
    backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
    list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
    irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
    gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
    nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
    libuuid:x:100:101::/var/lib/libuuid:
    syslog:x:101:104::/home/syslog:/bin/false
    messagebus:x:102:106::/var/run/dbus:/bin/false
    usbmux:x:103:46:usbmux daemon,,,:/home/usbmux:/bin/false
    dnsmasq:x:104:65534:dnsmasq,,,:/var/lib/misc:/bin/false
    avahi-autoipd:x:105:113:Avahi autoip daemon,,,:/var/lib/avahi-autoipd:/bin/false
    kernoops:x:106:65534:Kernel Oops Tracking Daemon,,,:/:/bin/false
    rtkit:x:107:114:RealtimeKit,,,:/proc:/bin/false
    saned:x:108:115::/home/saned:/bin/false
    whoopsie:x:109:116::/nonexistent:/bin/false
    speech-dispatcher:x:110:29:Speech Dispatcher,,,:/var/run/speech-dispatcher:/bin/sh
    avahi:x:111:117:Avahi mDNS daemon,,,:/var/run/avahi-daemon:/bin/false
    lightdm:x:112:118:Light Display Manager:/var/lib/lightdm:/bin/false
    colord:x:113:121:colord colour management daemon,,,:/var/lib/colord:/bin/false
    hplip:x:114:7:HPLIP system user,,,:/var/run/hplip:/bin/false
    pulse:x:115:122:PulseAudio daemon,,,:/var/run/pulse:/bin/false
    yaofei:x:1000:1000:ubuntu14.04,,,:/home/yaofei:/bin/bash
    sshd:x:116:65534::/var/run/sshd:/usr/sbin/nologin
    mysql:x:117:125:MySQL Server,,,:/nonexistent:/bin/false

从文件中我们可以看到，/etc/passwd中一行记录对应着一个用户，每行记录又被冒号(:)分隔为7个字段，其格式和具体含义如下：
用户名:口令:用户标识号:组标识号:注释性描述:主目录:登录Shell

    用户名(login_name):是代表用户账号的字符串。通常长度不超过8个字符，并且由大小写字母和/或数字组成。登录名中不能有冒号(:)，因为冒号在这里是分隔符。为了兼容起见，登录名中最好不要包含点字符(.)，并且不使用连字符(-)和加号(+)打头。

    口令(passwd):一些系统中，存放着加密后的用户口令字。虽然这个字段存放的只是用户口令的加密串，不是明文，但是由于/etc/passwd文件对所有用户都可读，所以这仍是一个安全隐患。因此，现在许多Linux系统（如SVR4）都使用了shadow技术，把真正的加密后的用户口令字存放到/etc/shadow文件中，而在/etc/passwd文件的口令字段中只存放一个特殊的字符，例如“x”或者“*”。

    用户标识号(UID):是一个整数，系统内部用它来标识用户。一般情况下它与用户名是一一对应的。如果几个用户名对应的用户标识号是一样的，系统内部将把它们视为同一个用户，但是它们可以有不同的口令、不同的主目录以及不同的登录Shell等。取值范围是0-65535。0是超级用户root的标识号，1-99由系统保留，作为管理账号，普通用户的标识号从100开始。在Linux系统中，这个界限是500。

    组标识号(GID):字段记录的是用户所属的用户组。它对应着/etc/group文件中的一条记录。

    注释性描述(users):字段记录着用户的一些个人情况，例如用户的真实姓名、电话、地址等，这个字段并没有什么实际的用途。在不同的Linux系统中，这个字段的格式并没有统一。在许多Linux系统中，这个字段存放的是一段任意的注释性描述文字，用做finger命令的输出。

    主目录(home_directory):也就是用户的起始工作目录，它是用户在登录到系统之后所处的目录。在大多数系统中，各用户的主目录都被组织在同一个特定的目录下，而用户主目录的名称就是该用户的登录名。各用户对自己的主目录有读、写、执行（搜索）权限，其他用户对此目录的访问权限则根据具体情况设置。

    登录Shell(Shell):用户登录后，要启动一个进程，负责将用户的操作传给内核，这个进程是用户登录到系统后运行的命令解释器或某个特定的程序，即Shell。Shell是用户与Linux系统之间的接口。Linux的Shell有许多种，每种都有不同的特点。常用的有sh(BourneShell),csh(CShell),ksh(KornShell),tcsh(TENEX/TOPS-20typeCShell),bash(BourneAgainShell)等。系统管理员可以根据系统情况和用户习惯为用户指定某个Shell。如果不指定Shell，那么系统使用sh为默认的登录Shell，即这个字段的值为/bin/sh。

## /etc/shadow文件介绍

/etc/shadow文件格式与/etc/passwd文件格式类似，同样由若干个字段组成，字段之间用“:”隔开。

通过命令行输入sudo cat /etc/shadow进行文件内容查看：

    root:!:17043:0:99999:7:::
    daemon:*:16652:0:99999:7:::
    bin:*:16652:0:99999:7:::
    sys:*:16652:0:99999:7:::
    sync:*:16652:0:99999:7:::
    games:*:16652:0:99999:7:::
    man:*:16652:0:99999:7:::
    lp:*:16652:0:99999:7:::
    mail:*:16652:0:99999:7:::
    news:*:16652:0:99999:7:::
    uucp:*:16652:0:99999:7:::
    proxy:*:16652:0:99999:7:::
    www-data:*:16652:root:!:17043:0:99999:7:::
    daemon:*:16652:0:99999:7:::
    bin:*:16652:0:99999:7:::
    sys:*:16652:0:99999:7:::
    sync:*:16652:0:99999:7:::
    games:*:16652:0:99999:7:::
    man:*:16652:0:99999:7:::
    lp:*:16652:0:99999:7::99:7:::
    gnats:*:16652:0:99999:7:::
    nobody:*:16652:0:99999:7:::
    libuuid:!:16652:0:99999:7:::
    syslog:*:16652:0:99999:7:::
    messagebus:*:16652:0:99999:7:::
    usbmux:*:16652:0:99999:7:::
    dnsmasq:*:16652:0:99999:7:::
    avahi-autoipd:*:16652:0:99999:7:::
    kernoops:*:16652:0:99999:7:::
    rtkit:*:16652:0:99999:7:::
    saned:*:16652:0:99999:7:::
    whoopsie:*:16652:0:99999:7:::
    speech-dispatcher:!:16652:0:99999:7:::
    avahi:*:16652:0:99999:7:::
    lightdm:*:16652:0:99999:7:::
    colord:*:16652:0:99999:7:::
    hplip:*:16652:0:99999:7:::
    pulse:*:16652:0:99999:7:::
    yaofei:$1$5M0Rbozg$1fWsJaQB.TFAL24b96xi41:17043:0:99999:7:::
    sshd:*:17043:0:99999:7:::
    mysql:!:17048:0:99999:7:::


文件中字段主要含义为：登录名:加密口令:最后一次修改时间:最小时间间隔:最大时间间隔:警告时间:不活动时间:失效时间:标志

    “登录名”是与/etc/passwd文件中的登录名相一致的用户账号

    “口令”字段存放的是加密后的用户口令字：

        如果为空，则对应用户没有口令，登录时不需要口令；
        星号代表帐号被锁定；
        双叹号表示这个密码已经过期了；
        $6$开头的，表明是用SHA-512加密；
        $1$表明是用MD5加密；
        $2$ 是用Blowfish加密；
        $5$ 是用 SHA-256加密；

    “最后一次修改时间”表示的是从某个时刻起，到用户最后一次修改口令时的天数。时间起点对不同的系统可能不一样。例如在SCOLinux中，这个时间起点是1970年1月1日。

    “最小时间间隔”指的是两次修改口令之间所需的最小天数。

    “最大时间间隔”指的是口令保持有效的最大天数。

    “警告时间”字段表示的是从系统开始警告用户到用户密码正式失效之间的天数。

    “不活动时间”表示的是用户没有登录活动但账号仍能保持有效的最大天数。
    
    “失效时间”字段给出的是一个绝对的天数，如果使用了这个字段，那么就给出相应账号的生存期。期满后，该账号就不再是一个合法的账号，也就不能再用来登录了。
