# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Data.ShouldLink'
        db.add_column('Queries_data', 'ShouldLink', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Data.ShouldLink'
        db.delete_column('Queries_data', 'ShouldLink')


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
            'ShouldLink': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
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
