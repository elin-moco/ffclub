# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Product'
        db.create_table('product_product', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('product', ['Product'])

        # Adding model 'Order'
        db.create_table('product_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('usage', self.gf('django.db.models.fields.TextField')(max_length=512)),
            ('fullname', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('occupation', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('feedback', self.gf('django.db.models.fields.TextField')(default='', max_length=512, blank=True)),
            ('create_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['event.Event'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='wait_for_confirm', max_length=20)),
        ))
        db.send_create_signal('product', ['Order'])

        # Adding model 'OrderDetail'
        db.create_table('product_orderdetail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('quantity', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='details', to=orm['product.Order'])),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['product.Product'])),
        ))
        db.send_create_signal('product', ['OrderDetail'])

        # Adding model 'OrderVerification'
        db.create_table('product_orderverification', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('create_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('status', self.gf('django.db.models.fields.CharField')(default='issued', max_length=20)),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['product.Order'])),
        ))
        db.send_create_signal('product', ['OrderVerification'])


    def backwards(self, orm):
        # Deleting model 'Product'
        db.delete_table('product_product')

        # Deleting model 'Order'
        db.delete_table('product_order')

        # Deleting model 'OrderDetail'
        db.delete_table('product_orderdetail')

        # Deleting model 'OrderVerification'
        db.delete_table('product_orderverification')


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
        'event.event': {
            'Meta': {'object_name': 'Event'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'create_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'num_of_ppl': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'product.order': {
            'Meta': {'object_name': 'Order'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'create_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['event.Event']"}),
            'feedback': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'occupation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'+'", 'symmetrical': 'False', 'through': "orm['product.OrderDetail']", 'to': "orm['product.Product']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'wait_for_confirm'", 'max_length': '20'}),
            'usage': ('django.db.models.fields.TextField', [], {'max_length': '512'})
        },
        'product.orderdetail': {
            'Meta': {'object_name': 'OrderDetail'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'details'", 'to': "orm['product.Order']"}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['product.Product']"}),
            'quantity': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'product.orderverification': {
            'Meta': {'object_name': 'OrderVerification'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'create_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['product.Order']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'issued'", 'max_length': '20'})
        },
        'product.product': {
            'Meta': {'object_name': 'Product'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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

    complete_apps = ['product']