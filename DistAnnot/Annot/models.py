from django.db import models
from django.contrib.auth.models import User
from Interaction.models import Mutation, InteractionEffect, Gene

# Create your models here.
class MutationAnnot(models.Model):

    User = models.ForeignKey(User)
    Mutation = models.ForeignKey(Mutation)
    

class InteractionEffectAnnot(models.Model):

    User = models.ForeignKey(User)
    InteractionEffect = models.ForeignKey(InteractionEffect)
