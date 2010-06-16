from __future__ import with_statement
import csv, os
import os.path
from PubmedUtils import GetXML
from threading import Semaphore, Timer




def GetXMLData(pmid, cachedir, timed_sem):
    """Get an XML document either from the cache-directory or download it from Pubmed"""

    f = os.path.join(cachedir, pmid+'.xml')
    if os.path.exists(f):
        return open(f).read()
    else:
        with timed_sem:
            out = GetXML([pmid])
        with open(f,'w') as handle:
            handle.write(out)
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


    cachedir = os.path.abspath('cachedata')+os.sep

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

    timed_sem = TimedSemaphore(2, 3)
    for row in inter_list:
        for pmid in row['PubMed-ID'].split(','):
            key = (row['Gene-ID-2'], row['HIV-product-name'],
                   row['Interaction-short-phrase'], pmid)
            if key in known_set:
                continue

            print 'retrieving %s' % pmid
            xmldata = GetXMLData(pmid, cachedir, timed_sem)

            



































