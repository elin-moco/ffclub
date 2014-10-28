# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ColorBundle'
        db.create_table('thememaker_colorbundle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('bg_color', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('font_color', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('thememaker', ['ColorBundle'])

        # Adding model 'ThemeCategory'
        db.create_table('thememaker_themecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2047, blank=True)),
            ('enabled', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('thememaker', ['ThemeCategory'])

        # Adding model 'ThemeTemplate'
        db.create_table('thememaker_themetemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2047, blank=True)),
            ('template_image', self.gf('django.db.models.fields.files.ImageField')(max_length=255, db_index=True)),
            ('icon_image', self.gf('django.db.models.fields.files.ImageField')(max_length=255, db_index=True)),
            ('edit_image', self.gf('django.db.models.fields.files.ImageField')(max_length=255, db_index=True)),
            ('color', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['thememaker.ColorBundle'])),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['thememaker.ThemeCategory'])),
            ('used', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('enabled', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('thememaker', ['ThemeTemplate'])

        # Adding model 'UserTheme'
        db.create_table('thememaker_usertheme', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2047, blank=True)),
            ('header_image', self.gf('django.db.models.fields.files.ImageField')(max_length=255, db_index=True)),
            ('icon_image', self.gf('django.db.models.fields.files.ImageField')(max_length=255, db_index=True)),
            ('preview_image', self.gf('django.db.models.fields.files.ImageField')(max_length=255, db_index=True)),
            ('bg_color', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('font_color', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('template', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['thememaker.ThemeTemplate'], null=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['thememaker.ThemeCategory'], null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('enabled', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('covered', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('viewed', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('download', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('likes', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('thememaker', ['UserTheme'])


    def backwards(self, orm):
        # Deleting model 'ColorBundle'
        db.delete_table('thememaker_colorbundle')

        # Deleting model 'ThemeCategory'
        db.delete_table('thememaker_themecategory')

        # Deleting model 'ThemeTemplate'
        db.delete_table('thememaker_themetemplate')

        # Deleting model 'UserTheme'
        db.delete_table('thememaker_usertheme')


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
        'thememaker.colorbundle': {
            'Meta': {'object_name': 'ColorBundle'},
            'bg_color': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'font_color': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'thememaker.themecategory': {
            'Meta': {'object_name': 'ThemeCategory'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2047', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'thememaker.themetemplate': {
            'Meta': {'object_name': 'ThemeTemplate'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['thememaker.ThemeCategory']"}),
            'color': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['thememaker.ColorBundle']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2047', 'blank': 'True'}),
            'edit_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'db_index': 'True'}),
            'enabled': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'icon_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'template_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'used': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'thememaker.usertheme': {
            'Meta': {'object_name': 'UserTheme'},
            'bg_color': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['thememaker.ThemeCategory']", 'null': 'True'}),
            'covered': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2047', 'blank': 'True'}),
            'download': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'enabled': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'font_color': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'header_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'db_index': 'True'}),
            'icon_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'likes': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'preview_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '255', 'db_index': 'True'}),
            'template': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['thememaker.ThemeTemplate']", 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'viewed': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['thememaker']