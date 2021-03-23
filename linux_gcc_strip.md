linux gcc strip命令简介

strip简介

    strip经常用来去除目标文件中的一些符号表、调试符号表信息，以减小静态库、动态库和程序的大小。

    strip支持的选项可通过如下命令查看：strip --help

Linux strip命令的用法

    https://www.linuxidc.com/Linux/2011-05/35773.htm

程序开发是否要strip

    strip可以压缩目标文件、静态库、动态库、可执行程序的大小，但是会失去符号表、调试符号表信息。为了方便定位问题（比如定位 core dump问题）， 建议， 尽量不要strip, 除非存储紧张。

    在实际的开发中， 若需要对动态库.so进行strip操作， 减少占地空间。 通常的做法是： strip前的库用来调试， strip后的库用来实际发布， 他们两者有对应关系。 一旦发布的strip后的库出了问题， 就可以找对应的未strip的库来定位。
    
静态库如何strip

    https://www.cnblogs.com/welhzh/p/4858695.html