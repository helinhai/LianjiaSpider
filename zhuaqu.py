import json
from bs4 import BeautifulSoup
import re
import requests
import demjson
import time
import pandas as pd


headers={'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2;.NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; InfoPath.3; .NET4.0C; .NET4.0E)',
		 'Accept':'image/webp,image/*,*/*;q=0.8',
		 'Accept-Encoding':'gzip, deflate',
		 'Referer':'http://www.baidu.com/link?url=_andhfsjjjKRgEWkj7i9cFmYYGsisrnm2A-TN3XZDQXxvGsM9k9ZZSnikW2Yds4s&amp;amp;wd=&amp;amp;eqid=c3435a7d00006bd600000003582bfd1f',
		 'Connection':'keep-alive'}
page=('pg')

def generate_cityurl(user_in_city):  # 生成url
	cityurl = 'https://' + user_in_city + '.lianjia.com/ershoufang/'    
	return  cityurl
	#return demjson.encode(res)
	"""
	d = json.loads(res.read().decode()).get('data')

	if d is None:
		print("城市首页加载完成")
		return 
	"""
		
def homeinfo(cityurl,user_in_city):  
	res = requests.get(cityurl,headers=headers)
	homehtml = res.text
	lj = BeautifulSoup(homehtml,'html.parser')
	urldiv = lj.find("div",attrs={"data-role":"ershoufang"})
	links = urldiv.contents[1]
	links = str(links)
	res_url = r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"  
	link = re.findall(res_url,links,re.I|re.S|re.M)  # 获取href里面的链接内容
	arealists = []
	for url in link:
		arealist = 'https://'+user_in_city+'.lianjia.com'+url
		arealists.append(arealist)
	print("获取"+user_in_city+"的各个城区起始url:")
	print(arealists[0])
	return arealists

def areainfo(url):
	page = ('pg')
	for i in range(1,100):  #获取1-100页的数据
		if i == 1:
			i = str(i)
			a = (url+page+i+'/') 
			r = requests.get(url=a,headers=headers)
			print(a)
			htmlinfo = r.content
		else:
			i = str(i)
			a = (url+page+i+'/') 
			print(a)
			r = requests.get(url=a,headers=headers)
			html2 = r.content
			htmlinfo = htmlinfo+html2
	time.sleep(0.5)
	return htmlinfo

def listinfo(listhtml):
	areasoup = BeautifulSoup(listhtml,'html.parser')
	ljhouse = areasoup.find_all('div',attrs={'class':'info clear'})
	for house in ljhouse:
		print(house)
		titleinfo = house.find("div",attrs={"class":"title"})
		addressinfo = house.find("div",attrs={"class":"address"})
		floodinfo = house.find("div",attrs={"class":"flood"})
		followinfo = house.find("div",attrs={"class":"followInfo"})
		taginfo = house.find("div",attrs={"class":"tag"})
		priceinfo = house.find("div",attrs={"class":"priceInfo"})
		url = titleinfo.a['href']
		title = titleinfo.a.get_text()
		xiaoqu_url = addressinfo.div.a['href']
		xiaoqu_name = addressinfo.div.a.get_text()
		desc = addressinfo.div.get_text()
		region = floodinfo.div.a.get_text()
		region_desc = floodinfo.div.get_text()
		follow = followinfo.span.get_text()
		#获取描述性tag
		tags = taginfo.find_all('span')
		i = 0
		tagdesc = []
		for tag in tags:
			tagdesc.append(tag.get_text())
		totalprice = priceinfo.find("div",attrs={"class":"totalPrice"}).span.get_text()
		unitprice = priceinfo.find("div",attrs={"class":"unitPrice"}).span.get_text()
		houseinfo = houseinfo.append({'title':title,'url':url,'xiaoqu_name':xiaoqu_name,'xiaoqu_url':xiaoqu_url,'desc':desc,'region':region,'region_desc':region_desc,'follow':follow,'tagdesc':tagdesc,'totalprice':totalprice,'unitprice':unitprice},ignore_index=True)
		print(houseinfo.tail(10))

if __name__ == '__main__':
	user_in_city = input('输入抓取城市：')
	url = generate_cityurl(user_in_city)
	print(url)
	homelist = homeinfo(url,user_in_city) # 获取各个城区起始页url
	print(homelist)
	houseinfo = pd.DataFrame({'title':'','url':'','xiaoqu_name':'','xiaoqu_url':'','desc':'','region':'','region_desc':'','follow':'','tagdesc':'','totalprice':'','unitprice':''},index=["0"])
	for homeurl in homelist:
		areahtml = areainfo(homeurl)
		listinfo(areahtml)
	houseinfo.to_csv('data/data_chengdu.csv',encoding='utf-8',index=False)  




		

