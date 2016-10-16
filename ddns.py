# -*- coding:utf-8 -*-
import urllib,urllib2,json,sys,ssl
reload(sys)
sys.setdefaultencoding("utf-8")
ssl._create_default_https_context = ssl._create_unverified_context

###设置######################Config###
#从服务器获取本地外网IP地址
url = "http://your.server.here/ip.php"
#设置Dnspod账户
mytoken = "API Token ID,Token"
#域名ID
domain_id = "your domain id here"
#记录ID
record_id = "your record id here"
###设置######################Config###

def getip():
	req = urllib2.Request(url)
	res_data = urllib2.urlopen(req)
	return res_data.read()

def dnspodapi(requrl,postdata):
	data_urlencode = urllib.urlencode(postdata)
	req = urllib2.Request(url = requrl,data =data_urlencode)
	res_data = urllib2.urlopen(req)
	return json.loads(res_data.read())

#获取本机外网IP
localip=getip()
#获取记录IP
data = {
	'login_token':mytoken,
	'domain_id':domain_id,
	'record_id':record_id,
	'format':'json'}
code=dnspodapi("https://dnsapi.cn/Record.Info",data)
#判断返回状态是否正常
if (code['status']['code']!='1'):
	print "Error:"+code['status']['code']
	print code['status']['message']
	exit(1)

print "local_ip:	"+localip
print "record_ip:	"+code['record']['value']

#检查本地IP是否与记录IP不同
if (code['record']['value']!=localip):
	data = {
                'login_token':mytoken,
                'domain_id':domain_id,
                'record_id':record_id,
                'record_type':code['record']['record_type'],
                'record_line':code['record']['record_line'],
                'sub_domain':code['record']['sub_domain'],
                'value':localip,
                'format':'json'
                }
	code= dnspodapi("https://dnsapi.cn/Record.Modify",data)
	#判断返回状态是否正常
	if (code['status']['code']!='1'):
		print "Error:"+code['status']['code']
		print code['status']['message']
		exit(1)
	print "record ip was updated to"+code['record']['value']
	exit(0)
else:
	print "record ip is the latest!"
	exit(0)

