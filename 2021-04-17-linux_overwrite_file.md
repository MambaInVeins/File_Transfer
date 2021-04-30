清空json文件并写入内容

    tee hello.json >/dev/null <<EOF
    {
    "hello": "world"
    }
    EOF

清空文件

    echo > xxx
    cat /dev/null> xxx
    truncate -s 0 xxx
    > xxx