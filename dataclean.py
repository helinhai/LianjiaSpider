import json
from bs4 import BeautifulSoup
import re
import requests
import demjson
import time
import pandas as pd

def data_clean(housedata):
	houseinfo_split = pd.DataFrame((x.str.extract('?室？厅') for x in housedata.desc),index=housedata.index,columns=['test'])
	#index=housedata.index,columns=['xiaoqu','huxing','miaoji','chaoxiang','zhuangxiu','dianti'])
	print(houseinfo_split.head(10))

if __name__ == '__main__':
	df = pd.read_csv('data/data_jinjiang.csv')  
	housedata = pd.DataFrame(df.head(1))
	print(housedata.head(10))
	data_clean(housedata)
