from selenium import selenium
import urllib2
import re, os.path, os
import logging
from types import FunctionType, StringType
from random import shuffle
from functools import partial
#from optparse import OptionParser

from BeautifulSoup import BeautifulSoup


def do_search(uid):

    return get_soup(r'http://www.ncbi.nlm.nih.gov/pubmed/'+uid)


def get_soup(url):
    data = urllib2.urlopen(url)
    return BeautifulSoup(data.read())


def find_linkout(soup, reg):

    linkouts = soup.findAll(id = reg)

    if len(linkouts) == 1:
        logging.warning('Found single linkout')
        return linkouts[0]['id'], linkouts[0].parent['href']
    elif len(linkouts) > 1:
        logging.warning('Found multiple linkouts')
        return False
    else:
        logging.warning('Found NO linkouts!')
        return False


def get_pdf(url, uid, path = '/results'):

    if type(url) != StringType:
        url = url.pop()

    logging.warning('Opening path for %s' % uid)
    data = urllib2.urlopen(url)
    with open(os.path.join(path, '%s.pdf' % uid), 'w') as handle:
        logging.warning('Writting data for %s' % uid)
        handle.write(data.read())
    logging.warning('Sucess for %s' % uid)

def process_soup(kwargs, soup, top_url, final = False, parent = True):

    tag = soup.find(**kwargs)
    if parent:
        url = tag.parent['href']
    else:
        url = tag['href']

    if url.startswith('http'):
        final_url = url
    else:
        final_url = top_url+url

    if final:
        return final_url, None
    else:
        return None, get_soup(final_url)





if __name__ == '__main__':

    results_dir = '/results/'

    with open('no_links.txt') as handle:
        finished = set([x.strip() for x in handle if x.strip()])

    with open('skipping.txt') as handle:
        finished |= set([x.strip() for x in handle if x.strip()])

    with open('missing_path.txt') as handle:
        finished |= set([x.split(',')[0] for x in handle if x.strip()])

    with open('pubmed_result.txt') as handle:
        pmids = [x.strip() for x in handle if x.strip() and x not in finished]
    shuffle(pmids)

    #this dict contains the "click" items that will bring the selenium item to a
    #page with the pdf-url
    path_dict = {
        'linkout-icon-unknown-jvi_final':None,
        'linkout-icon-unknown-4690':None,
        'linkout-icon-unknown-jem_final':(partial(process_soup, {'text':"Full Text (PDF)"}),
                                            partial(process_soup, {})),
        'linkout-icon-unknown-jbc_full_free':tuple(),
        'linkout-icon-unknown-UChicago100x25':("link=PDF Version",),
        'linkout-icon-unknown-aac_final':("link=Full Text (PDF)",),
        'linkout-icon-unknown-vir_full':("link=Full Text (PDF)",),
        'linkout-icon-unknown-acspubs':(acs_custom,),
        'linkout-icon-unknown-oxfordjournals':("link=Full Text (PDF)",),
        'linkout-icon-unknown-ben_pubmed':False,
        'linkout-icon-unknown-pnas_full':tuple(),
        'linkout-icon-unknown-jvi_full':tuple(),
        'linkout-icon-unknown-anakarder':False,
        'linkout-icon-unknown-pmc':None,
        'linkout-icon-unknown-lo_npg':tuple(),
        'linkout-icon-unknown-wiley_interscience_pubmed_logo_120x27':None, #
        'linkout-icon-unknown-bj_pubmed_latest':tuple(),
        'linkout-icon-unknown-adis1':None, #need redirect
        'linkout-icon-unknown-springerlink':tuple(), #
        'linkout-icon-unknown-jbc_final':("link=Full Text (PDF)",),
        'linkout-icon-unknown-jcm_final':("link=Full Text (PDF)",),
        'linkout-icon-unknown-linkout':None,
        'linkout-icon-unknown-Button_120x27px_FullText':None,
        'linkout-icon-unknown-aac_full':tuple(),
        'linkout-icon-unknown-pmlo_ijmm':False,
        'linkout-icon-unknown-MAL_100x25':None,
        'linkout-icon-unknown-lo_nature':tuple(),
        'linkout-icon-unknown-mc':False,
        'linkout-icon-unknown-dmd_final':False,
        'linkout-icon-unknown-annintmed_final':("link=Full Text (PDF)",),
        'linkout-icon-unknown-jcm_full':tuple(),
        'linkout-icon-unknown-wjg':False,
        'linkout-icon-unknown-MS':tuple(),
        'linkout-icon-unknown-bmc':tuple(),
        'linkout-icon-unknown-pmlogo':False
        #'linkout-icon-unknown-PubMedLink':(process_sd, ),
        #'linkout-icon-unknown-cellhub':(process_sd),
    }




    no_links = open('no_links.txt', 'a')
    missing_path = open('missing_path.txt', 'a')
    skipping = open('skipping.txt', 'a')

    linkout_reg = re.compile('linkout-icon-unknown-[\w-]*')

    for pmid in pmids:
        found = do_search(pmid)
        if found:
            linkout_res = find_linkout(found, linkout_reg)
            if linkout_res:
                linkout, url = linkout_res
                top_url = ''
                try:
                    path = path_dict[linkout]
                except KeyError:
                    logging.warning('No path for linkout!: %s at pmid:%s' % (linkout, pmid))
                    missing_path.write('%s,%s\n' % (pmid, linkout))
                    continue
                if path:
                    soup = get_soup(url)
                    pdf_url = None
                    for func in path:
                        pdf_url, soup = func(soup, top_url)

                    get_pdf(pdf_url, pmid, path = results_dir)
                elif path is False:
                    skipping.write(pmid+'\n')
                elif path is None:
                    missing_path.write('%s,%s\n' % (pmid, linkout))

        else:
            no_links.write(pmid+'\n')












































