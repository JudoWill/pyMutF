from django.forms import ModelForm
from DistAnnot.Annot.models import MutationAnnot


class MutationAnnotForm(ModelForm):
    class Meta:
        model =  MutationAnnot

        