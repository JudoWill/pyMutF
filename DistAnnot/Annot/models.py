from django.db import models
from django.contrib.auth.models import User
from DistAnnot.Interaction.models import Mutation, InteractionEffect, Gene, EffectType

# Create your models here.
class MutationAnnot(models.Model):

    User = models.ForeignKey(User)
    Mutation = models.ForeignKey(Mutation)
    GeneChosen = models.ForeignKey(Gene)

    def update_link(self):
        self.Mutation.Gene = self.GeneChosen

class InteractionEffectAnnot(models.Model):

    User = models.ForeignKey(User)
    InteractionEffect = models.ForeignKey(InteractionEffect)
    EffectChosen = models.ForeignKey(EffectType)

    def update_link(self):
        self.InteractionEffect.Gene = self.EffectChosen