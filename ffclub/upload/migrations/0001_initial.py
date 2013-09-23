# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ImageUpload'
        db.create_table('upload_imageupload', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usage', self.gf('django.db.models.fields.CharField')(default='original', max_length=20)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('status', self.gf('django.db.models.fields.CharField')(default='normal', max_length=20)),
            ('image_large', self.gf('django.db.models.fields.files.ImageField')(max_length=255, db_index=True)),
            ('create_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['contenttypes.ContentType'])),
            ('entity_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('image_medium', self.gf('django.db.models.fields.files.ImageField')(db_index=True, max_length=255, null=True, blank=True)),
            ('image_small', self.gf('django.db.models.fields.files.ImageField')(db_index=True, max_length=255, null=True, blank=True)),
            ('image_large_width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('image_large_height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('image_medium_width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('image_medium_height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('image_small_width', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('image_small_height', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('upload', ['ImageUpload'])


    def backwards(self, orm):
        # Deleting model 'ImageUpload'
        db.delete_table('upload_imageupload')


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
        'upload.imageupload': {
            'Meta': {'object_name': 'ImageUpload'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['contenttypes.ContentType']"}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'create_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'entity_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_large': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'db_index': 'True'}),
            'image_large_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'image_large_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'image_medium': ('django.db.models.fields.files.ImageField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_medium_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'image_medium_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'image_small': ('django.db.models.fields.files.ImageField', [], {'db_index': 'True', 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_small_height': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'image_small_width': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '20'}),
            'usage': ('django.db.models.fields.CharField', [], {'default': "'original'", 'max_length': '20'})
        }
    }

    complete_apps = ['upload']