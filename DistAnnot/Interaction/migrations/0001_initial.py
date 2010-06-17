# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Sentence'
        db.create_table('Interaction_sentence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Text', self.gf('django.db.models.fields.TextField')()),
            ('PMID', self.gf('django.db.models.fields.IntegerField')()),
            ('Interactions', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Interaction.Interaction'])),
        ))
        db.send_create_signal('Interaction', ['Sentence'])

        # Adding model 'Interaction'
        db.create_table('Interaction_interaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('HIVGene', self.gf('django.db.models.fields.related.ForeignKey')(related_name='HIVPartner', to=orm['Interaction.Gene'])),
            ('HumanGene', self.gf('django.db.models.fields.related.ForeignKey')(related_name='HumanPartner', to=orm['Interaction.Gene'])),
            ('InteractionType', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Interaction.InteractionType'])),
        ))
        db.send_create_signal('Interaction', ['Interaction'])

        # Adding model 'Mutation'
        db.create_table('Interaction_mutation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Mut', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('Gene', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Interaction.Gene'])),
        ))
        db.send_create_signal('Interaction', ['Mutation'])

        # Adding model 'InteractionEffect'
        db.create_table('Interaction_interactioneffect', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Interaction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Interaction.Interaction'])),
            ('Mutation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['Interaction.Mutation'])),
            ('Type', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('Interaction', ['InteractionEffect'])

        # Adding model 'Gene'
        db.create_table('Interaction_gene', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Organism', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('Name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('Entrez', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('Interaction', ['Gene'])

        # Adding model 'InteractionType'
        db.create_table('Interaction_interactiontype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Type', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('Interaction', ['InteractionType'])


    def backwards(self, orm):
        
        # Deleting model 'Sentence'
        db.delete_table('Interaction_sentence')

        # Deleting model 'Interaction'
        db.delete_table('Interaction_interaction')

        # Deleting model 'Mutation'
        db.delete_table('Interaction_mutation')

        # Deleting model 'InteractionEffect'
        db.delete_table('Interaction_interactioneffect')

        # Deleting model 'Gene'
        db.delete_table('Interaction_gene')

        # Deleting model 'InteractionType'
        db.delete_table('Interaction_interactiontype')


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
            'Gene': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Interaction.Gene']"}),
            'Interaction': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Interaction.Interaction']", 'through': "orm['Interaction.InteractionEffect']", 'symmetrical': 'False'}),
            'Meta': {'object_name': 'Mutation'},
            'Mut': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Interaction.sentence': {
            'Interactions': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['Interaction.Interaction']"}),
            'Meta': {'object_name': 'Sentence'},
            'PMID': ('django.db.models.fields.IntegerField', [], {}),
            'Text': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['Interaction']
