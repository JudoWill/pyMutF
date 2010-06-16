from __future__ import with_statement
from BeautifulSoup import BeautifulStoneSoup
import xml.parsers.expat
import datetime
from copy import deepcopy



def ParsePMC(XML_DATA):
	"""
	Parses a PMC XML and returns a dictionary with:
	title, journal, abstract, keywords, pub_date
	
	"""
	wanted_tags = { frozenset([u'article-meta', u'article-title', u'title-group', u'front', u'article']): ('title', 'append', ''),
			frozenset([u'front', u'article', u'journal-meta', u'journal-title']): ('journal', 'save', ''),
			frozenset([u'article-meta', u'pub-date', u'front', u'article', u'day']): ('pub_day', 'save', ''),
			frozenset([u'article-meta', u'pub-date', u'month', u'front', u'article']): ('pub_month', 'save', ''),
			frozenset([u'article-meta', u'pub-date', u'year', u'front', u'article']): ('pub_year', 'save', ''),
			frozenset([u'article-meta', u'abstract', u'p', u'front', u'article']): ('abstract', 'append', ''),
			frozenset([u'article-meta', u'abstract', u'p', u'sec', u'front', u'article']): ('abstract', 'append', ''),
			frozenset([u'article-meta', u'kwd', u'kwd-group', u'front', u'article']): ('keywords', 'append', ', ')}
	def start_element(name, attr):
		if name == u'italic':
			return
		cur_tag.add(name)
		#print name, attr
	
	def end_element(name):
		cur_tag.discard(name)
		#attrib = None
	def process_text(data):
		if len(data.strip()) == 0:
			return
		if frozenset(cur_tag) in wanted_tags:
			item, act, spacer = wanted_tags[frozenset(cur_tag)]
			if act == 'save':
				art[item] = data.strip()
			elif act == 'append':
				art[item] = spacer.join([art.get(item, ''), data.strip()])
			else:
				print 'dunno'
	cur_tag = set()
	art = {}
	p = xml.parsers.expat.ParserCreate()
	p.StartElementHandler = start_element
	p.EndElementHandler = end_element
	p.CharacterDataHandler = process_text
	
	soup = BeautifulStoneSoup(XML_DATA)
	p.Parse(soup.prettify())
	
	try:
		this_date = datetime.date(int(art.get('pub_year','2000')), 
							int(art.get('pub_month', '1')),
							int(art.get('pub_day', '1')))
	except:
		this_date = datetime.date(2000,1,1)
	finally:
		art.pop('pub_year','')
		art.pop('pub_month','')
		art.pop('pub_day','')
	
	art['pub_date'] = this_date
	
	return art
	
	
def ParsePUBMED(XML_DATA):
	"""
	Parses a PUBMED style XML data and returns a LIST od dicts with:
	title, journal, abstract, keywords, pub_date
	"""
	"""
	Parses a PMC XML and returns a dictionary with:
	title, journal, abstract, keywords, pub_date

	"""
	this_art = {}
	wanted_tags = { frozenset([u'pubmedarticle', u'pubmedarticleset', u'medlinecitation', u'articletitle', u'article']): ('title', 'append', ''),
			frozenset([u'title', u'pubmedarticle', u'journal', u'pubmedarticleset', u'medlinecitation', u'article']): ('journal', 'save', ''),
			frozenset([u'pubmedarticle', u'pubmedarticleset', u'datecreated', u'medlinecitation', u'day']): ('pub_day', 'save', ''),
			frozenset([u'pubmedarticle', u'pubmedarticleset', u'datecreated', u'medlinecitation', u'month']): ('pub_month', 'save', ''),
			frozenset([u'pubmedarticle', u'pubmedarticleset', u'datecreated', u'medlinecitation', u'year']): ('pub_year', 'save', ''),
			frozenset([u'pubmedarticle', u'abstract', u'pubmedarticleset', u'medlinecitation', u'article', u'abstracttext']): ('abstract', 'append', ''),
			frozenset([u'pubmedarticle', u'medlinecitation', u'pmid', u'pubmedarticleset']): ('PMID', 'reset', '')}
	def start_element(name, attr):
		if name == u'italic':
			return
		cur_tag.add(name)
		#print name, attr

	def end_element(name):
		cur_tag.discard(name)
		#attrib = None
	def process_text(data):
		if len(data.strip()) == 0:
			return
		if frozenset(cur_tag) in wanted_tags:
			item, act, spacer = wanted_tags[frozenset(cur_tag)]
			if act == 'save':
				this_art[item] = data.strip()
			elif act == 'append':
				this_art[item] = spacer.join([this_art.get(item, ''), data.strip()])
			elif act == 'reset':
				art_list.append(deepcopy(this_art))
				while len(this_art):
					this_art.popitem()
				this_art[item] = int(data.strip())
			else:
				print 'dunno'
	cur_tag = set()
	art_list = []
	this_art = {}
	p = xml.parsers.expat.ParserCreate()
	p.StartElementHandler = start_element
	p.EndElementHandler = end_element
	p.CharacterDataHandler = process_text
	soup = BeautifulStoneSoup(XML_DATA)
	p.Parse(soup.prettify())
	art_list.append(this_art)
	art_list.pop(0)
	for art in art_list:
		try:
			this_date = datetime.date(int(art.get('pub_year','2000')),
							int(art.get('pub_month', '1')),
							int(art.get('pub_day', '1')))
		except:
			this_date = datetime.date(2000,1,1)
		finally:
			art.pop('pub_year','')
			art.pop('pub_month','')
			art.pop('pub_day','')
		art['pub_date'] = this_date
	return art_list
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	