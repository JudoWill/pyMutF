# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Sentence.ParNum'
        db.alter_column('Interaction_sentence', 'ParNum', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True))

        # Changing field 'Sentence.SentNum'
        db.alter_column('Interaction_sentence', 'SentNum', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True))

        # Changing field 'Mutation.Gene'
        db.alter_column('Interaction_mutation', 'Gene_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Interaction.Gene'], null=True, blank=True))


    def backwards(self, orm):
        
        # Changing field 'Sentence.ParNum'
        db.alter_column('Interaction_sentence', 'ParNum', self.gf('django.db.models.fields.IntegerField')(blank=True))

        # Changing field 'Sentence.SentNum'
        db.alter_column('Interaction_sentence', 'SentNum', self.gf('django.db.models.fields.IntegerField')(blank=True))

        # Changing field 'Mutation.Gene'
        db.alter_column('Interaction_mutation', 'Gene_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Interaction.Gene'], blank=True))


    models = {
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
