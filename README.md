# dnspod-ddns-script

##获取Token


  登陆Dnspod后台,依次点击 用户中心 -> 安全设定 -> API Token

  添加一个Token 记下ID和Token

  打开ddns.py token变量填写ID与Token 格式为:
  
      id,token 

 例子:
 
      123456,1234567890abcef1234567890abcdef


  已不需要填写域名ID和记录ID,自动获取

##添加定时任务

    crontab -e
    */5 * * * * python /path/to/ddns.py &
