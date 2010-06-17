from __future__ import with_statement
import csv, os
import os.path
from PubmedUtils import *
from threading import Semaphore, Timer
from BeautifulSoup import BeautifulStoneSoup
from mutation_finder import *


def GetXMLData(pmid, cachedir, timed_sem, db='pubmed', use_cache=True):
    """Get an XML document either from the cache-directory or download it from Pubmed"""

    f = os.path.join(cachedir, pmid + '.xml')
    if os.path.exists(f) and use_cache:
        return open(f).read()
    else:
        with timed_sem:
            out = GetXML([pmid], db=db)
        with open(f, 'w') as handle:
            tree = BeautifulStoneSoup(out)
            handle.write(tree.prettyify())
        return out

class TimedSemaphore():
    def __init__(self, timer, total):
        self.sem = Semaphore(total)
        self.time = timer

    def release(self):
        print 'releasing'
        self.sem.release()

    def acquire(self):
        self.sem.acquire()

    def __enter__(self):
        print 'waiting'
        self.acquire()

    def __exit__(self, typ, value, traceback):
        Timer(self.time, self.release).start()


if __name__ == '__main__':
    cachedir = os.path.abspath('cachedata') + os.sep

    with open('hiv_interactions') as handle:
        inter_list = list(csv.DictReader(handle, delimiter='\t'))

    with open('results.csv') as handle:
        known_list = list(csv.DictReader(handle))

    pmid_pmc = {}
    with open('PMC-ids.csv') as handle:
        for row in csv.DictReader(handle):
            pmid_pmc[row['PMID']] = row['PMCID']

    known_set = set()
    for row in known_list:
        known_set.add((row['human-entrez'], row['hiv-protein'],
                       row['interaction-type'], row['pmid']))

    mutFinder = mutation_finder_from_regex_filepath('regex.txt')

    timed_sem = TimedSemaphore(2, 3)
    with open('results.csv', 'w') as handle:
        fnames = ('hiv-protein', 'human-protein', 'human-entrez', 'interaction-type',
                  'pmid', 'paragraph', 'protein', 'mutation', 'effect')
        res_writter = csv.DictWriter(handle, fnames)
        res_writter.writerows(known_list)

        for row in inter_list:
            for pmid in row['PubMed-ID'].split(','):
                key = (row['Gene-ID-2'], row['HIV-product-name'],
                       row['Interaction-short-phrase'], pmid)
                if key not in known_set:
                    print 'retrieving %s' % pmid
                    if pmid in pmid_pmc:
                        print 'getting PMC'
                        xmldata = GetXMLData(pmid_pmc[pmid], cachedir, timed_sem,
                                             db='pmc')
                        pargen = ExtractPMCPar(xmldata)
                    else:
                        xmldata = GetXMLData(pmid, cachedir, timed_sem)
                        pargen = ExtractPubPar(xmldata)

                    try:
                        for par in pargen:
                            for mut, loc in mutFinder(par).items():
                                t = {'hiv-protein': row['HIV-product-name'],
                                     'human-protein': row['Human-product-name'],
                                     'human-entrez': row['Gene-ID-2'],
                                     'interaction-type':row['Interaction-short-phrase'],
                                     'pmid':pmid, 'paragraph':par, 'mutation':str(mut)}

                                res_writter.writerow(t)
                        handle.flush()
                        os.fsync(handle)
                    except:
                        pass



































