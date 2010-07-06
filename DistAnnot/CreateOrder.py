from DistAnnot.Interaction.models import *
import random





def UpdatePriority(sentence):
    pri = max(10-sentence.Mutation.filter(Gene__isnull = True).count(), 1)

    sentence.Priority = pri if pri != 10 else None
    sentence.RandOrder = random.random()
    sentence.save()




def main():


    

    for num, sent in enumerate(Sentence.objects.all().select_related('Mutation').iterator()):
        print num
        UpdatePriority(sent)





if __name__ == '__main__':
    main()