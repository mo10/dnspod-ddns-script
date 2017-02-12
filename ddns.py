# -*- coding:utf-8 -*-
#import urllib,urllib2,json,sys,ssl
import sys,json,requests
#reload(sys)
#sys.setdefaultencoding("utf-8")

###设置######################Config###
#从服务器获取本地外网IP地址
ip_api_url = "https://api.ipify.org"
#服务器超时时间
request_timeout=10
#你的Dnspod Token
#token = "123456,1234567890abcef1234567890abcdef"#例子
token = "Token ID,Token"
#域名
#domain="google.com"#例子
domain="Your.domain.com"
#记录
#record = "www"#例子
#record = "@"#例子
record = "@"
###设置######################Config###
class DnspodError(Exception):
    def __init__(self, status, msg):
        Exception.__init__(self)
        self.status = status
        self.msg = msg
try:
    #读取Dnspod记录
    payload = {
        'login_token':token,
        'domain':domain,
        'sub_domain':record,
        'format':'json'
        }
    record_info = requests.post("https://dnsapi.cn/Record.List",data=payload,timeout=request_timeout).json()
    #判断状态码
    if (record_info['status']['code']!='1'):
        #读取记录异常
        raise DnspodError(record_info['status']['code'],record_info['status']['message'])
    #遍历记录列表 查找A记录
    for i in record_info['records']:
        if(i['type'] == 'A'):
            #获取本机IP
            local_ip=requests.get(ip_api_url, timeout=request_timeout).text
            print("domain id:%s,record id:%s,record ip:%s,local ip:%s"%(record_info['domain']['id'],i['id'],i['value'],local_ip))
            #对比本机IP与记录中的IP 没区别就不需要更新记录
            if(i['value'] == local_ip):
                print("然而IP并没有变化")
                sys.exit(0)
            #更新记录
            payload = {
                'login_token':token,
                'domain_id':record_info['domain']['id'],
                'record_id':i['id'],
                'record_type':i['type'],
                'record_line_id':i['line_id'],
                'sub_domain':record,
                'value':local_ip,
                'format':'json'
                }
            record_modify = requests.post("https://dnsapi.cn/Record.Modify",data=payload,timeout=request_timeout).json()
            #判断状态码
            if (record_modify['status']['code']!='1'):
                #修改记录异常
                raise DnspodError(record_modify['status']['code'],record_modify['status']['message'])
            print("记录IP更新完了")
except requests.exceptions.Timeout as e:
    print("%s连接超时!"%(e.request.url))
    exit(1)
except DnspodError as e:
    print("Dnspod错误:%s,%s"%(e.status,e.msg))
    exit(1)
