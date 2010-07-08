from DistAnnot.Interaction.models import *
from itertools import groupby
from operator import attrgetter


def main():

    qset = Mutation.objects.order_by('Mut', 'Gene')
    for mut_id, MutIter in groupby(qset, attrgetter('Mut')):
        for gene_id, gene_iter in groupby(MutIter, attrgetter('Gene')):
            if gene_id is None:
                continue
            gene_list = list(gene_iter)
            if len(gene_list) > 1:
                print 'joining %s' % gene_id
                gene_list[0].JoinMuts(*gene_list[1:])






if __name__ == '__main__':
    main()