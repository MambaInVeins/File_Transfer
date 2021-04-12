# 将shell的输出重定向/存储到GDB变量中

我想知道如何在GDB中了解当前的系统架构，并将此信息存储在一个变量中供以后评估。

就像是：

    set variable $x=`shell uname -m`

theres 2种方式：

旧的方式：

    (gdb) shell echo set \$x=\"$(uname -m)\" >/tmp/foo.gdb
    (gdb) source /tmp/foo.gdb

python更新：

    (gdb) python gdb.execute("set $y=\"" + os.uname()[4] + "\"")

