# 使用powershell 管理windows 2016服务器

    大家知道，在管理linux服务器上，我们基本上通过ssh和bash这两个工具，就可以很好的管理一台服务器。
但是在windows服务器上，大部分人都是使用远程桌面，远程登录上去，通过windows的图形界面进行操作，
这种方式虽然简单，容易入门，但是它的另一个后果就是不方便自动化。想象一下，你要部署一个应用服务，
每次都要手工打包，手工拷贝上传到服务器，然后通过远程桌面，上去启动服务，这个过程都是手工链接的，
没有自动化。效率和linux比起来是天差地别。虽然windows也可以写bat脚本，但是bat文件的语法，极其
丑陋，操作极其不方便，有写过的都肯定有深切体会，另外功能也远远比不上bash，所以在自动化部署方面，windows是远远落后于linux的。
   但是powershell出现后，这一切大大改观了，可以说，powershell功能甚至比linux bash还强大，同时
powershell支持linux系统，也可以在linux上使用。感兴趣的可以看 (https://docs.microsoft.com/en-us/powershell/scripting/install/installing-powershell-core-on-linux?view=powershell-7)

## winrm 简介
   winrm 是windows remote management 的简称。它相当于linux上面的sshd服务器，可以提供对windows服务器进行远程管理的接口。为了通过powershell
远程登录服务器，我们需要在服务器上启动winrm服务。

## 使用powershell，服务器端配置
* 启动winrm 服务
  先以管理员身份启动一个powershell窗口  
  使用如下命令启动winrm服务
  `start-service winrm`    
  配置winrm服务  
  `winrm quickconfig`
## 使用powershell，客户端配置
   以管理员身份打开一个powershell窗口
   开启winrm服务  
   `start-service winrm`  
   把服务器的地址设置为受信任的主机  
   `set-item wsman:\localhost\Client\TrustedHosts -value "192.168.0.31,192.168.0.32"`    
   把远程计算机加入受信任列表，可以有通配符,这一步很重要

## 使用powershell远程登录
   经过以上配置，我们就可以通过powershell远程登录到服务器了
   在powershell窗口里，输入如下命令  
   `enter-pssession -computerName 192.168.0.31 -credential administrator `
   系统会弹出登录对话框，输入密码即可
## 使用powershell 拷贝文件
   

   `
      $remote = New-PSSession -computerName 192.168.0.100  # 建立一个到远程的连接
      Copy-Item my.ps1  -Destination d:\server -ToSession $remote  # 拷贝文件到远程
   `
## powershell 脚本编程基础
   * 命令返回值  
     通过变量 $? 获取前一个命令的返回值，命令成功返回值为$True,否则为 $False
   * 比较操作符
     `$1 -ne $2 ` 判断两个变量是否不等
     `$1 -eq $2 ` 判断两个变量是否相等
     `$1 -lt $2`  小于比较  
     `$1 -gt $2`  大于比较
     条件判断语句  
     `
            if($1 -ne $2){  
                # 执行不等操作  
            }else{  
                # 否则执行相等操作  
            }   
     `
## 一个例子，使用powershell脚本部署代码
  * 登录，拷贝，启动
  `
  #设置用户名密码
  $defaultCredential = New-Object Management.Automation.PSCredential "username", (ConvertTo-SecureString 'password' -AsPlainText -Force)
 
  $PSDefaultParameterValues = @{
	  "Enter-PSSession:Credential" = $defaultCredential;
	  "Invoke-Command:Credential" = $defaultCredential;
    "New-PSSession:Credential" = $defaultCredential;
}
  #打开到服务端的连接
  $remote = New-PSSession -computerName 192.168.0.100
  if($? -ne $True){
     write-host "connect to host failed."
     exit 1
  }
  #拷贝脚本到服务端
  Copy-Item my.ps1  -Destination d:\server -ToSession $remote
  #启动服务端的脚本
  Invoke-Command -Session $remote -ScriptBlock {d:\server\my.ps1}
  
  `
  
