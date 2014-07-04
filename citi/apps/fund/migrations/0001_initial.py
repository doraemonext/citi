# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Order'
        db.create_table(u'fund_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sn', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')()),
            ('user_email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('order_type', self.gf('django.db.models.fields.IntegerField')()),
            ('order_status', self.gf('django.db.models.fields.IntegerField')()),
            ('order_content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('pay_status', self.gf('django.db.models.fields.IntegerField')()),
            ('pay_way', self.gf('django.db.models.fields.IntegerField')()),
            ('sender_type', self.gf('django.db.models.fields.IntegerField')()),
            ('sender_id', self.gf('django.db.models.fields.IntegerField')()),
            ('sender_email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('money', self.gf('django.db.models.fields.FloatField')()),
            ('add_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('pay_datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'fund', ['Order'])

        # Adding model 'Trade'
        db.create_table(u'fund_trade', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order_id', self.gf('django.db.models.fields.IntegerField')()),
            ('sn', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')()),
            ('user_email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('money', self.gf('django.db.models.fields.FloatField')()),
            ('balance', self.gf('django.db.models.fields.FloatField')()),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'fund', ['Trade'])


    def backwards(self, orm):
        # Deleting model 'Order'
        db.delete_table(u'fund_order')

        # Deleting model 'Trade'
        db.delete_table(u'fund_trade')


    models = {
        u'fund.order': {
            'Meta': {'object_name': 'Order'},
            'add_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'money': ('django.db.models.fields.FloatField', [], {}),
            'order_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'order_status': ('django.db.models.fields.IntegerField', [], {}),
            'order_type': ('django.db.models.fields.IntegerField', [], {}),
            'pay_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'pay_status': ('django.db.models.fields.IntegerField', [], {}),
            'pay_way': ('django.db.models.fields.IntegerField', [], {}),
            'sender_email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'sender_id': ('django.db.models.fields.IntegerField', [], {}),
            'sender_type': ('django.db.models.fields.IntegerField', [], {}),
            'sn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'user_email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'fund.trade': {
            'Meta': {'object_name': 'Trade'},
            'balance': ('django.db.models.fields.FloatField', [], {}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'money': ('django.db.models.fields.FloatField', [], {}),
            'order_id': ('django.db.models.fields.IntegerField', [], {}),
            'sn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'user_email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['fund']