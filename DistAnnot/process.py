from __future__ import with_statement
import csv, os
import os.path
from PubmedUtils import *
from threading import Semaphore, Timer
from BeautifulSoup import BeautifulStoneSoup
from mutation_finder import *
from collections import defaultdict

from nltk.tokenize import sent_tokenize
from itertools import count, izip

import django.db.transaction
#from django.conf import settings
#import DistAnnot.settings

#settings.configure(default_settings = DistAnnot.settings)
from Interaction.models import *

def GetXMLData(pmid, cachedir, timed_sem, db='pubmed', use_cache=True):
    """Get an XML document either from the cache-directory or download it from Pubmed"""

    f = os.path.join(cachedir, pmid + '.xml')
    if os.path.exists(f) and use_cache:
        return open(f).read()
    else:
        with timed_sem:
            out = GetXML([pmid], db=db)
        if len(out) < 10:
            return False
        try:
            with open(f, 'w') as handle:
                tree = BeautifulStoneSoup(out)
                if tree is not None:
                    handle.write(tree.prettyify())
                else:
                    return False
            return out
        except TypeError:
            print 'bad getting with %s' % pmid
            return False

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
def AddGeneNames(Fname):
    
    namedict = defaultdict(list)
    with open(Fname) as handle:
        for row in csv.DictReader(handle, delimiter = '\t'):
            namedict[int(row['GeneID'])].append(row['Symbol'])
    for gene in Gene.objects.all():
        for name in namedict[gene.Entrez]:
            ex, isnew = ExtraGeneName.objects.get_or_create(Name = name)
            gene.ExtraNames.add(ex)
            

@django.db.transaction.commit_on_success
def AddArticleToDB(ParGen, MutFinder, article, interaction):
    """Add sentences into the database"""

    def JoinSent(sent_list, ind):
        if ind == 0:
            return sent_list[ind]+sent_list[ind+1]
        elif ind == len(sent_list)-1:
            return sent_list[ind-1]+sent_list[ind]
        else:
            
            return ' '.join(sent_list[ind-1:ind+1])


    for par, parnum in izip(ParGen, count(0)):
        sent_list = list(sent_tokenize(par))

        for sent, sentnum in izip(sent_list, count(0)):
            for mut, loc in MutFinder(par).items():
                obj, isnew = Sentence.objects.get_or_create(Article = article,
                                                ParNum = parnum,
                                                SentNum = sentnum,
                                                defaults = {'Text':JoinSent(sent_list, sentnum)})
                obj.Interactions.add(interaction)

                qset = obj.Mutation.filter(Mut = mut)
                if not qset.exists() and mut is not None and isnew:
                    mut_obj = Mutation.objects.create(Mut = mut)
                    obj.Mutation.add(mut_obj)


def main():
    cachedir = os.sep + os.path.join('home', 'will', 'pyMutF',
                                     'cachedata') + os.sep
    cachedir = os.sep + os.path.join('Users', 'will', 'pyMutF', 'cachedata') + os.sep

    with open('hiv_interactions') as handle:
        inter_list = list(csv.DictReader(handle, delimiter='\t'))

    print 'Adding Genes'
    AddGenesToDB(inter_list)
    
    print 'Adding ExtraNames'
    AddGeneNames('gene_info_human')



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
            article, isnew = Article.objects.get_or_create(PMID = int(pmid))
            if not Sentence.objects.filter(Interactions = inter,
                                           Article = article).exists():


                print 'retrieving %s' % pmid
                if pmid in pmid_pmc:
                    print 'getting PMC'
                    article.PMCID = pmid_pmc[pmid]
                    article.save()
                    xmldata = GetXMLData(pmid_pmc[pmid], cachedir, EUtilsSem,
                                         db='pmc')
                    if xmldata:
                        pargen = ExtractPMCPar(xmldata)
                    else:
                        continue
                else:
                    xmldata = GetXMLData(pmid, cachedir, EUtilsSem)
                    if xmldata:
                        pargen = ExtractPubPar(xmldata)
                    else:
                        continue

                AddArticleToDB(pargen, mutFinder, article, inter)
            else:
                print 'Aldready wrote: %s'  % pmid




if __name__ == '__main__':
    main()
































