# dnspod-ddns-script

##配置方法

  登陆Dnspod后台页面,打开 用户中心 -> 安全设定 -> API Token
  添加一个Token 记下ID和Token
  打开ddns.py mytoken变量填写ID和Token 格式为:
  
      id,token 
      
   例
   
      1234,fbcd1234bfbd34fd
      
   域名ID和记录ID获取请见 https://github.com/mo10/get-my-dnspod-id
 
##添加定时任务

    crontab -e
    */5 * * * * python /path/to/dnspod.py &
