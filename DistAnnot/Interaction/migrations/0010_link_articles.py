# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
import DistAnnot.Interaction.models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        for sent in DistAnnot.Interaction.models.Sentence.objects.all():
            art, isnew = DistAnnot.Interaction.models.Article.objects.get_or_create(PMID = sent.PMID)
            sent.Article = art
            sent.save()

    def backwards(self, orm):
        "Write your backwards methods here."
        pass

    models = {
        'Interaction.article': {
            'Meta': {'object_name': 'Article'},
            'PMCID': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'PMID': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Interaction.gene': {
            'Entrez': ('django.db.models.fields.IntegerField', [], {}),
            'Meta': {'object_name': 'Gene'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'Organism': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Interaction.interaction': {
            'HIVGene': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'HIVPartner'", 'to': "orm['Interaction.Gene']"}),
            'HumanGene': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'HumanPartner'", 'to': "orm['Interaction.Gene']"}),
            'InteractionType': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Interaction.InteractionType']"}),
            'Meta': {'object_name': 'Interaction'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Interaction.interactioneffect': {
            'Interaction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Interaction.Interaction']"}),
            'Meta': {'object_name': 'InteractionEffect'},
            'Mutation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Interaction.Mutation']"}),
            'Type': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Interaction.interactiontype': {
            'Meta': {'object_name': 'InteractionType'},
            'Type': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Interaction.mutation': {
            'Gene': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Interaction.Gene']", 'null': 'True', 'blank': 'True'}),
            'Interaction': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Interaction.Interaction']", 'through': "orm['Interaction.InteractionEffect']", 'symmetrical': 'False'}),
            'Meta': {'object_name': 'Mutation'},
            'Mut': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Interaction.sentence': {
            'Article': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['Interaction.Article']", 'null': 'True'}),
            'Genes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Interaction.Gene']", 'symmetrical': 'False'}),
            'Interactions': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Interaction.Interaction']"}),
            'Meta': {'object_name': 'Sentence'},
            'Mutation': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Interaction.Mutation']", 'symmetrical': 'False'}),
            'PMID': ('django.db.models.fields.IntegerField', [], {}),
            'ParNum': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'SentNum': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'Text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['Interaction']
