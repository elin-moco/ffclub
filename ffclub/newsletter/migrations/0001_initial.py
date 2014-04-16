# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Newsletter'
        db.create_table('newsletter_newsletter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('issue', self.gf('django.db.models.fields.DateField')()),
            ('volume', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('publish_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('newsletter', ['Newsletter'])

        # Adding model 'Subscription'
        db.create_table('newsletter_subscription', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.TextField')(db_column='u_email')),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1, db_column='u_status')),
            ('edit_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('newsletter', ['Subscription'])

        # Adding model 'Metadata'
        db.create_table('newsletter_metadata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='string', max_length=20)),
            ('index', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='metadata', to=orm['newsletter.Newsletter'])),
        ))
        db.send_create_signal('newsletter', ['Metadata'])

        # Adding model 'MetaString'
        db.create_table('newsletter_metastring', (
            ('metadata_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['newsletter.Metadata'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
        ))
        db.send_create_signal('newsletter', ['MetaString'])

        # Adding model 'MetaNumber'
        db.create_table('newsletter_metanumber', (
            ('metadata_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['newsletter.Metadata'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.FloatField')(default=0.0)),
        ))
        db.send_create_signal('newsletter', ['MetaNumber'])

        # Adding model 'MetaDatetime'
        db.create_table('newsletter_metadatetime', (
            ('metadata_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['newsletter.Metadata'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('newsletter', ['MetaDatetime'])

        # Adding model 'MetaFile'
        db.create_table('newsletter_metafile', (
            ('metadata_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['newsletter.Metadata'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.files.FileField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal('newsletter', ['MetaFile'])


    def backwards(self, orm):
        # Deleting model 'Newsletter'
        db.delete_table('newsletter_newsletter')

        # Deleting model 'Subscription'
        db.delete_table('newsletter_subscription')

        # Deleting model 'Metadata'
        db.delete_table('newsletter_metadata')

        # Deleting model 'MetaString'
        db.delete_table('newsletter_metastring')

        # Deleting model 'MetaNumber'
        db.delete_table('newsletter_metanumber')

        # Deleting model 'MetaDatetime'
        db.delete_table('newsletter_metadatetime')

        # Deleting model 'MetaFile'
        db.delete_table('newsletter_metafile')


    models = {
        'newsletter.metadata': {
            'Meta': {'object_name': 'Metadata'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'metadata'", 'to': "orm['newsletter.Newsletter']"}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'string'", 'max_length': '20'})
        },
        'newsletter.metadatetime': {
            'Meta': {'object_name': 'MetaDatetime', '_ormbases': ['newsletter.Metadata']},
            'metadata_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsletter.Metadata']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'newsletter.metafile': {
            'Meta': {'object_name': 'MetaFile', '_ormbases': ['newsletter.Metadata']},
            'metadata_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsletter.Metadata']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.files.FileField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'newsletter.metanumber': {
            'Meta': {'object_name': 'MetaNumber', '_ormbases': ['newsletter.Metadata']},
            'metadata_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsletter.Metadata']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {'default': '0.0'})
        },
        'newsletter.metastring': {
            'Meta': {'object_name': 'MetaString', '_ormbases': ['newsletter.Metadata']},
            'metadata_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['newsletter.Metadata']", 'unique': 'True', 'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        'newsletter.newsletter': {
            'Meta': {'object_name': 'Newsletter'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.DateField', [], {}),
            'publish_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'volume': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'newsletter.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'edit_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.TextField', [], {'db_column': "'u_email'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1', 'db_column': "'u_status'"})
        }
    }

    complete_apps = ['newsletter']