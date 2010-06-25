# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Deleting field 'Sentence.Interactions'
        db.delete_column('Interaction_sentence', 'Interactions_id')

        # Adding M2M table for field Interactions on 'Sentence'
        db.create_table('Interaction_sentence_Interactions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sentence', models.ForeignKey(orm['Interaction.sentence'], null=False)),
            ('interaction', models.ForeignKey(orm['Interaction.interaction'], null=False))
        ))
        db.create_unique('Interaction_sentence_Interactions', ['sentence_id', 'interaction_id'])
    
    
    def backwards(self, orm):
        
        # Adding field 'Sentence.Interactions'
        db.add_column('Interaction_sentence', 'Interactions', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['Interaction.Interaction']), keep_default=False)

        # Removing M2M table for field Interactions on 'Sentence'
        db.delete_table('Interaction_sentence_Interactions')
    
    
    models = {
        'Interaction.article': {
            'Meta': {'object_name': 'Article'},
            'PMCID': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'PMID': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Interaction.effecttype': {
            'Description': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'Meta': {'object_name': 'EffectType'},
            'Slug': ('django.db.models.fields.SlugField', [], {'max_length': '256', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Interaction.extragenename': {
            'Meta': {'object_name': 'ExtraGeneName'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Interaction.gene': {
            'Entrez': ('django.db.models.fields.IntegerField', [], {}),
            'ExtraNames': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Interaction.ExtraGeneName']", 'symmetrical': 'False'}),
            'Meta': {'object_name': 'Gene'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'Organism': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Interaction.geneannotation': {
            'Gene': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Interaction.Gene']"}),
            'Meta': {'object_name': 'GeneAnnotation'},
            'Sentence': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Interaction.Sentence']"}),
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
            'EffectType': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Interaction.EffectType']", 'null': 'True'}),
            'Interaction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Interaction.Interaction']"}),
            'Meta': {'object_name': 'InteractionEffect'},
            'Mutation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Interaction.Mutation']"}),
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
            'Genes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Interaction.Gene']", 'through': "orm['Interaction.GeneAnnotation']", 'symmetrical': 'False'}),
            'Interactions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Interaction.Interaction']", 'symmetrical': 'False'}),
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
