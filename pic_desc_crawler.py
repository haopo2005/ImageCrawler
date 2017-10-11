#coding=utf-8
import requests,os
from bs4 import BeautifulSoup
import urllib2,sys
reload(sys)
sys.setdefaultencoding("utf-8")
base_url = "http://www.ivsky.com/"
mypath = '/home/jst/share/tupian/'
headers = {'User-Agent': 'Chrome/60.0.3112.113'}
 
 """
 get url of larger imgs
 """
def get_bigimg_url(url): 
	page = urllib2.urlopen(url)
	soup_packtpage = BeautifulSoup(page,"lxml")
	page.close()
	#print soup_packtpage.prettify()
	imgurl = soup_packtpage.find("div", id="pic_con")
	#print imgurl.div.img['src']
	return imgurl.div.img['src']

"""
get the image details
"""
def get_realimg(url):
	page = urllib2.urlopen(url)
	soup_packtpage = BeautifulSoup(page,"lxml")
	page.close()
	#print soup_packtpage.prettify()
	desc = soup_packtpage.find("div", class_="al_p")
	title = soup_packtpage.find("div", class_="al_tit")
	url = soup_packtpage.find_all("div", class_="il_img")
	img_title = title.h1.string
	try:
		img_desc =  desc.p.string
	except AttributeError: 
		print '叼毛网站不规范'
		img_desc = None
		
	img_list = []
	for img_url in url:
		cur_img_url = base_url + img_url.a['href']
		img_list.append(get_bigimg_url(cur_img_url))
	return img_desc, img_title, img_list

"""
save the descirption file and image file
"""
def download_imgs_desc(img_desc, img_title, img_list):
	current_path = mypath + img_title
	if not os.path.exists(current_path):
		os.mkdir(current_path)
		print 'Successfully created directory ', current_path
	
	if img_desc != None:
		file_object = open(os.path.join(current_path, "desc"),'w')
		print img_desc
		file_object.write(img_desc)
		file_object.close()
	
	name=0
	for img_url in img_list:
		request = urllib2.Request(img_url, None, headers)  
		response = urllib2.urlopen(request)
		with open(os.path.join(current_path, "%s.jpg" % name),'wb') as f:
			f.write(response.read())
			name += 1
"""
get the current page details
"""
def get_imgsdetails(url):
	page = urllib2.urlopen(url)
	soup_packtpage = BeautifulSoup(page,"lxml")
	page.close()
	cur_page =  soup_packtpage.find_all("div", class_="il_img")
	for mp in cur_page:
		cur_img_url = base_url + mp.a['href']
		#print cur_img_url
		img_desc, img_title, img_list = get_realimg(cur_img_url)
		download_imgs_desc(img_desc, img_title, img_list)

"""
returns the next page URL if we provide
the current page URL. For the last page, it returns None
"""
def get_img_urls(url):
	page = urllib2.urlopen(url)
	soup_packtpage = BeautifulSoup(page,"lxml")
	page.close()
	next_page_li = soup_packtpage.find("a", class_="page-next")
	#print next_page_li['href']
	if next_page_li is None :
		next_page_url = None
	else:
		next_page_url = base_url + next_page_li['href']
	return next_page_url

if __name__ == "__main__":
	start_url = 'http://www.ivsky.com/tupian/meishishijie/index_7.html'
	
	if not os.path.exists(mypath):
		os.mkdir(mypath)
		print 'Successfully created directory ', mypath

	while True:
		get_imgsdetails(start_url)
		next_page_url = get_img_urls(start_url)
		if next_page_url is None:
			break
		else:
			print 'located: '+next_page_url
			start_url = next_page_url
	print 'end!'
	sys.exit(0)