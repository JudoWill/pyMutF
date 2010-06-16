import sys
import logging, logging.handlers
import PyMozilla
import re
from BeautifulSoup import BeautifulStoneSoup


def GetXML(ID_LIST, db = 'pubmed'):

    valid_db = set(['pubmed', 'pmc'])
    assert db in valid_db

    POST_URL = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/epost.fcgi?db=%s' % db
    RET_URL = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=%s&query_key=1&mode=xml&rettype=full' % db

    pmid_list = ','.join(map(lambda x: str(x), ID_LIST))
    post_req_url = POST_URL + '&id=' + pmid_list

    moz_emu = PyMozilla.MozillaEmulator(cacher = None)
    post_res = moz_emu.download(post_req_url, trycount = 3)

    web_env = re.findall('<WebEnv>(.*?)</WebEnv>', post_res)[0]

    req_url = RET_URL + '&WebENV=' + web_env

    xml_data = moz_emu.download(req_url, trycount = 3)
    return xml_data


def SearchPUBMED(search_sent, recent_date = None):

    POST_URL = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&retmax=1000000'
    moz_emu = PyMozilla.MozillaEmulator(cacher = None)

    search_term = search_sent.replace(' ', '+')
    search_url = POST_URL + '&term=' + search_term
    if recent_date:
        search_url += '&reldate=' + str(recent_date)

    xml_data = moz_emu.download(search_url, trycount = 3)

    id_list = re.findall('<Id>(\d*)</Id>', xml_data)
    id_nums = map(lambda x: int(x), id_list)
    return id_nums


def ExtractPMCPar(xmldata):
    """Yields sucessive paragraphs from a PMC xml"""

    xmltree = BeautifulStoneSoup(xmldata)
    for par in xmltree.findAll('p'):
        buffer = ''
        for item in par.findAll(text=True):
            buffer += item.string.strip()

        yield buffer


def ExtractPubPar(xmldata):
    """Yields sucessive paragraphs from a Pubmed xml"""

    xmltree = BeautifulStoneSoup(xmldata)
    yield xmltree.find('abstracttext').string.strip()
























