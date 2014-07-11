# -*- coding: utf-8 -*-

"""
该文件用于在第一次 syncdb 时新建用户组及用户组权限。

有三个用户组，分别为admin, nocertification, certification

该表需手工维护，其中管理员权限表为所有权限, 可直接复制并修改

命令用法：

    ./manage.py create_group

"""

from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission


class Command(BaseCommand):
    args = ''
    help = 'Create groups and permissions of citi.'

    def handle(self, *args, **options):
        group_perms = {
            u'admin': {
                'perms': (
                    u'add_location',
                    u'change_location',
                    u'delete_location',
                    u'view_location',
                    u'add_order',
                    u'change_order',
                    u'delete_order',
                    u'view_order',
                    u'add_trade',
                    u'change_trade',
                    u'delete_trade',
                    u'view_trade',
                    u'add_projectcategory',
                    u'change_projectcategory',
                    u'delete_projectcategory',
                    u'view_projectcategory',
                    u'add_project',
                    u'change_project',
                    u'delete_project',
                    u'view_project',
                    u'add_projectcover',
                    u'change_projectcover',
                    u'delete_projectcover',
                    u'view_projectcover',
                    u'add_projectfeedback',
                    u'change_projectfeedback',
                    u'delete_projectfeedback',
                    u'view_projectfeedback',
                    u'add_projectpackage',
                    u'change_projectpackage',
                    u'delete_projectpackage',
                    u'view_projectpackage',
                    u'add_projectattention',
                    u'change_projectattention',
                    u'delete_projectattention',
                    u'view_projectattention',
                    u'add_projectsupport',
                    u'change_projectsupport',
                    u'delete_projectsupport',
                    u'view_projectsupport',
                    u'add_projectretention',
                    u'change_projectretention',
                    u'delete_projectretention',
                    u'view_projectretention',
                    u'add_question',
                    u'change_question',
                    u'delete_question',
                    u'view_question',
                    u'add_questionanswer',
                    u'change_questionanswer',
                    u'delete_questionanswer',
                    u'view_questionanswer',
                    u'add_questioncomment',
                    u'change_questioncomment',
                    u'delete_questioncomment',
                    u'view_questioncomment',
                    u'add_questionattention',
                    u'change_questionattention',
                    u'delete_questionattention',
                    u'view_questionattention',
                    u'add_questionanswervote',
                    u'change_questionanswervote',
                    u'delete_questionanswervote',
                    u'view_questionanswervote',
                )
            },
            u'certification': {
                'perms': (
                    u'add_project',
                    u'change_project',
                    u'delete_project',
                    u'view_project',
                    u'add_projectcover',
                    u'change_projectcover',
                    u'delete_projectcover',
                    u'view_projectcover',
                    u'add_projectfeedback',
                    u'change_projectfeedback',
                    u'delete_projectfeedback',
                    u'view_projectfeedback',
                    u'add_projectpackage',
                    u'change_projectpackage',
                    u'delete_projectpackage',
                    u'view_projectpackage',
                    u'add_projectattention',
                    u'change_projectattention',
                    u'delete_projectattention',
                    u'view_projectattention',
                    u'add_projectsupport',
                    u'change_projectsupport',
                    u'delete_projectsupport',
                    u'view_projectsupport',
                    u'add_projectretention',
                    u'change_projectretention',
                    u'delete_projectretention',
                    u'view_projectretention',
                    u'add_question',
                    u'change_question',
                    u'delete_question',
                    u'view_question',
                    u'add_questionanswer',
                    u'change_questionanswer',
                    u'delete_questionanswer',
                    u'view_questionanswer',
                    u'add_questioncomment',
                    u'change_questioncomment',
                    u'delete_questioncomment',
                    u'view_questioncomment',
                    u'add_questionattention',
                    u'change_questionattention',
                    u'delete_questionattention',
                    u'view_questionattention',
                    u'add_questionanswervote',
                    u'change_questionanswervote',
                    u'delete_questionanswervote',
                    u'view_questionanswervote',
                )
            },
            u'nocertification': {
                'perms': (
                    u'view_project',
                    u'view_projectcover',
                    u'view_projectfeedback',
                    u'view_projectpackage',
                    u'add_projectattention',
                    u'change_projectattention',
                    u'delete_projectattention',
                    u'view_projectattention',
                    u'add_projectsupport',
                    u'change_projectsupport',
                    u'delete_projectsupport',
                    u'view_projectsupport',
                    u'add_projectretention',
                    u'change_projectretention',
                    u'delete_projectretention',
                    u'view_projectretention',
                    u'add_question',
                    u'change_question',
                    u'delete_question',
                    u'view_question',
                    u'add_questionanswer',
                    u'change_questionanswer',
                    u'delete_questionanswer',
                    u'view_questionanswer',
                    u'add_questioncomment',
                    u'change_questioncomment',
                    u'delete_questioncomment',
                    u'view_questioncomment',
                    u'add_questionattention',
                    u'change_questionattention',
                    u'delete_questionattention',
                    u'view_questionattention',
                    u'add_questionanswervote',
                    u'change_questionanswervote',
                    u'delete_questionanswervote',
                    u'view_questionanswervote',
                )
            },
        }

        for group_name in group_perms.keys():
            group, created = Group.objects.get_or_create(name=group_name)
            for perm_codename in group_perms[group_name]['perms']:
                try:
                    perm = Permission.objects.get(codename=perm_codename)
                    group.permissions.add(perm)
                except ObjectDoesNotExist:
                    raise CommandError('Error when insert permissions "%(codename)s" into table.' % {'codename': perm_codename})
            group.save()

        self.stdout.write('Successfully create groups and permissions.')