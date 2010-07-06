from DistAnnot.Interaction.models import *
import random




def main():


    

    for num, sent in enumerate(Sentence.objects.all().select_related('Mutation').iterator()):
        print num
        pri = max(10-sent.Mutation.filter(Gene__isnull = True).count(), 1)
        
        sent.Priority = pri if pri != 10 else None
        sent.RandOrder = random.random()
        sent.save()





if __name__ == '__main__':
    main()