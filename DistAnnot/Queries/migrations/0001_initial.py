# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'QueryRule'
        db.create_table('Queries_queryrule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Slug', self.gf('django.db.models.fields.SlugField')(max_length=256, db_index=True)),
            ('QueryRule', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('Queries', ['QueryRule'])

        # Adding M2M table for field Queries on 'QueryRule'
        db.create_table('Queries_queryrule_Queries', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('queryrule', models.ForeignKey(orm['Queries.queryrule'], null=False)),
            ('query', models.ForeignKey(orm['Queries.query'], null=False))
        ))
        db.create_unique('Queries_queryrule_Queries', ['queryrule_id', 'query_id'])

        # Adding M2M table for field Data on 'QueryRule'
        db.create_table('Queries_queryrule_Data', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('queryrule', models.ForeignKey(orm['Queries.queryrule'], null=False)),
            ('data', models.ForeignKey(orm['Queries.data'], null=False))
        ))
        db.create_unique('Queries_queryrule_Data', ['queryrule_id', 'data_id'])

        # Adding model 'Data'
        db.create_table('Queries_data', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('Queries', ['Data'])

        # Adding model 'Query'
        db.create_table('Queries_query', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('QueryText', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('DateAdded', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('LastChecked', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('Queries', ['Query'])

        # Adding M2M table for field DataObjects on 'Query'
        db.create_table('Queries_query_DataObjects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('query', models.ForeignKey(orm['Queries.query'], null=False)),
            ('data', models.ForeignKey(orm['Queries.data'], null=False))
        ))
        db.create_unique('Queries_query_DataObjects', ['query_id', 'data_id'])

        # Adding M2M table for field Articles on 'Query'
        db.create_table('Queries_query_Articles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('query', models.ForeignKey(orm['Queries.query'], null=False)),
            ('article', models.ForeignKey(orm['Interaction.article'], null=False))
        ))
        db.create_unique('Queries_query_Articles', ['query_id', 'article_id'])


    def backwards(self, orm):
        
        # Deleting model 'QueryRule'
        db.delete_table('Queries_queryrule')

        # Removing M2M table for field Queries on 'QueryRule'
        db.delete_table('Queries_queryrule_Queries')

        # Removing M2M table for field Data on 'QueryRule'
        db.delete_table('Queries_queryrule_Data')

        # Deleting model 'Data'
        db.delete_table('Queries_data')

        # Deleting model 'Query'
        db.delete_table('Queries_query')

        # Removing M2M table for field DataObjects on 'Query'
        db.delete_table('Queries_query_DataObjects')

        # Removing M2M table for field Articles on 'Query'
        db.delete_table('Queries_query_Articles')


    models = {
        'Interaction.article': {
            'HasMut': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'Article'},
            'PMCID': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'PMCXML': ('django.db.models.fields.XMLField', [], {'default': 'None', 'null': 'True'}),
            'PMID': ('django.db.models.fields.IntegerField', [], {}),
            'PubMedXML': ('django.db.models.fields.XMLField', [], {'default': 'None', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Queries.data': {
            'Meta': {'object_name': 'Data'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'Queries.query': {
            'Articles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Interaction.Article']", 'symmetrical': 'False'}),
            'DataObjects': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Queries.Data']", 'symmetrical': 'False'}),
            'DateAdded': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'LastChecked': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'Query'},
            'QueryText': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'Queries.queryrule': {
            'Data': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Queries.Data']", 'symmetrical': 'False'}),
            'Meta': {'object_name': 'QueryRule'},
            'Queries': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['Queries.Query']", 'symmetrical': 'False'}),
            'QueryRule': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'Slug': ('django.db.models.fields.SlugField', [], {'max_length': '256', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['Queries']
