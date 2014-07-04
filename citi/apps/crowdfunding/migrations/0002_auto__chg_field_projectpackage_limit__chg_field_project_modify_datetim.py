# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ProjectPackage.limit'
        db.alter_column(u'crowdfunding_projectpackage', 'limit', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Project.modify_datetime'
        db.alter_column(u'crowdfunding_project', 'modify_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'Project.post_datetime'
        db.alter_column(u'crowdfunding_project', 'post_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

    def backwards(self, orm):

        # Changing field 'ProjectPackage.limit'
        db.alter_column(u'crowdfunding_projectpackage', 'limit', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Project.modify_datetime'
        db.alter_column(u'crowdfunding_project', 'modify_datetime', self.gf('django.db.models.fields.DateTimeField')())

        # Changing field 'Project.post_datetime'
        db.alter_column(u'crowdfunding_project', 'post_datetime', self.gf('django.db.models.fields.DateTimeField')())

    models = {
        u'crowdfunding.project': {
            'Meta': {'object_name': 'Project'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crowdfunding.ProjectCategory']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['location.Location']"}),
            'location_detail': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'modify_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'now_money': ('django.db.models.fields.FloatField', [], {}),
            'post_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'underway'", 'max_length': '10'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'total_days': ('django.db.models.fields.IntegerField', [], {}),
            'total_money': ('django.db.models.fields.FloatField', [], {})
        },
        u'crowdfunding.projectcategory': {
            'Meta': {'object_name': 'ProjectCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['crowdfunding.ProjectCategory']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'crowdfunding.projectcover': {
            'Meta': {'object_name': 'ProjectCover'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crowdfunding.Project']"})
        },
        u'crowdfunding.projectfeedback': {
            'Meta': {'object_name': 'ProjectFeedback'},
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crowdfunding.Project']"})
        },
        u'crowdfunding.projectpackage': {
            'Meta': {'object_name': 'ProjectPackage'},
            'feedback': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['crowdfunding.ProjectFeedback']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'money': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crowdfunding.Project']"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '10'})
        },
        u'location.location': {
            'Meta': {'object_name': 'Location'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['location.Location']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['crowdfunding']