# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProjectCategory'
        db.create_table(u'crowdfunding_projectcategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['crowdfunding.ProjectCategory'])),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'crowdfunding', ['ProjectCategory'])

        # Adding model 'Project'
        db.create_table(u'crowdfunding_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.CustomUser'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['location.Location'])),
            ('location_detail', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crowdfunding.ProjectCategory'])),
            ('total_money', self.gf('django.db.models.fields.FloatField')()),
            ('total_days', self.gf('django.db.models.fields.IntegerField')()),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('now_money', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('status', self.gf('django.db.models.fields.CharField')(default='underway', max_length=20)),
            ('attention_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('post_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modify_datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'crowdfunding', ['Project'])

        # Adding model 'ProjectCover'
        db.create_table(u'crowdfunding_projectcover', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crowdfunding.Project'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'crowdfunding', ['ProjectCover'])

        # Adding model 'ProjectFeedback'
        db.create_table(u'crowdfunding_projectfeedback', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crowdfunding.Project'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'crowdfunding', ['ProjectFeedback'])

        # Adding model 'ProjectPackage'
        db.create_table(u'crowdfunding_projectpackage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crowdfunding.Project'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('money', self.gf('django.db.models.fields.FloatField')()),
            ('type', self.gf('django.db.models.fields.CharField')(default='normal', max_length=10)),
            ('limit', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'crowdfunding', ['ProjectPackage'])

        # Adding M2M table for field feedback on 'ProjectPackage'
        m2m_table_name = db.shorten_name(u'crowdfunding_projectpackage_feedback')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('projectpackage', models.ForeignKey(orm[u'crowdfunding.projectpackage'], null=False)),
            ('projectfeedback', models.ForeignKey(orm[u'crowdfunding.projectfeedback'], null=False))
        ))
        db.create_unique(m2m_table_name, ['projectpackage_id', 'projectfeedback_id'])

        # Adding model 'ProjectAttention'
        db.create_table(u'crowdfunding_projectattention', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crowdfunding.Project'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.CustomUser'])),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'crowdfunding', ['ProjectAttention'])

        # Adding model 'ProjectSupport'
        db.create_table(u'crowdfunding_projectsupport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crowdfunding.Project'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.CustomUser'])),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crowdfunding.ProjectPackage'])),
            ('money', self.gf('django.db.models.fields.FloatField')()),
            ('status', self.gf('django.db.models.fields.IntegerField')()),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'crowdfunding', ['ProjectSupport'])

        # Adding model 'ProjectRetention'
        db.create_table(u'crowdfunding_projectretention', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crowdfunding.Project'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.CustomUser'])),
            ('apiration', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('datetime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'crowdfunding', ['ProjectRetention'])


    def backwards(self, orm):
        # Deleting model 'ProjectCategory'
        db.delete_table(u'crowdfunding_projectcategory')

        # Deleting model 'Project'
        db.delete_table(u'crowdfunding_project')

        # Deleting model 'ProjectCover'
        db.delete_table(u'crowdfunding_projectcover')

        # Deleting model 'ProjectFeedback'
        db.delete_table(u'crowdfunding_projectfeedback')

        # Deleting model 'ProjectPackage'
        db.delete_table(u'crowdfunding_projectpackage')

        # Removing M2M table for field feedback on 'ProjectPackage'
        db.delete_table(db.shorten_name(u'crowdfunding_projectpackage_feedback'))

        # Deleting model 'ProjectAttention'
        db.delete_table(u'crowdfunding_projectattention')

        # Deleting model 'ProjectSupport'
        db.delete_table(u'crowdfunding_projectsupport')

        # Deleting model 'ProjectRetention'
        db.delete_table(u'crowdfunding_projectretention')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'crowdfunding.project': {
            'Meta': {'object_name': 'Project'},
            'attention_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crowdfunding.ProjectCategory']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['location.Location']"}),
            'location_detail': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'modify_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'now_money': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'post_datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'underway'", 'max_length': '20'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'total_days': ('django.db.models.fields.IntegerField', [], {}),
            'total_money': ('django.db.models.fields.FloatField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.CustomUser']"})
        },
        u'crowdfunding.projectattention': {
            'Meta': {'object_name': 'ProjectAttention'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crowdfunding.Project']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.CustomUser']"})
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
        u'crowdfunding.projectretention': {
            'Meta': {'object_name': 'ProjectRetention'},
            'apiration': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crowdfunding.Project']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.CustomUser']"})
        },
        u'crowdfunding.projectsupport': {
            'Meta': {'object_name': 'ProjectSupport'},
            'datetime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'money': ('django.db.models.fields.FloatField', [], {}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crowdfunding.ProjectPackage']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['crowdfunding.Project']"}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.CustomUser']"})
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
        },
        u'users.customuser': {
            'Meta': {'object_name': 'CustomUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"})
        }
    }

    complete_apps = ['crowdfunding']