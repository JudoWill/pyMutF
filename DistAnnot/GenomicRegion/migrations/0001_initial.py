# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Name'
        db.create_table('GenomicRegion_name', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('NameType', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['GenomicRegion.NameType'])),
        ))
        db.send_create_signal('GenomicRegion', ['Name'])

        # Adding model 'NameType'
        db.create_table('GenomicRegion_nametype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Type', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('GenomicRegion', ['NameType'])

        # Adding model 'Organism'
        db.create_table('GenomicRegion_organism', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('GenomicRegion', ['Organism'])

        # Adding M2M table for field Names on 'Organism'
        db.create_table('GenomicRegion_organism_Names', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('organism', models.ForeignKey(orm['GenomicRegion.organism'], null=False)),
            ('name', models.ForeignKey(orm['GenomicRegion.name'], null=False))
        ))
        db.create_unique('GenomicRegion_organism_Names', ['organism_id', 'name_id'])

        # Adding model 'Genome'
        db.create_table('GenomicRegion_genome', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Organism', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['GenomicRegion.Organism'])),
        ))
        db.send_create_signal('GenomicRegion', ['Genome'])

        # Adding M2M table for field Names on 'Genome'
        db.create_table('GenomicRegion_genome_Names', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('genome', models.ForeignKey(orm['GenomicRegion.genome'], null=False)),
            ('name', models.ForeignKey(orm['GenomicRegion.name'], null=False))
        ))
        db.create_unique('GenomicRegion_genome_Names', ['genome_id', 'name_id'])

        # Adding model 'Gene'
        db.create_table('GenomicRegion_gene', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('GenomicRegion', ['Gene'])

        # Adding M2M table for field Names on 'Gene'
        db.create_table('GenomicRegion_gene_Names', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('gene', models.ForeignKey(orm['GenomicRegion.gene'], null=False)),
            ('name', models.ForeignKey(orm['GenomicRegion.name'], null=False))
        ))
        db.create_unique('GenomicRegion_gene_Names', ['gene_id', 'name_id'])

        # Adding model 'Product'
        db.create_table('GenomicRegion_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('GenomicRegion', ['Product'])

        # Adding M2M table for field Names on 'Product'
        db.create_table('GenomicRegion_product_Names', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('product', models.ForeignKey(orm['GenomicRegion.product'], null=False)),
            ('name', models.ForeignKey(orm['GenomicRegion.name'], null=False))
        ))
        db.create_unique('GenomicRegion_product_Names', ['product_id', 'name_id'])

        # Adding model 'GeneLocation'
        db.create_table('GenomicRegion_genelocation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Start', self.gf('django.db.models.fields.IntegerField')()),
            ('Stop', self.gf('django.db.models.fields.IntegerField')()),
            ('Gene', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['GenomicRegion.Gene'])),
            ('Genome', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['GenomicRegion.Genome'])),
        ))
        db.send_create_signal('GenomicRegion', ['GeneLocation'])

        # Adding model 'ProductLocation'
        db.create_table('GenomicRegion_productlocation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['GenomicRegion.Product'])),
            ('Gene', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['GenomicRegion.Gene'])),
        ))
        db.send_create_signal('GenomicRegion', ['ProductLocation'])


    def backwards(self, orm):
        
        # Deleting model 'Name'
        db.delete_table('GenomicRegion_name')

        # Deleting model 'NameType'
        db.delete_table('GenomicRegion_nametype')

        # Deleting model 'Organism'
        db.delete_table('GenomicRegion_organism')

        # Removing M2M table for field Names on 'Organism'
        db.delete_table('GenomicRegion_organism_Names')

        # Deleting model 'Genome'
        db.delete_table('GenomicRegion_genome')

        # Removing M2M table for field Names on 'Genome'
        db.delete_table('GenomicRegion_genome_Names')

        # Deleting model 'Gene'
        db.delete_table('GenomicRegion_gene')

        # Removing M2M table for field Names on 'Gene'
        db.delete_table('GenomicRegion_gene_Names')

        # Deleting model 'Product'
        db.delete_table('GenomicRegion_product')

        # Removing M2M table for field Names on 'Product'
        db.delete_table('GenomicRegion_product_Names')

        # Deleting model 'GeneLocation'
        db.delete_table('GenomicRegion_genelocation')

        # Deleting model 'ProductLocation'
        db.delete_table('GenomicRegion_productlocation')


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
