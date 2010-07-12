# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MutationTags'
        db.create_table('Interaction_mutationtags', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Slug', self.gf('django.db.models.fields.SlugField')(max_length=50, db_index=True)),
            ('Description', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('Interaction', ['MutationTags'])

        # Adding M2M table for field Descriptions on 'Mutation'
        db.create_table('Interaction_mutation_Descriptions', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mutation', models.ForeignKey(orm['Interaction.mutation'], null=False)),
            ('mutationtags', models.ForeignKey(orm['Interaction.mutationtags'], null=False))
        ))
        db.create_unique('Interaction_mutation_Descriptions', ['mutation_id', 'mutationtags_id'])


    def backwards(self, orm):
        
        # Deleting model 'MutationTags'
        db.delete_table('Interaction_mutationtags')

        # Removing M2M table for field Descriptions on 'Mutation'
        db.delete_table('Interaction_mutation_Descriptions')


    models = {
        'Interaction.article': {
            'HasMut': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'Interactions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Interaction.Interaction']", 'symmetrical': 'False'}),
            'Meta': {'object_name': 'Article'},
            'PMCID': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'PMCXML': ('django.db.models.fields.XMLField', [], {'default': 'None', 'null': 'True'}),
            'PMID': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'PubMedXML': ('django.db.models.fields.XMLField', [], {'default': 'None', 'null': 'True'}),
            'Title': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
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
            'Descriptions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Interaction.MutationTags']", 'symmetrical': 'False'}),
            'Gene': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Interaction.Gene']", 'null': 'True', 'blank': 'True'}),
            'Interaction': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Interaction.Interaction']", 'through': "orm['Interaction.InteractionEffect']", 'symmetrical': 'False'}),
            'Meta': {'object_name': 'Mutation'},
            'Mut': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'Position': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Interaction.mutationtags': {
            'Description': ('django.db.models.fields.TextField', [], {}),
            'Meta': {'object_name': 'MutationTags'},
            'Slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Interaction.sentence': {
            'Article': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['Interaction.Article']", 'null': 'True'}),
            'Genes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Interaction.Gene']", 'through': "orm['Interaction.GeneAnnotation']", 'symmetrical': 'False'}),
            'Meta': {'object_name': 'Sentence'},
            'Mutation': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Interaction.Mutation']", 'symmetrical': 'False'}),
            'PMID': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'ParNum': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'Priority': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True'}),
            'RandOrder': ('django.db.models.fields.FloatField', [], {'default': 'None', 'null': 'True'}),
            'SentNum': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'Text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['Interaction']
