from __future__ import with_statement
import csv, os
import os.path
from PubmedUtils import *
from threading import Semaphore, Timer
from BeautifulSoup import BeautifulStoneSoup
from mutation_finder import *
from collections import defaultdict

from nltk.tokenize import sent_tokenize
from itertools import count, izip, groupby

from django.core.exceptions import MultipleObjectsReturned

import django.db.transaction
#from django.conf import settings
#import DistAnnot.settings

#settings.configure(default_settings = DistAnnot.settings)
from Interaction.models import *

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
        
        t = {'Organism':'HIV', 'Name': row['HIV-product-name']}
        try:
            obj, isnew = Gene.objects.get_or_create(Entrez = int(row['Gene-ID-1']), defaults = t)
        except MultipleObjectsReturned:
            obj = Gene.objects.filter(Entrez = int(row['Gene-ID-1']))[0]
            isnew = False

        if obj.Name != t['Name']:
            try:
                ex, isnew = ExtraGeneName.objects.get_or_create(Name = t['Name'])
                obj.ExtraNames.add(ex)
            except MultipleObjectsReturned:
                pass


        t = {'Organism':'Human', 'Name': row['Human-product-name']}
        try:
            Gene.objects.get_or_create(Entrez = int(row['Gene-ID-2']), defaults = t)
        except:
            pass

@django.db.transaction.commit_on_success
def AddGeneNames(Fname):
    
    namedict = defaultdict(list)
    with open(Fname) as handle:
        for row in csv.DictReader(handle, delimiter = '\t'):
            namedict[int(row['GeneID'])].append(row['Symbol'])
    for gene in Gene.objects.all():
        for name in namedict[gene.Entrez]:
            try:
                ex, isnew = ExtraGeneName.objects.get_or_create(Name = name)
            except MultipleObjectsReturned:
                continue
            gene.ExtraNames.add(ex)

@django.db.transaction.commit_on_success
def AddAllNames(Fname):
    with open(Fname) as handle:
        rowgen = csv.DictReader(handle, delimiter = '\t')
        for key, rows in groupby(rowgen, lambda x: x['GeneID']):
            try:
                gene, isnew = Gene.objects.get_or_create(Entrez = int(key))
            except MultipleObjectsReturned:
                continue
            if isnew:
                gene.Organism = 'Human'
                gene.Name = rows.next()['Symbol']
                for row in rows:
                    try:
                        ex, isnew = ExtraGeneName.objects.get_or_create(Name = row['Symbol'])
                    except MultipleObjectsReturned:
                        continue
                    if isnew:
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

    article.HasMut = False
    for par, parnum in izip(ParGen, count(0)):
        sent_list = ['']+list(sent_tokenize(par))+['']

        for sentnum, sent in enumerate(sent_list):
            for mut, loc in MutFinder(sent).items():
                print 'Found Mut!!'
                article.HasMut = True
                text = ' '.join(sent_list[sentnum-1:sentnum+1])
                obj, isnew = Sentence.objects.get_or_create(Article = article,
                                                ParNum = parnum,
                                                SentNum = sentnum,
                                                defaults = {'Text':text})
                obj.Article.Interactions.add(interaction)

                qset = obj.Mutation.filter(Mut = mut)
                if not qset.exists() and mut is not None and isnew:
                    mut_obj = Mutation.objects.create(Mut = mut)
                    obj.Mutation.add(mut_obj)
    article.save()

def main():

    with open('hiv_interactions') as handle:
        inter_list = list(csv.DictReader(handle, delimiter='\t'))

    print 'Adding Genes'
    #AddGenesToDB(inter_list)

    print 'Adding ExtraNames'
    #AddGeneNames('gene_info_human')



    pmid_pmc = defaultdict(lambda : None)
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
            article, isnew = Article.objects.get_or_create(PMID = int(pmid),
                                                    PMCID = pmid_pmc[pmid])
            
            if article.HasMut is None:
                article.HasMut = False
                article.save()
                xml = None
                pargen = None
                print 'Processing: %s' % pmid
                #try:
                if article.PMCID is not None:
                    xml = article.GetPMCXML()
                    if xml:
                        pargen = ExtractPMCPar(xml)

                elif article.PMID is not None:
                    xml = article.GetPubMedXML()
                    if xml:
                        pargen = ExtractPubPar(xml)
                if pargen:
                    AddArticleToDB(pargen, mutFinder, article, inter)
                #except:
                #    print 'got error: ', article.PMID
                #    article.HasMut = None
                #    article.save()
                #    continue
            elif article.HasMut:
                print 'Already processed'
                article.Interactions.add(inter)
            else:
                print 'Aldready wrote: %s'  % pmid




if __name__ == '__main__':
    main()
































