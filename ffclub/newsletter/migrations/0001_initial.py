# -*- coding: utf-8 -*-
import datetime
from south.db import dbs
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Newsletter'
        dbs['newsletter'].create_table(u'issue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('issue', self.gf('django.db.models.fields.DateField')()),
            ('volume', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('publish_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now)),
        ))
        dbs['newsletter'].send_create_signal('newsletter', ['Newsletter'])

        # Adding model 'Subscription'
        dbs['newsletter'].create_table(u'newsletter', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.TextField')(db_column='u_email')),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1, db_column='u_status')),
            ('edit_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime.now)),
        ))
        dbs['newsletter'].send_create_signal('newsletter', ['Subscription'])


    def backwards(self, orm):
        # Deleting model 'Newsletter'
        dbs['newsletter'].delete_table(u'issue')

        # Deleting model 'Subscription'
        dbs['newsletter'].delete_table(u'newsletter')


    models = {
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