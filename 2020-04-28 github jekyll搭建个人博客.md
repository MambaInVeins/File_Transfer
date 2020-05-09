## github jekyll搭建个人博客



### 第一步 网站托管



一个网站要能够在任何地方都能够被访问，那么需要部署到服务器上。github就提供了这样的功能，只要按照github格式要求，新建一个仓库，把你的网站代码上传到里面，那么就可以在任何时候任何地方都能够访问了，那么如何搭建这个代码托管仓库呢？可参考[官方链接](https://links.jianshu.com/go?to=https%3A%2F%2Fpages.github.com%2F)。



1.首先你要到GitHub上注册一个账号,例如我注册的用户名为：MambaInVeins（用户名可以在设置里改）



2.点击New repository–>输入仓库名称格式为：用户名.github.io(如：MambaInVeins.github.io)->点击Create repository

![image-20200423133451529](https://raw.githubusercontent.com/MambaInVeins/ImageHosting/master/img/20200423133849.png)

3.浏览器里访问https://MambaInVeins.github.io/,可以发现这个url可以被访问了，你可以把改仓库拉取到本地，然后在里面新建一个index.html的文件,在里面输入任意内容，然后再把代码推送到git上，然后再访问改链接，可以发现index.html里面的内容被访问到了。到这里，一个免费且无限流量的github代码托管仓库就创建完成了。



### 第二步 Jekyll安装

windows下的安装步骤：

1. 首先点击下载安装[Ruby installer](https://rubyinstaller.org/downloads/);（参考[博客](https://blog.csdn.net/qq_42451091/article/details/105483983)）

   选择自己需要的版本，不知道的话就选择红色加粗的那个。

   ![image-20200427125506456](https://raw.githubusercontent.com/MambaInVeins/ImageHosting/master/img/20200427125515.png)

   （1）下载完成后双击打开,选择 I accept … 后点击next

   （2）下一步里，三个复选框第一个是把Ruby添加到环境变量，第二个是.rb和.rbw文件和Ruby关联，第三个是将UTF-8作为默认的编码，都选上就行了，安装Install。

   ![](https://raw.githubusercontent.com/MambaInVeins/ImageHosting/master/img/20200427130943.png)

   （3）下一步里，复选框的两个都要选，第二个对于使用C语言拓展是必要的，之后点击next

   ![](https://raw.githubusercontent.com/MambaInVeins/ImageHosting/master/img/20200427130140.png)

   （4）等待安装完成。

   （5）这里的复选框不要选，点击Finish

   ![https://img-blog.csdnimg.cn/20200413121358635.png](https://raw.githubusercontent.com/MambaInVeins/ImageHosting/master/img/20200427130905.png)

   （6）接下来需要设置镜像源，打开你安装Ruby的目录，就是这样

   ![在这里插入图片描述](https://raw.githubusercontent.com/MambaInVeins/ImageHosting/master/img/20200427131128.png)

   （7）然后点击msys64进入，点击etc进入，点击pcman.d进入，现在是这样

   ![在这里插入图片描述](https://raw.githubusercontent.com/MambaInVeins/ImageHosting/master/img/20200427131201.png)

   （8）现在随便找个 文本编辑器打开目录下的三个文件，我建议使用VS Code(可以百度如何安装)，之后学习Ruby也可以用。
   编辑 mirrorlist.mingw32 ，在文件开头添加：
   Server = https://mirrors.tuna.tsinghua.edu.cn/msys2/mingw/i686
   编辑 mirrorlist.mingw64 ，在文件开头添加：
   Server = https://mirrors.tuna.tsinghua.edu.cn/msys2/mingw/x86_64
   编辑 mirrorlist.msys ，在文件开头添加：
   Server = https://mirrors.tuna.tsinghua.edu.cn/msys2/msys/$arch
   操作类似于这样
   ![在这里插入图片描述](https://raw.githubusercontent.com/MambaInVeins/ImageHosting/master/img/20200427131235.png)

   （9）现在我们需要回到上一步路过的msys64目录，打开msys2.exe	

   ![在这里插入图片描述](https://raw.githubusercontent.com/MambaInVeins/ImageHosting/master/img/20200427131316.png)

   （10）打开后它会自动执行一些操作，执行完成后会出现

   ![image-20200427131400392](https://raw.githubusercontent.com/MambaInVeins/ImageHosting/master/img/20200427131627.png)

   这时把msys64.exe关闭，之后再重新打开，现在是这样

   ![在这里插入图片描述](https://raw.githubusercontent.com/MambaInVeins/ImageHosting/master/img/20200427131444.png)

   输入 `pacman -Sy` 后回车，等待结束关闭即可

   ![在这里插入图片描述](https://raw.githubusercontent.com/MambaInVeins/ImageHosting/master/img/20200427131622.png)

   （11）现在，进入windows开始菜单(就是左下角的windows图标)，在里面字母R下面找到Ruby下面的命令行，具体看图，找到后点击打开

   ![在这里插入图片描述](https://raw.githubusercontent.com/MambaInVeins/ImageHosting/master/img/20200427131658.png)

   输入 `ridk install 3` 点击回车，之后就是等待操作完成(不要关闭程序还要用)。

   ![在这里插入图片描述](https://raw.githubusercontent.com/MambaInVeins/ImageHosting/master/img/20200427131819.png)

   完成后的样子

   ![在这里插入图片描述](https://raw.githubusercontent.com/MambaInVeins/ImageHosting/master/img/20200427131825.png)

   （12）现在输入：
    `gem sources --remove https://rubygems.org/` 回车
    `gem sources --add https://mirrors.tuna.tsinghua.edu.cn/rubygems/` 回车

   （13）现在所有安装都完成了，关闭命令行，可以开始使用Ruby。

2. 点击下载[RubyGems](https://rubygems.org/pages/download),下载完成后解压至你想放的位置。 打开命令行执行：

   ```
   cd D:\rubygems-2.7.4 //进入到解压包的位置
   ruby setup.rb
   ```

3. 在命令行执行

   ```
   gem install jekyll
   ```

4. 安装完成，我们可以用jekyll命令创建一个博客模板,打开命令行执行：

   ```
   cd d:
   jekyll new testblog
   cd testblog
   jekyll server
   ```

   在浏览器输入http://127.0.0.1:4000/即可浏览刚刚创建的blog,到此jekyll 就安装完成了。
   
   

### 第三步 Jekyll 主题选择

上一步我们完成了jekyll的安装，默认创建的博客模板一般比较简单，jekyll官网提供了大量博客模板，我们可以去挑选一个自己喜欢的博客模板，然后在这个博客基础上修改到满足自己需求的博客

点击前往[jekyll 主题官网](http://jekyllthemes.org/)

我选择的[adam-blog](http://jekyllthemes.org/themes/adam-blog/)这篇主题。点击Homepage可以链接到该blog Github页面，点击download可以下载该博客源码，点击demo可以预览该博客效果 

![img](https://raw.githubusercontent.com/MambaInVeins/ImageHosting/master/img/20200428131520)

我们点击download，将该源码下载下来，命令行进入该目录执行jekyll server，执行成功可以在控制台看到运行路径： 

```
Server address: http://127.0.0.1:4000/adam-blog/
```



若下载的主题jekyll server执行失败，出现如下几类错误

（1）执行jekyll server命令后可能会出现如下错误

```
    D:/Ruby23-x64/lib/ruby/2.3.0/rubygems/core_ext/kernel_require.rb:55:in `require': cannot load such file -- bundler (LoadError)
        from D:/Ruby23-x64/lib/ruby/2.3.0/rubygems/core_ext/kernel_require.rb:55:in `require'
        from D:/Ruby23-x64/lib/ruby/gems/2.3.0/gems/jekyll-3.3.1/lib/jekyll/plugin_manager.rb:34:in `require_from_bundler'
        from D:/Ruby23-x64/lib/ruby/gems/2.3.0/gems/jekyll-3.3.1/exe/jekyll:9:in `<top (required)>'
        from D:/Ruby23-x64/bin/jekyll:22:in `load'
        from D:/Ruby23-x64/bin/jekyll:22:in `<main>'
```

解决：执行以下命令

```
gem install bundler
```

（2）执行jekyll server命令后可能会出现如下错误

```
D:/Ruby23-x64/lib/ruby/gems/2.3.0/gems/bundler-1.14.3/lib/bundler/spec_set.rb:87:in `block in materialize: Could not find i18n-0.7.0 in any of the sources (Bundler::GemNotFound)



...
```

​	解决：执行以下命令

```
bundle install
```

（3）执行jekyll server命令后可能会出现如下错误

```
D:/Ruby23-x64/lib/ruby/gems/2.3.0/gems/bundler-1.14.0/lib/bundler/resolver.rb:376:in `block in verify_gemfile_dependencies_are_found!': Could not find gem 'jekyll (~> 3.2.1) x64-mingw32' in any of the gem sources listed in your Gemfile. (Bundler::GemNotFound)



    ......
```

解决：查看Gemfile文件里的jekyll版本是否与安装的版本一致，若不一致，修改为此时安装的版本

（4）执行jekyll server命令后可能会出现如下类似错误

```
D:/Ruby23-x64/lib/ruby/gems/2.3.0/gems/bundler-1.14.0/lib/bundler/resolver.rb:376:in `block in verify_gemfile_dependencies_are_found!': Could not find gem 'jekyll-sitemap x64-mingw32' in any of the gem sources listed in your Gemfile. (Bundler::GemNotFound)
```

解决：执行以下命令

```
gem install jekyll-sitemap
```



若还不成功，则根据控制台提示的错误，可以百度到解决方案。 到此，我们已经选定了一个博客主题模板，接下来我们讲解下jekyll主题的目录结构。



### 第四步 Jekyll目录结构



