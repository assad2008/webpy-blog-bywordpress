#/usr/bin/python
#coding=utf-8

import sys
import hashlib
import web,datetime
from web.net import htmlquote

db = web.database(dbn = 'mysql', db = '36coder', user = '36coder',pw = '36coder')

def get_post(id):
	try:
		ret = db.select('wp_posts', where='id=%s' % id, vars=locals())[0]
		ret['post_content'] = ret.get('post_content').rstrip()
		return ret
	except:
		return None
	

def get_posts(start = 0,perpage = 10):
	try:
		blog = []
		ret = db.query("select * from wp_posts where post_status='publish' and post_type='post' order by id desc limit %s,%s" % (start,perpage))
		for post in ret:
			post['post_content'] = post.get('post_content').rstrip()
			blog.append(post)
		return blog
	except:
		return None

def get_post_count():
	return db.query("select count(*) as num from wp_posts where post_status='publish' and post_type='post'")[0].get('num')

def get_page(id):
	try:
		return db.select('wp_posts', where="id=%s and post_type='page'" % id, vars=locals())[0]
	except:
		return None

def get_id_by_post_name(post_name):
	try:
		return db.select('wp_posts', where="post_name='%s'" % post_name, vars=locals())[0].get('ID')
	except:
		return None	

def get_page_title():
	return db.select('wp_posts',where = "post_type='page' and post_status='publish'",order = 'id ASC')
	
def get_archives():
	year = db.query("select YEAR(post_date) AS year from wp_posts where post_status='publish' and post_type='post' group by year order by post_date desc")
	list = []
	for Y in year:
		yn = str(Y.get('year'))
		posts = db.query("select * from wp_posts where post_status='publish' and post_type='post' and str_to_date('" +yn +"-01-01 00:00:00','%Y-%m-%d %H:%i:%s')<post_date and str_to_date('" + yn + "-12-31 23:59:59','%Y-%m-%d %H:%i:%s')>post_date order by post_date desc")
		nl = {}
		nl['year'] = yn
		nl['list'] = []
		for lp in posts:
			yeardate = lp.get('post_date_gmt').strftime("%Y")
			nlp = {}
			nlp['id'] = lp.get('ID')
			nlp['title'] = lp.get('post_title')
			nlp['dateline'] = lp.get('post_date_gmt').strftime("%Y-%m-%d")
			nl['list'].append(nlp)
		list.append(nl)
	return list
	
def get_links():
	return db.select('wp_links',order = 'link_id ASC',where = "link_visible='Y'")
	
def do_comment(id,content):
	pass
	
def get_avatar(email):
	return "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest()+'?s=60'

def get_blog_comment(id):
	list = []
	ret = db.select('wp_comments',where = "comment_post_ID=%s and comment_approved=1" % id,order = 'comment_date_gmt desc')
	if not ret:
		return None
	for r in ret:
		r['avatar'] = get_avatar(r.get('comment_author_email'))
		list.append(r)
	return list

def get_category():
	result = db.query("select wt.term_id,wt.name,wt.slug,wtt.count from wp_term_taxonomy as wtt left join wp_terms as wt on wtt.term_id=wt.term_id where wtt.taxonomy='category'")
	data = []
	for i in result:
		data.append(i)
	return data
	
def get_tags():
	result = db.query("select wt.term_id,wt.name,wt.slug,wtt.count from wp_term_taxonomy as wtt left join wp_terms as wt on wtt.term_id=wt.term_id where wtt.taxonomy='post_tag'")
	data = []
	for i in result:
		data.append(i)
	return data
	
def get_blog_by_tag(tag_id,start = 0, perpage = 20):
	result = db.query("select wtr.object_id as id from wp_term_relationships as wtr left join wp_term_taxonomy as wtt on wtr.term_taxonomy_id=wtt.term_taxonomy_id where wtt.term_id=%s order by object_id desc limit %s,%s" % (tag_id,start,perpage))
	data = []
	for i in result:
		blog = db.query('select ID,post_title,post_date_gmt from wp_posts where ID=%s' % i.get('id'))[0]
		data.append(blog)
	return data
	
def get_blog_tags(id):
	return db.query('select wt.term_id,wt.name from wp_term_relationships as wtr left join wp_term_taxonomy as wtt on wtr.term_taxonomy_id=wtt.term_taxonomy_id left join wp_terms as wt on wt.term_id=wtt.term_id where wtr.object_id=%s' % id)
	
def makerss():
	list = db.select('wp_posts', where = "post_status='publish' and post_type='post'", order='id DESC', limit = '%s' % 20)
	xml = ''
	xml += '<?xml version="1.0" encoding="utf-8" ?>' + "\n"
	xml += '<rss version="2.0">' + "\n"
	xml += '<channel>' + "\n"
	xml += '<title>三流编码员</title>' + "\n"
	xml += '<link>http://py.36coder.com/</link>' + "\n"
	xml += '<description>Latest 20 threads of all jobs</description>' + "\n"
	xml += '<copyright>Copyright(C) 三流编码员</copyright>' + "\n"
	xml += '<generator>36coder by River King.</generator>' + "\n"
	xml += '<lastBuildDate>' + datetime.datetime.now().strftime("%Y-%m-%d %X") + '</lastBuildDate>' + "\n"
	xml += '<ttl>3600</ttl>' + "\n"
	for l in list:
		xml += '<item>' + "\n"
		xml += '<title>' + l.get('post_title').encode('utf-8') + '</title>' + "\n"
		xml += '<link>http://py.36coder.com/view/' + str(l.get('ID')) + '</link>' + "\n"
		xml += '<description><![CDATA[' + l.get('post_content').encode('utf-8') + ']]></description>' + "\n"
		xml += '<author>36coder</author>' + "\n"
		xml += '<pubDate>' + l.get('post_date_gmt').strftime("%Y-%m-%d %X") + '</pubDate>' + "\n"
		xml += '</item>' + "\n"
	xml += '</channel>' + "\n"
	xml += '</rss>'
	return xml