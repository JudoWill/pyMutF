# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'NameType.is_required'
        db.delete_column('GenomicRegion_nametype', 'is_required')

        # Adding field 'NameType.Slug'
        db.add_column('GenomicRegion_nametype', 'Slug', self.gf('django.db.models.fields.SlugField')(default='default-value', max_length=255, db_index=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'NameType.is_required'
        db.add_column('GenomicRegion_nametype', 'is_required', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True), keep_default=False)

        # Deleting field 'NameType.Slug'
        db.delete_column('GenomicRegion_nametype', 'Slug')


    models = {
        'GenomicRegion.gene': {
            'Genome': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['GenomicRegion.Genome']", 'through': "orm['GenomicRegion.GeneLocation']", 'symmetrical': 'False'}),
            'Meta': {'object_name': 'Gene'},
            'Names': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['GenomicRegion.Name']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'GenomicRegion.genelocation': {
            'Gene': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['GenomicRegion.Gene']"}),
            'Genome': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['GenomicRegion.Genome']"}),
            'Meta': {'object_name': 'GeneLocation'},
            'Start': ('django.db.models.fields.IntegerField', [], {}),
            'Stop': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'GenomicRegion.genome': {
            'Meta': {'object_name': 'Genome'},
            'Names': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['GenomicRegion.Name']", 'symmetrical': 'False'}),
            'Organism': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['GenomicRegion.Organism']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'GenomicRegion.name': {
            'Meta': {'object_name': 'Name'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'NameType': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['GenomicRegion.NameType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'GenomicRegion.nametype': {
            'Meta': {'object_name': 'NameType'},
            'Slug': ('django.db.models.fields.SlugField', [], {'max_length': '255', 'db_index': 'True'}),
            'Type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'GenomicRegion.organism': {
            'Meta': {'object_name': 'Organism'},
            'Names': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['GenomicRegion.Name']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'GenomicRegion.product': {
            'Gene': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['GenomicRegion.Gene']", 'through': "orm['GenomicRegion.ProductLocation']", 'symmetrical': 'False'}),
            'Meta': {'object_name': 'Product'},
            'Names': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['GenomicRegion.Name']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'GenomicRegion.productlocation': {
            'Gene': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['GenomicRegion.Gene']"}),
            'Meta': {'object_name': 'ProductLocation'},
            'Product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['GenomicRegion.Product']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['GenomicRegion']
