#/usr/bin/python
#coding=utf-8

import sys,web

sys.path.append("/pythonweb/36coder/")
from model import *
from function import *

urls = (
	'/','Index',
	'/view/(\d+)','View',
	'/news/(\w+)','News',
	'/archives','Archives',
	'/links','Links',
	'/comment','Comment',
	'/page/(\d+)','Pages',
	'/feed','Feeds'
)

web.config.debug = True
base_url = 'http://py.36coder.com'
t_globals = {
    'datestr': web.datestr
}

render = web.template.render('/pythonweb/36coder/templates/',globals=t_globals)

class Index:
	def GET(self):
		posts = get_posts()
		pages = get_page_arr()
		page_urls = page_url(get_post_count(),1)
		return render.index(posts,base_url,pages,page_urls)

class Pages:
	def GET(self,id):
		id = int(id)
		id = id <= 0 and 1 or id
		start = (id - 1) * 10
		posts = get_posts(start)
		pages = get_page_arr()
		page_urls = page_url(get_post_count(),id)
		return render.index(posts,base_url,pages,page_urls)
		
		
class View:
	def GET(self,id):
		post = get_post(int(id))
		pages = get_page_arr()
		comments = get_blog_comment(id)
		if not post:
			return notfound()
		else:
			return render.view(post,comments,base_url,pages)
		
class News:
	def GET(self,id):
		page_id = get_id_by_post_name(id)
		if not page_id:
			return notfound()
		pageinfo = get_page(page_id)
		comments = get_blog_comment(page_id)
		pages = get_page_arr()
		if not pageinfo:
			return notfound()
		else:
			return render.pages(pageinfo,comments,base_url,pages)
		
class Archives:
	def GET(self):
		aclist = get_archives()
		pages = get_page_arr()
		return render.archives(aclist,base_url,pages)
		
class Links:
	def GET(self):
		links = get_links()
		pages = get_page_arr()
		return render.links(links,base_url,pages)
		
class Comment:
	def POST(self):
		form = web.input()		
		if not form.c_ontent:
			raise web.seeother('/view/' + id)
		else:
			id = form.id;
			content = form.c_ontent
			do_comment(id,content)
			raise web.seeother('/view/' + id)

class Feeds:
	def GET(self):
		return makerss()
		
class Search:
	def GET(self):
		pass

app = web.application(urls, globals())
application = app.wsgifunc()