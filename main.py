#author: linzhang 2015 qq:9166794
import requests
import hashlib
from urllib.parse import quote,unquote
from bs4 import BeautifulSoup
headers = {'Referer': 'http://jwweb.fzfu.com/_data/login_home.aspx'}
def getmd5(val):
	return hashlib.md5(val.encode(encoding='UTF-8')).hexdigest()

def getcode(s, headers):
	try:
		#如果服务器异常或者返回乱码则重新请求，死循环
		codelen = 1
		while codelen < 30:
			vc = s.get('http://jwweb.fzfu.com/sys/ValidateCode.aspx?tid=5600', headers=headers)
			if vc.status_code == 200 and len(vc.text) > 30:
				codelen = 31
		return vc.content
	except:
		#死循环抛出异常
		return getcode(s, headers)

def getlogin(s, headers, dsdsdsdsdxcxdfgfg, fgfggfdgtyuuyyuuckjg, __VIEWSTATE, pcInfo, typeName, vuser):
	try:
		codelen = 1
		print('全力抢课中\r\n')
		while codelen < 30:
			response = s.post('http://jwweb.fzfu.com/_data/login_home.aspx', data={"__VIEWSTATE": __VIEWSTATE, "Sel_Type": Sel_Type, "pcInfo":pcInfo, "typeName":typeName, "dsdsdsdsdxcxdfgfg":dsdsdsdsdxcxdfgfg, "fgfggfdgtyuuyyuuckjg":fgfggfdgtyuuyyuuckjg, "txt_asmcdefsddsd": vuser}, headers=headers) 
			if response.text.find('MAINFRM.aspx'):
				return '登陆成功..请稍后'
				codelen = 31
			else:
				print('...')
				codelen = 29
	except:
		return getlogin(s, headers, dsdsdsdsdxcxdfgfg, fgfggfdgtyuuyyuuckjg, __VIEWSTATE, pcInfo, typeName, vuser)

def getkc(s, headers):
	return s.post('http://jwweb.fzfu.com/wsxk/stu_xsyx_rpt.aspx', data={"sel_lx":2, "Submit":"%BC%EC%CB%F7"})

def endgo(s, headers, xhid):
	try:
		codelen = 1
		while codelen < 30:
			qkresult = s.post('http://jwweb.fzfu.com/wsxk/stu_xsyx_rpt.aspx?func=1', data={"sel_lx":2, "id":xhid, "chkCount":"57"}, headers=headers)
			if qkresult.text.find('成功') or qkresult.text.find('突破学分'):
				return '选课成功'
				codelen = 31
			else:
				print('错误重试中...')
				codelen = 29
	except:
		endgo(s, headers, xhid)

#初始化获得cookie
s = requests.session()
vs = s.get('http://jwweb.fzfu.com/_data/login_home.aspx')
soup = BeautifulSoup(vs.text,features='html.parser')
__VIEWSTATE = soup.input.get('value')
typeName = '%D1%A7%C9%FA'
pcInfo = 'Mozilla%2F5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F75.0.3770.100+Safari%2F537.36undefined5.0+%28Windows+NT+10.0%3B+Win64%3B+x64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F75.0.3770.100+Safari%2F537.36+SN%3ANULL'
Sel_Type = 'STU'

#拿验证码
vc = getcode(s, headers)
with open('picture.jpg', 'wb') as file:
	file.write(vc)

#用户提示	
vcode = input('请输入验证码')
vuser = input('请输入账号')
vpwd = input('请输入密码')
#计算变量
dsdsdsdsdxcxdfgfg = getmd5(vuser + getmd5(vpwd)[0:30].upper() + '13762')[0:30].upper()
fgfggfdgtyuuyyuuckjg = getmd5(getmd5(vcode.upper())[0:30].upper() + '13762' )[0:30].upper()

#登录
print(getlogin(s, headers, dsdsdsdsdxcxdfgfg, fgfggfdgtyuuyyuuckjg, __VIEWSTATE, pcInfo, typeName, vuser))

#拿到课程
xklist = getkc(s, headers)
soupxklist = BeautifulSoup(xklist.text,features='html.parser')
for xkc in soupxklist.find_all("input", attrs = {"type":"checkbox"}):
	print(xkc.get('value'), end="\r\n")

#选课
getxhid = input('请复制下你想选课的信息，不要有多余空格！')
xhid = 'TTT,' + getxhid + '$1'
print(endgo(s, headers, xhid))



