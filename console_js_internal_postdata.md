浏览器控制台循环发送数据包

利用js定时器实现，发包部分在 Network - use as fetch in console


    var t1 = self.setInterval(clock,1000);
    async function clock()
    {
    await fetch("https://www.baidu.com/img/flexible/logo/pc/result.png", {
        "credentials": "include",
        "headers": {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0",
            "Accept": "image/webp,*/*",
            "Accept-Language": "en-US,en;q=0.5",
            "If-Modified-Since": "Sat, 09 May 2020 09:33:56 GMT",
            "If-None-Match": "\"19d9-5a533d00d4900\"",
            "Cache-Control": "max-age=0"
        },
        "referrer": "https://www.baidu.com/",
        "method": "GET",
        "mode": "cors"
    });
    }
    self.clearInterval(t1);


循环定时器

    timename=setInterval("function();",delaytime);

    第一个参数"function()"是定时器触发时要执行的动作，可以是一个函数，也可以是几个函数，函数间用";"隔开即可。比如要弹出两个警告窗口，便可将"function();"换成"alert('第一个警告窗口!');alert('第二个警告窗口!');"；而第二个参数“delaytime”则是间隔的时间，以毫秒为单位，即填写“5000”，就表示5秒钟。

采坑记录

    报 "SyntaxError: await is only valid in async function"

    await 关键字必须用在async函数主体中,不能直接用在脚本函数之外.

    同时也意味着, 只有 function 中有异步操作, 才要在 function 前面定义 async 关键字.

    async function Demo() 