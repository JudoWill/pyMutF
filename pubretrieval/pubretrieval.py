from selenium import selenium
import urllib2
import re, os.path, os
import logging
from types import FunctionType, StringType
#from optparse import OptionParser




def do_search(sel, uid):

    sel.open('/pubmed')
    sel.type('search_term', '%s[uid]' % uid)
    sel.click('search')
    sel.wait_for_page_to_load("30000")
    sel.select_frame("relative=up")
    return sel.is_text_present(uid)


def find_linkout(sel):

    linkouts = re.findall('linkout-icon-unknown-[\w-]*', sel.get_html_source())

    if len(linkouts) == 1:
        logging.warning('Found single linkout')
        return linkouts[0]
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
    data = urllib2.open(url)
    with open(os.path.join(path, '%s.pdf' % uid), 'w') as handle:
        logging.warning('Writting data for %s' % uid)
        handle.write(data.read())
    logging.warning('Sucess for %s' % uid)


def get_pdf_link(sel):
    url_reg = r'http\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?.pdf'

    return re.findall(url_reg, sel.get_html_source())

def process_sd(sel):
    return False

def acs_custom(sel):
    return False


if __name__ == '__main__':

    results_dir = '/results/'

    with open('finished.txt') as handle:
        finished = set([x for x in handle if x.strip()])

    with open('pubmed_result.txt') as handle:
        pmids = [x.strip() for x in handle if x.strip() and x not in finished]


    #this dict contains the "click" items that will bring the selenium item to a
    #page with the pdf-url
    path_dict = {
        'linkout-icon-unknown-jvi_final':("//div[@id='content-block-1']/table[1]/tbody/tr/td/table/tbody/tr[4]/td[2]/strong/a/strong",),
        'linkout-icon-unknown-4690':tuple(),
        'linkout-icon-unknown-jem_final':("link=Full Text (PDF)",),
        'linkout-icon-unknown-jbc_full_free':tuple(),
        'linkout-icon-unknown-UChicago100x25':("link=PDF Version",),
        'linkout-icon-unknown-aac_final':("link=Full Text (PDF)",),
        'linkout-icon-unknown-vir_full':("link=Full Text (PDF)",),
        'linkout-icon-unknown-acspubs':(acs_custom,),
        'linkout-icon-unknown-oxfordjournals':None,
        'linkout-icon-unknown-ben_pubmed':None,
        'linkout-icon-unknown-pnas_full':None,
        'linkout-icon-unknown-jvi_full':None,
        'linkout-icon-unknown-anakarder':None,
        'linkout-icon-unknown-pmc':None,
        'linkout-icon-unknown-lo_npg':None,
        'linkout-icon-unknown-wiley_interscience_pubmed_logo_120x27':None,
        'linkout-icon-unknown-bj_pubmed_latest':None,
        'linkout-icon-unknown-adis1':None,
        'linkout-icon-unknown-springerlink':None,
        'linkout-icon-unknown-jbc_final':None,
        'linkout-icon-unknown-jcm_final':None,
        'linkout-icon-unknown-linkout':None,
        'linkout-icon-unknown-Button_120x27px_FullText':None,
        'linkout-icon-unknown-aac_full':None,
        'linkout-icon-unknown-pmlo_ijmm':None,
        'linkout-icon-unknown-MAL_100x25':None,
        'linkout-icon-unknown-lo_nature':None,
        'linkout-icon-unknown-mc':None,
        'linkout-icon-unknown-dmd_final':None,
        'linkout-icon-unknown-annintmed_final':None,
        'linkout-icon-unknown-jcm_full':None,
        'linkout-icon-unknown-wjg':None,
        'linkout-icon-unknown-MS':None,
        'linkout-icon-unknown-bmc':None,
        'linkout-icon-unknown-pmlogo':("//div[@id='site-left']/a/img", "//a[@id='pdf']/span"),
        #'linkout-icon-unknown-PubMedLink':(process_sd, ),
        #'linkout-icon-unknown-cellhub':(process_sd),
    }


    sel = selenium("localhost", 4444, "*chrome", "http://www.ncbi.nlm.nih.gov/")
    sel.start()

    out_handle = open('finished.txt', 'a')

    for pmid in pmids:
        found = do_search(sel, pmid)
        if found:
            linkout = find_linkout(sel)
            if linkout:
                try:
                    path = path_dict[linkout]
                except KeyError:
                    logging.warning('No path for linkout!: %s at pmid:%s' % (linkout, pmid))
                    continue
                if path is not None:
                    sel.click(linkout)
                    sel.wait_for_page_to_load("30000")
                    further_dl = True
                    for link in path:

                        if type(link) == StringType:
                            print 'clicking: ', link
                            sel.click(link)
                            sel.wait_for_page_to_load("30000")
                        elif type(link) == FunctionType:
                            further_dl = link(sel)
                    if further_dl:
                        pdf_url = get_pdf_link(sel)
                        if pdf_url:
                            get_pdf(pdf_url, pmid, path = results_dir)
                else:
                    continue
            out_handle.write(pmid+'\n')













































