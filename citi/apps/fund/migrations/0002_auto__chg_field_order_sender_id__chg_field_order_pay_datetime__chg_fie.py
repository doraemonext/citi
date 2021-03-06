# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Order.sender_id'
        db.alter_column(u'fund_order', 'sender_id', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Order.pay_datetime'
        db.alter_column(u'fund_order', 'pay_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'Order.sender_email'
        db.alter_column(u'fund_order', 'sender_email', self.gf('django.db.models.fields.EmailField')(max_length=255, null=True))

    def backwards(self, orm):

        # Changing field 'Order.sender_id'
        db.alter_column(u'fund_order', 'sender_id', self.gf('django.db.models.fields.IntegerField')(default=1))

        # Changing field 'Order.pay_datetime'
        db.alter_column(u'fund_order', 'pay_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 9, 4, 0, 0)))

        # Changing field 'Order.sender_email'
        db.alter_column(u'fund_order', 'sender_email', self.gf('django.db.models.fields.EmailField')(default='admin@admin.com', max_length=255))

    models = {
        u'fund.order': {
            'Meta': {'object_name': 'Order'},
            'add_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'money': ('django.db.models.fields.FloatField', [], {}),
            'order_content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'order_status': ('django.db.models.fields.IntegerField', [], {}),
            'order_type': ('django.db.models.fields.IntegerField', [], {}),
            'pay_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'pay_status': ('django.db.models.fields.IntegerField', [], {}),
            'pay_way': ('django.db.models.fields.IntegerField', [], {}),
            'sender_email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'sender_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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