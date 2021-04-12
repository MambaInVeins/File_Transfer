# HTTP Basic auth认证

## Basic 概述

Basic认证是HTTP中非常简单的认证方式，因为简单，所以不是很安全，不过仍然非常常用。

当一个客户端向一个需要认证的HTTP服务器进行数据请求时，如果之前没有认证过，HTTP服务器会返回401状态码，要求客户端输入用户名和密码。用户输入用户名和密码后，用户名和密码会经过BASE64加密附加到请求信息中再次请求HTTP服务器，HTTP服务器会根据请求头携带的认证信息，决定是否认证成功及做出相应的响应。

## 使用Tomcat进行Basic认证

如果熟悉Tomcat的朋友，肯定知道Tomcat自带的有个manager项目，访问这个项目需要Basic认证。

下面我们来给我们自己的项目加Basic认证。

配置项目的 web.xml

示例：

    <?xml version="1.0" encoding="UTF-8"?>
    <web-app xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://java.sun.com/xml/ns/javaee" 
    　　xmlns:web="http://java.sun.com/xml/ns/javaee/web-app_2_5.xsd" 
    　　xsi:schemaLocation="http://java.sun.com/xml/ns/javaee http://java.sun.com/xml/ns/javaee/web-app_3_0.xsd" id="WebApp_ID" version="3.0">
    <display-name>lvyou</display-name>
    <servlet>
        <servlet-name>home</servlet-name>
        <servlet-class>com.coder4j.web.servlet.HomeServlet</servlet-class>
    </servlet>
    <servlet-mapping>
        <servlet-name>home</servlet-name>
        <url-pattern>/home.do</url-pattern>
    </servlet-mapping>

        <!-- 下面是Basic认证配置 -->
        <security-constraint>
            <web-resource-collection>
                <web-resource-name>GuiLin</web-resource-name>
                <url-pattern>/*</url-pattern>
            </web-resource-collection>

            <auth-constraint>
                <role-name>lvyou</role-name>
            </auth-constraint>
        </security-constraint>

        <login-config>
            <auth-method>BASIC</auth-method>
            <realm-name>guilin photos</realm-name>
        </login-config>
        <!-- Basic认证配置结束 -->


    <welcome-file-list>
        <welcome-file>index.html</welcome-file>
        <welcome-file>index.jsp</welcome-file>
    </welcome-file-list>
    </web-app>

对上面加注释的部分进行简单的解释：

    web-resource-name : 给这个认证起个名字

    url-pattern : 哪些地址需要认证，/*表示此项目的任意地址都需要认证，/lvyou/*表示/lvyou下的任意地址都需要认证。

    role-name : 哪些角色的用户认证后可以访问此资源（光认证还不够哟，必须得是许可的角色哟），我这里规定必须是lvyou这个角色的用户才能看我的照片。

    auth-method : 认证方式为BASIC认证。

    realm-name : 给出的认证提示。

修改 tomcat-users.xml

tomcat 提供了用户配置文件，我们直接使用就行了。

    <?xml version='1.0' encoding='utf-8'?>
    <tomcat-users>
    <role rolename="lvyou"/>
    <user username="tom" password="tomcat" roles="lvyou"/>
    </tomcat-users>

至此，两步就完成了Basic 认证，如果想访问我的照片，就需要输入tom 和 tomcat才行。


## Basic 认证的过程

Basic认证的流程很简单，现概述如下：

1, 客户端向服务器请求数据，并且请求的数据是需要认证才能看的，并且客户端目前没有认证过。

2, 访问的页面需要认证，客户端弹出认证窗口。

认证窗口关闭之前，浏览器状态一直是：pending等待用户输入。

点击 x 或取消，将会出现401状态码，响应内容如下：

![](https://image-static.segmentfault.com/782/440/782440550-58e8660c86082_fix732)

响应头中有一句话：

    WWW-Authorization: Basic realm="guilin photos"

表示需要认证，提示信息为：guilin photos

3, 刷新页面，输入正确的用户名和密码，将会进入到我们的项目中

输入用户名和密码的请求信息头如下：

![](https://image-static.segmentfault.com/356/688/3566880750-57393b338b1ee_fix732)

这是我们的认证信息。

加密策略如下：

    用户名和密码用:合并，将合并后的字符串使用BASE64加密为密文，每次请求时，将密文附于请求头中，服务器接收此密文，进行解析，判断是否认证

## Java 实现

我们知道了流程，当然可以用代码来实现。

核心代码：

    HttpSession session = request.getSession();
    String user = (String) session.getAttribute("user");
    String pass;
    if (user == null) {
        try {
            response.setCharacterEncoding("utf-8");
            PrintWriter out = response.getWriter();
            String authorization = request.getHeader("Authorization");
            if (authorization == null || authorization.equals("")) {
                response.setStatus(401);
                response.setHeader("WWW-Authenticate", "Basic realm=\"input username and password\"");
                out.print("401 认证失败");
                return;
            }
            String userAndPass = new String(new BASE64Decoder().decodeBuffer(authorization.split(" ")[1]));
            if (userAndPass.split(":").length < 2) {
                response.setStatus(401);
                response.setHeader("WWW-Authenticate", "Basic realm=\"input username and password\"");
                out.print("401 认证失败");
                return;
            }
            user = userAndPass.split(":")[0];
            pass = userAndPass.split(":")[1];
            if (user.equals("111") && pass.equals("111")) {
                session.setAttribute("user", user);
                // 跳转合适的地方
            } else {
                response.setStatus(401);
                response.setHeader("WWW-Authenticate", "Basic realm=\"input username and password\"");
                out.print("401 认证失败");
                return;
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    } else {
        // 跳转合适的地方
    }

Basic认证的核心就是响应401状态码，告知浏览器需要用户输入用户名和密码，然后就是后台按照Basic加密的方式进行解密验证即可。

## 缺点

HTTP基本认证的目标是提供简单的用户验证功能，其认证过程简单明了，适合于对安全性要求不高的系统或设备中，如大家所用路由器的配置页面的认证，几乎都采取了这种方式。其缺点是没有灵活可靠的认证策略，另外，BASE64的加密强度非常低，直接能在请求头中看到，几乎相当于明文了。

## 实例：弱口令穷举攻击

某VPN admin console 中 Authorization 是采用 basic auth 授权方式验证客户端请求，Authorization 请求头对应的值是 (basic base64编码) 忽略括号，其中 base64编码是将 用户名:密码 这种格式进行处理生成的。可利用口令爆破的方式，对其管理员口令进行破解。

弱口令集合

    https://github.com/legik/fast-detects/blob/master/weak-basic-auth.yaml