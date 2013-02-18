#/usr/bin/python
#coding=utf-8

import web
from model import *
from page import *

def get_page_arr():
	list = get_page_title()
	lists = []
	for l in list:
		nl = {}
		nl['id'] = l.get('ID')
		nl['title'] = l.get('post_title')
		nl['post_name'] = l.get('post_name')
		lists.append(nl)
	return lists
	
def notfound():
	return web.notfound("Sorry, the page you were looking for was not found.")
	
def page_url(total, cur_page = 0, url = '/page/%s', perpage = 10):
	return Pager(url = url,total_count = total, page_size = perpage, cur_page = cur_page).getPage()
	

	
	