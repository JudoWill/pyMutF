from DistAnnot.Interaction.models import *
from csv import DictReader, DictWriter
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


def dump_muts(file_name):
    fnames = ('Mut', 'Gene-Entrez', 'Description', 'PMID')
    with open(file_name, 'w') as handle:
        handle.write(','.join(fnames) + '\n')
        writer = DictWriter(handle, fnames)
        for ref in Reference.objects.all():
            writer.writerow({
                            'Mut':ref.Mutation.Mut,
                            'Description':ref.Tag.Slug,
                            'PMID':ref.Article.PMID,
                            'Gene-Entrez':ref.Mutation.Gene.Entrez
                            })


def load_muts(file_name):

    with open(file_name) as handle:
        for row in DictReader(handle):
            try:
                mut = Mutation.objects.get(Mut = row['Mut'],
                                           Gene__Entrez = int(row['Mut']))
            except ObjectDoesNotExist:
                continue

            tag = MutationTags.objects.get_or_create(Slug = row['Description'])

            try:
                art = Article.objects.get(PMID = int(row['PMID']))
            except ObjectDoesNotExist:
                continue

            try:
                gene = Gene.objects.get(Entrez = int(row['Gene-Entrez']))
            except MultipleObjectsReturned:
                gene = Gene.objects.filter(Entrez = int(row['Gene-Entrez']))[0]
            except ObjectDoesNotExist:
                continue

            obj, isnew = Reference.objects.get_or_create(Article = art,
                                                         Mutation = mut,
                                                         Tag = tag)





if __name__ == '__main__':
    pass