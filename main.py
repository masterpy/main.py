# -*- coding: utf-8 -*-

import getopt,sys
import requests
from bs4 import BeautifulSoup
import time
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')

headers={
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/34.0.1847.116 Chrome/34.0.1847.116 Safari/537.36",
	"Accept-Encoding": "gzip,deflate,sdch",
	"Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
	"Cookie": "vjuids=-46625fb1a.14d0dabe5e2.0.3a08331c; vjlast=1430453479.1432302557.13; SUV=1505011211209788; ip_city=%E5%8C%97%E4%BA%AC; _smuid=7mFkCrvkoWJl29DZVh7Gz; adaptor_version=3; position=8; page_version=3; _xsrf=3f8a9a1534524940acfe8b32f9f3ce29; home_infoflow_ad_turn=52; indexWin=1; home_banner_ad_turn=66; hide_ad=0; indexSelect=1"
}

def usage():
	print("Usae:main.py [options] 抓取保存文件")
	print("\n\n")
	print("Options:\n")
	print("-d   时间以秒计数i\n")
	print("-u   要抓取的网址如http://m.sohu.com\n")
	print("-o   抓取完成要保存的文件夹\n")

def now_time():
	return time.strftime('%Y%m%d%H%M',time.localtime(time.time()))


def spider(url, headers, BASE):
	"""
	@deco 爬取网页内容
	"""
	# 加上头部，否则抓取不完整
	response = requests.get(url=url, headers=headers)
	soup = BeautifulSoup(response.text, 'lxml')
	lst_img = soup.find_all('img')
	img_length = len(lst_img)
	dirname = now_time()
	dir_base = BASE + dirname
	dir_base_img = dir_base + '/img/'
	dir_base_js = dir_base + '/js/'
	dir_base_css = dir_base + '/css/'
	if not os.path.exists(dir_base):
		os.mkdir(dir_base)
		os.mkdir(dir_base_img)
		os.mkdir(dir_base_js)
		os.mkdir(dir_base_css)
	for i in xrange(img_length):
		url = lst_img[i]['src']
		image = requests.get(url=url)
		print url
		final_path = dir_base_img + url.split('/')[-1]
		with open(final_path, "wb") as f:
			f.write(image.content)
		lst_img[i]['src'] = final_path


	js_file = soup.find_all('script')[1]
	js_script = requests.get(url=js_file['src'])
	final_path = dir_base_js + js_file['src'].split('/')[-1]


	png_file = soup.find_all('link')[0]
	print png_file
	css_file = soup.find_all('link')[1]
	logo_file = requests.get(url=url + png_file['href'])
	home_file = requests.get(url=css_file['href'])
	png_final_path = dir_base_img + png_file['href'].split('/')[-1]
	css_final_path = dir_base_css + css_file['href'].split('/')[-1]

	with open(final_path, "wb") as f0, open(css_final_path, "wr") as f1, open(png_final_path, "wb") as f2:
		f0.write(js_script.content)
		f1.write(home_file.content)
		f2.write(logo_file.content)

	js_file['src'] = final_path
	png_file['href'] = png_final_path
	css_file['href'] = css_final_path

	with open(dir_base + '/index.html', 'wb') as f:
		f.write(str(soup))

if __name__ == "__main__":
	try:
		opts, args = getopt.getopt(sys.argv[1:], "d:u:o:")
	except getopt.GetoptError:
		# print help information
		pass
	for opt, arg in opts:
		if opt in ("-d"):
			rand_time = arg
			print opt, arg
		elif opt in ("-u"):
			url = arg
			print opt, arg
		elif opt in ("-o"):
			directory = arg
			print opt, arg
		else:
			usage()
			sys.exit()
	while True:
		spider(url=url, headers=headers, BASE=directory)
		time.sleep(int(rand_time))