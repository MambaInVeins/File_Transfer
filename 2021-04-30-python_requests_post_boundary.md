
1.什么是Multipart/form-data？
Multipart/form-data是上传文件的一种方式。

Multipart/form-data其实就是浏览器用表单上传文件的方式。最常见的情境是：在写邮件时，向邮件后添加附件，附件通常使用表单添加，也就是用multipart/form-data格式上传到服务器。

enctype属性:
enctype：规定了form表单在发送到服务器时候编码方式，它有如下的三个值。
①application/x-www-form-urlencoded：默认的编码方式。但是在用文本的传输和MP3等大型文件的时候，使用这种编码就显得 效率低下。
②multipart/form-data：指定传输数据为二进制类型，比如图片、mp3、文件。
③text/plain：纯文体的传输。空格转换为 “+” 加号，但不对特殊字符编码。

2.multipart/form-data请求请求体的格式(以某网站模拟登录为例)

![](https://upload-images.jianshu.io/upload_images/11227136-81b32e28c183b97f.png?imageMogr2/auto-orient/strip|imageView2/2/w/1200)

3. 实现请求体的拼接

3.1 第一种：使用 requests库

    # coding: utf-8
    from collections import OrderedDict
    import requests

    # 构建有序字典
    params = OrderedDict([("username", (None, '130533193203240022')),
                    ("password", (None, 'qwerqwer')),
                    ('captchaId', (None, 'img_captcha_7d96b3cd-f873-4c36-8986-584952e38f20')),
                    ('captchaWord', (None, 'rdh5')),
                    ('_csrf', (None, '200ea95d-90e9-4789-9e0b-435a6dd8b57b'))])

    res = requests.get('http://www.baidu.com', files=params)
    print res.request.body

    # 打印的结果：
    --6c7a1966e0294e1cb89b06b95cf3da84
    Content-Disposition: form-data; name="username"

    130533193203240022
    --6c7a1966e0294e1cb89b06b95cf3da84
    Content-Disposition: form-data; name="password"

    qwerqwer
    --6c7a1966e0294e1cb89b06b95cf3da84
    Content-Disposition: form-data; name="captchaId"

    img_captcha_7d96b3cd-f873-4c36-8986-584952e38f20
    --6c7a1966e0294e1cb89b06b95cf3da84
    Content-Disposition: form-data; name="captchaWord"

    rdh5
    --6c7a1966e0294e1cb89b06b95cf3da84
    Content-Disposition: form-data; name="_csrf"

    200ea95d-90e9-4789-9e0b-435a6dd8b57b
    --6c7a1966e0294e1cb89b06b95cf3da84--

    需要注意的是， 可以发现分隔符是随机生成的， 跟制定的不太一样， 这需要我们自己手动替换  
    # 替换使用的re
    temp = re.search(r'--(.*)--', res.request.body).group(1)                          
    data = re.sub(temp, '----WebKitFormBoundaryKPjN0GYtWEjAni5F', res.request.body)   

    注：这种方法可以构建想要的请求体， 麻烦的是分隔符并不是制定的那样，而是默认的 uuid4().hex   需要手动替换。 files可以接收的参数， 
        源码中解释截图在文末。

3.2 第二种：使用 encode_multipart_formdata函数

    # coding: utf-8
    from collections import OrderedDict
    from urllib3 import encode_multipart_formdata

    params = OrderedDict([("username", (None, '130533193203240022', 'multipart/form-data')),
                    ("password", (None, 'qwerqwer', 'multipart/form-data')),
                    ('captchaId', (None, 'img_captcha_7d96b3cd-f873-4c36-8986-584952e38f20', 'multipart/form-data')),
                    ('captchaWord', (None, 'rdh5', 'multipart/form-data')),
                    ('_csrf', (None, '200ea95d-90e9-4789-9e0b-435a6dd8b57b','multipart/form-data'))])
    m = encode_multipart_formdata(params, boundary='----WebKitFormBoundaryKPjN0GYtWEjAni5F')
    print m[0]

    # 打印结果
    ------WebKitFormBoundaryKPjN0GYtWEjAni5F
    Content-Disposition: form-data; name="username"
    Content-Type: multipart/form-data

    130533193203240022
    ------WebKitFormBoundaryKPjN0GYtWEjAni5F
    Content-Disposition: form-data; name="password"
    Content-Type: multipart/form-data

    qwerqwer
    ------WebKitFormBoundaryKPjN0GYtWEjAni5F
    Content-Disposition: form-data; name="captchaId"
    Content-Type: multipart/form-data

    img_captcha_7d96b3cd-f873-4c36-8986-584952e38f20
    ------WebKitFormBoundaryKPjN0GYtWEjAni5F
    Content-Disposition: form-data; name="captchaWord"
    Content-Type: multipart/form-data

    rdh5
    ------WebKitFormBoundaryKPjN0GYtWEjAni5F
    Content-Disposition: form-data; name="_csrf"
    Content-Type: multipart/form-data

    200ea95d-90e9-4789-9e0b-435a6dd8b57b
    ------WebKitFormBoundaryKPjN0GYtWEjAni5F--

    可以看得到， 这种方法多出来一个 Content-Type（我传递的参数中指定了这个值，
    如果没有指定，这个Content-Type依然存在，值为：application/octet-stream），
    我现在也没有太确定多的这个值对最后的结果有没有影响。还没试...[手动捂脸]


参考链接：

https://www.jianshu.com/p/0023bb7afddb

https://blog.csdn.net/Enderman_xiaohei/article/details/89421773