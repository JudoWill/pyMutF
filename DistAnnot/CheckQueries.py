from DistAnnot.Queries.models import *
from DistAnnot.Interaction.models import *
from PubmedUtils import *
from django.core.exceptions import MultipleObjectsReturned

from collections import defaultdict
from itertools import izip, count
import csv

import django.db.transaction
import nltk.tokenize
import datetime
import DistAnnot.mutation_finder
import DistAnnot.PubmedUtils
import DistAnnot.process


@django.db.transaction.commit_on_success
def AddQuery(obj_dict):

    qrule, isnew = QueryRule.objects.get_or_create(Slug = obj_dict['Slug'],
                                                 QueryRule = obj_dict['Text'])
    if isnew:
        for key, val in obj_dict['data'].items():
            for obj in val:
                ctype = ContentType.objects.get_for_model(obj)
                d, isn = Data.objects.get_or_create(identifier = key, object_id = obj.id,
                                                    content_type = ctype,
                                                    ShouldLink = obj_dict['ShouldLink'])
                if isn:
                    qrule.Data.add(d)


@django.db.transaction.commit_on_success
def CreateQueries(rule):
    print 'rule', rule
    for q, data_list in rule.YieldQueries():
        query, isnew = Query.objects.get_or_create(QueryText = q)
        if isnew:
            for data in data_list:
                query.DataObjects.add(data)

@django.db.transaction.commit_on_success
def DoQuery(rule, pmid_pmc, semaphore, MutFinder):

    with semaphore:
        pmids = rule.DoQuery(USE_RECENT = False)

    rule.LastChecked = datetime.datetime.now()
    rule.save()
    print rule, len(pmids)

    for pmid in pmids:

        try:
            art, isnew = Article.objects.get_or_create(PMID = pmid,
                                                   defaults = {'PMCID': pmid_pmc[pmid]})
        except MultipleObjectsReturned:
            art = Article.objects.filter(PMID = pmid)[0]
            isnew = False
                                        

        if isnew or art.HasMut is None:
            print 'new or unannotated article: ', pmid


        rule.Articles.add(art)
        with semaphore:
            art.ReadMuts(MutFinder = MutFinder)


def GetParGen(article):
    pargen = None
    if article.HasMut is None or article.HasMut:
        try:
            if article.PMCID is not None:
                xml = article.GetPMCXML()
                if xml:
                    pargen = DistAnnot.PubmedUtils.ExtractPMCPar(xml)

            elif article.PMID is not None:
                xml = article.GetPubMedXML()
                if xml:
                    pargen = DistAnnot.PubmedUtils.ExtractPubPar(xml)
            print 'good pargen'
        except:
            print 'got error: ', article.PMID
            article.HasMut = None
            article.save()

    else:
        print 'skipping because None'

    return pargen

@django.db.transaction.commit_on_success
def AddArticleToDB(ParGen, MutFinder, article):
    """Add sentences into the database"""



    article.HasMut = False
    for par, parnum in izip(ParGen, count(0)):
        sent_list = ['']+list(nltk.tokenize.sent_tokenize(par))+['']

        for sentnum, sent in enumerate(sent_list):
            for mut in MutFinder(sent).keys():
                print 'Found mut!'
                article.HasMut = True
                text = ' '.join(sent_list[sentnum-1:sentnum+1])
                obj, isnew = Sentence.objects.get_or_create(Article = article,
                                                ParNum = parnum,
                                                SentNum = sentnum,
                                                defaults = {'Text':text})


                qset = obj.Mutation.filter(Mut = mut)
                if not qset.exists() and mut is not None and isnew:
                    mut_obj = Mutation(Mut = mut)
                    obj.Mutation.add(mut_obj)
    article.save()




def main():
    global_queries = [{'Text':'%(inter)s+HIV',
                        'data':{'inter': Interaction.objects.all()},
                        'Slug': 'HIV-interaction',
                        'ShouldLink':True},
                      {'Text': 'HIV+%(hiv_gene)s+mutation',
                        'data': {'hiv_gene': Gene.objects.filter(Organism='HIV')},
                        'Slug': 'HIV-gene-search',
                        'ShouldLink':True},
                      { 'Text':'HIV+mutation+%(human_gene)s',
                        'data': {'human_gene': Gene.objects.filter(Organism='HIV')},
                        'Slug': 'human-mutation-search',
                        'ShouldLink':True}
                      ]



    MutFinder = DistAnnot.mutation_finder.mutation_finder_from_regex_filepath('regex.txt')
    EUtilsSem = DistAnnot.process.TimedSemaphore(2, 3)

    print 'Making Rules'
    #for obj_dict in global_queries:
    #    AddQuery(obj_dict)

    print 'Making Indiv Queries'
    #for rule in QueryRule.objects.all():
    #    CreateQueries(rule)

    print 'Reading pmc_conv'
    pmid_pmc = defaultdict(lambda : None)
    with open('PMC-ids.csv') as handle:
        for row in csv.DictReader(handle):
            pmid_pmc[row['PMID']] = row['PMCID']

    print 'Doing actual queries'
    for query in Query.objects.filter(LastChecked__isnull = True).order_by('-DateAdded'):
        try:
            DoQuery(query, pmid_pmc, EUtilsSem, MutFinder)
        except:
            pass


if __name__ == '__main__':
    main()