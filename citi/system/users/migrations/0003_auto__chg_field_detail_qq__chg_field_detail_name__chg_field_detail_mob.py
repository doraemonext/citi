# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Detail.qq'
        db.alter_column(u'users_detail', 'qq', self.gf('django.db.models.fields.CharField')(max_length=15, null=True))

        # Changing field 'Detail.name'
        db.alter_column(u'users_detail', 'name', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'Detail.mobile'
        db.alter_column(u'users_detail', 'mobile', self.gf('django.db.models.fields.CharField')(max_length=15, null=True))

        # Changing field 'Detail.age'
        db.alter_column(u'users_detail', 'age', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Detail.idcard'
        db.alter_column(u'users_detail', 'idcard', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'Detail.sex'
        db.alter_column(u'users_detail', 'sex', self.gf('django.db.models.fields.CharField')(max_length=1, null=True))

        # Changing field 'Detail.avatar'
        db.alter_column(u'users_detail', 'avatar', self.gf('awesome_avatar.fields.AvatarField')(max_length=100, null=True))

        # Changing field 'FundInfo.alipay'
        db.alter_column(u'users_fundinfo', 'alipay', self.gf('django.db.models.fields.CharField')(max_length=100, null=True))

        # Changing field 'FundInfo.bank_name'
        db.alter_column(u'users_fundinfo', 'bank_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'FundInfo.account'
        db.alter_column(u'users_fundinfo', 'account', self.gf('django.db.models.fields.CharField')(max_length=30, null=True))

        # Changing field 'FundInfo.bank_sub_name'
        db.alter_column(u'users_fundinfo', 'bank_sub_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'FundInfo.name'
        db.alter_column(u'users_fundinfo', 'name', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Detail.qq'
        raise RuntimeError("Cannot reverse this migration. 'Detail.qq' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Detail.qq'
        db.alter_column(u'users_detail', 'qq', self.gf('django.db.models.fields.CharField')(max_length=15))

        # User chose to not deal with backwards NULL issues for 'Detail.name'
        raise RuntimeError("Cannot reverse this migration. 'Detail.name' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Detail.name'
        db.alter_column(u'users_detail', 'name', self.gf('django.db.models.fields.CharField')(max_length=20))

        # User chose to not deal with backwards NULL issues for 'Detail.mobile'
        raise RuntimeError("Cannot reverse this migration. 'Detail.mobile' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Detail.mobile'
        db.alter_column(u'users_detail', 'mobile', self.gf('django.db.models.fields.CharField')(max_length=15))

        # User chose to not deal with backwards NULL issues for 'Detail.age'
        raise RuntimeError("Cannot reverse this migration. 'Detail.age' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Detail.age'
        db.alter_column(u'users_detail', 'age', self.gf('django.db.models.fields.IntegerField')())

        # User chose to not deal with backwards NULL issues for 'Detail.idcard'
        raise RuntimeError("Cannot reverse this migration. 'Detail.idcard' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Detail.idcard'
        db.alter_column(u'users_detail', 'idcard', self.gf('django.db.models.fields.CharField')(max_length=20))

        # User chose to not deal with backwards NULL issues for 'Detail.sex'
        raise RuntimeError("Cannot reverse this migration. 'Detail.sex' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Detail.sex'
        db.alter_column(u'users_detail', 'sex', self.gf('django.db.models.fields.CharField')(max_length=1))

        # User chose to not deal with backwards NULL issues for 'Detail.avatar'
        raise RuntimeError("Cannot reverse this migration. 'Detail.avatar' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Detail.avatar'
        db.alter_column(u'users_detail', 'avatar', self.gf('awesome_avatar.fields.AvatarField')(max_length=100))

        # User chose to not deal with backwards NULL issues for 'FundInfo.alipay'
        raise RuntimeError("Cannot reverse this migration. 'FundInfo.alipay' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'FundInfo.alipay'
        db.alter_column(u'users_fundinfo', 'alipay', self.gf('django.db.models.fields.CharField')(max_length=100))

        # User chose to not deal with backwards NULL issues for 'FundInfo.bank_name'
        raise RuntimeError("Cannot reverse this migration. 'FundInfo.bank_name' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'FundInfo.bank_name'
        db.alter_column(u'users_fundinfo', 'bank_name', self.gf('django.db.models.fields.CharField')(max_length=50))

        # User chose to not deal with backwards NULL issues for 'FundInfo.account'
        raise RuntimeError("Cannot reverse this migration. 'FundInfo.account' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'FundInfo.account'
        db.alter_column(u'users_fundinfo', 'account', self.gf('django.db.models.fields.CharField')(max_length=30))

        # User chose to not deal with backwards NULL issues for 'FundInfo.bank_sub_name'
        raise RuntimeError("Cannot reverse this migration. 'FundInfo.bank_sub_name' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'FundInfo.bank_sub_name'
        db.alter_column(u'users_fundinfo', 'bank_sub_name', self.gf('django.db.models.fields.CharField')(max_length=50))

        # User chose to not deal with backwards NULL issues for 'FundInfo.name'
        raise RuntimeError("Cannot reverse this migration. 'FundInfo.name' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'FundInfo.name'
        db.alter_column(u'users_fundinfo', 'name', self.gf('django.db.models.fields.CharField')(max_length=20))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'users.detail': {
            'Meta': {'object_name': 'Detail'},
            'age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'avatar': ('awesome_avatar.fields.AvatarField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idcard': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'qq': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'sex': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'users.fundinfo': {
            'Meta': {'object_name': 'FundInfo'},
            'account': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'alipay': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'bank_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'bank_sub_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['users']