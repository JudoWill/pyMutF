from selenium import selenium
import urllib2
import re, os.path, os
import logging
from types import FunctionType, StringType
from random import shuffle
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
    data = urllib2.urlopen(url)
    with open(os.path.join(path, '%s.pdf' % uid), 'w') as handle:
        logging.warning('Writting data for %s' % uid)
        handle.write(data.read())
    logging.warning('Sucess for %s' % uid)


def get_pdf_link(sel):
    url_reg = r'http\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?.pdf'

    res = re.findall(url_reg, sel.get_html_source())
    if len(res) == 0:

        url_reg = r'(/\S*)?.pdf'
        res = re.findall(url_reg, sel.get_html_source())
        if len(res):
            url = sel.get_location().split('/')
            base = '/'.join(url[:3])
            final = []
            for r in res:
                if r.startswith('/'):
                    final.append(base+r)
                else:
                    final.append(base+'/'+r)
            return final
    else:
        return res




def process_sd(sel):
    return False

def acs_custom(sel):
    return False

def change_focus(sel, new_window = 'undefined'):
    sel.select_window(new_window)
    return True

def close_window(sel):
    sel.close()

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
        'linkout-icon-unknown-jvi_final':("//div[@id='content-block-1']/table[1]/tbody/tr/td/table/tbody/tr[4]/td[2]/strong/a/strong",),
        'linkout-icon-unknown-4690':tuple(),
        'linkout-icon-unknown-jem_final':("link=Full Text (PDF)",),
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


    sel = selenium("localhost", 4444, "*chrome", "http://www.ncbi.nlm.nih.gov/")
    sel.start()
    sel.open('about:blank')
    raw_input()


    no_links = open('no_links.txt', 'a')
    missing_path = open('missing_path.txt', 'a')
    skipping = open('skipping.txt', 'a')


    for pmid in pmids:
        found = do_search(sel, pmid)
        if found:
            linkout = find_linkout(sel)
            if linkout:
                try:
                    path = path_dict[linkout]
                except KeyError:
                    logging.warning('No path for linkout!: %s at pmid:%s' % (linkout, pmid))
                    missing_path.write('%s,%s\n' % (pmid, linkout))
                    continue
                if path:
                    sel.click(linkout)
                    sel.select_pop_up('null')
                    print sel.get_all_window_titles()
                    try:
                        sel.wait_for_page_to_load("30000")
                    except:
                        pass
                    print sel.get_all_window_titles()
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
                elif path is False:
                    skipping.write(pmid+'\n')
                elif path is None:
                    missing_path.write('%s,%s\n' % (pmid, linkout))

        else:
            no_links.write(pmid+'\n')












































