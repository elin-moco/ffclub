# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MetaString'
        db.create_table('newsletter_metastring', (
            ('metadata_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['newsletter.Metadata'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
        ))
        db.send_create_signal('newsletter', ['MetaString'])

        # Adding model 'MetaFile'
        db.create_table('newsletter_metafile', (
            ('metadata_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['newsletter.Metadata'], unique=True, primary_key=True)),
            ('value', self.gf('django.db.models.fields.files.FileField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal('newsletter', ['MetaFile'])

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

        # Adding model 'Metadata'
        db.create_table('newsletter_metadata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='string', max_length=20)),
            ('index', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('create_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='metadata', to=orm['newsletter.Newsletter'])),
        ))
        db.send_create_signal('newsletter', ['Metadata'])


    def backwards(self, orm):
        # Deleting model 'MetaString'
        db.delete_table('newsletter_metastring')

        # Deleting model 'MetaFile'
        db.delete_table('newsletter_metafile')

        # Deleting model 'MetaNumber'
        db.delete_table('newsletter_metanumber')

        # Deleting model 'MetaDatetime'
        db.delete_table('newsletter_metadatetime')

        # Deleting model 'Metadata'
        db.delete_table('newsletter_metadata')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'newsletter.metadata': {
            'Meta': {'object_name': 'Metadata'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'create_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"}),
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
            'Meta': {'object_name': 'Newsletter', 'db_table': "u'issue'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.DateField', [], {}),
            'publish_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'volume': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'newsletter.subscription': {
            'Meta': {'object_name': 'Subscription', 'db_table': "u'newsletter'"},
            'edit_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.TextField', [], {'db_column': "'u_email'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1', 'db_column': "'u_status'"})
        }
    }

    complete_apps = ['newsletter']