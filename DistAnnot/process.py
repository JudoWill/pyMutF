from __future__ import with_statement
import csv, os
import os.path
from PubmedUtils import *
from threading import Semaphore, Timer
from BeautifulSoup import BeautifulStoneSoup
from mutation_finder import *

from nltk.tokenize import sent_tokenize
from itertools import count, izip

import django.db.transaction
#from django.conf import settings
#import DistAnnot.settings

#settings.configure(default_settings = DistAnnot.settings)
from Interaction.models import Gene, Sentence, Interaction, InteractionType, Mutation

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

@django.db.transaction.commit_on_success
def AddGenesToDB(INTER_LIST):
    """Add genes from the interaction list into the database"""

    for row in INTER_LIST:
        
        t = {'Organism':'HIV', 'Name':row['HIV-product-name']}
        Gene.objects.get_or_create(Entrez = int(row['Gene-ID-1']), defaults = t)
        t = {'Organism':'Human', 'Name': row['Human-product-name']}
        Gene.objects.get_or_create(Entrez = int(row['Gene-ID-2']), defaults = t)

@django.db.transaction.commit_on_success
def AddArticleToDB(ParGen, MutFinder, PMID, interaction):
    """Add sentences into the database"""



    for par, parnum in izip(ParGen, count(0)):
        for sent, sentnum in izip(sent_tokenize(par), count(0)):
            for mut, loc in mutFinder(par).items():
                obj, isnew = Sentence.objects.get_or_create(PMID = PMID,
                                                        ParNum = parnum,
                                                        SentNum = sentnum,
                                                        Interactions = interaction,
                                                        defaults = {'Text':sent})
                qset = obj.Mutation.filter(Mut = mut)
                if not qset.exists():
                    mut_obj = Mutation.objects.create(Mut = mut)
                    obj.Mutation.add(mut_obj)







if __name__ == '__main__':
    cachedir = os.sep + os.path.join('home', 'will', 'pyMutF',
                                     'cachedata') + os.sep

    with open('hiv_interactions') as handle:
        inter_list = list(csv.DictReader(handle, delimiter='\t'))

    print 'Adding Genes'
    #AddGenesToDB(inter_list)




    pmid_pmc = {}
    with open('PMC-ids.csv') as handle:
        for row in csv.DictReader(handle):
            pmid_pmc[row['PMID']] = row['PMCID']



    mutFinder = mutation_finder_from_regex_filepath('regex.txt')
    EUtilsSem = TimedSemaphore(2, 3)

    for row in inter_list:

        hiv_gene = Gene.objects.get(Entrez = int(row['Gene-ID-1']))
        human_gene = Gene.objects.get(Entrez = int(row['Gene-ID-2']))
        r, isnew = InteractionType.objects.get_or_create(Type=row['Interaction-short-phrase'])
        inter, isnew = Interaction.objects.get_or_create(HIVGene = hiv_gene,
                                                         HumanGene = human_gene,
                                                         InteractionType = r)

        for pmid in row['PubMed-ID'].split(','):
            



            print 'retrieving %s' % pmid
            if pmid in pmid_pmc:
                print 'getting PMC'
                xmldata = GetXMLData(pmid_pmc[pmid], cachedir, EUtilsSem,
                                     db='pmc')
                pargen = ExtractPMCPar(xmldata)
            else:
                xmldata = GetXMLData(pmid, cachedir, EUtilsSem)
                pargen = ExtractPubPar(xmldata)

            AddArticleToDB(pargen, mutFinder, pmid, inter)






































