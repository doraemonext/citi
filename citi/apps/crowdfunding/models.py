# -*- coding: utf-8 -*-

import logging

from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
from annoying.functions import get_config
from DjangoUeditor.models import UEditorField
from taggit.managers import TaggableManager

from apps.location.models import Location
from apps.image.models import Image
from libs.exceptions import AlreadyOperationException


logger = logging.getLogger(__name__)


class ProjectCategory(MPTTModel):
    """
    项目分类 model

    """
    name = models.CharField(u'项目分类名称', max_length=30)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u'分类父亲')
    order = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['order']

    class Meta:
        verbose_name = u'项目分类'
        verbose_name_plural = u'项目分类'
        permissions = (
            ('view_projectcategory', u'Can view 项目分类'),
        )

    def save(self, *args, **kwargs):
        super(ProjectCategory, self).save(*args, **kwargs)
        ProjectCategory.objects.rebuild()


class Project(models.Model):
    """
    项目 model

    """
    STATUS_DRAFT = 0
    STATUS_PENDING = 1
    STATUS_VERIFY_FAILED = 2
    STATUS_UNDERWAY = 3
    STATUS_SUCCEED = 4
    STATUS_ENDED = 5
    STATUS_RETENTION = 6
    STATUS = (
        (STATUS_DRAFT, u'草稿'),
        (STATUS_PENDING, u'等待审核'),
        (STATUS_VERIFY_FAILED, u'审核失败'),
        (STATUS_UNDERWAY, u'进行中'),
        (STATUS_SUCCEED, u'已成功'),
        (STATUS_ENDED, u'已结束'),
        (STATUS_RETENTION, u'停滞中'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'所属用户')
    name = models.CharField(u'项目名称', max_length=30)
    cover = models.IntegerField(u'项目封面ID')
    location = TreeForeignKey(Location, verbose_name=u'地理位置')
    location_detail = models.CharField(u'详细地址', max_length=255, blank=True, null=True)
    category = TreeForeignKey(ProjectCategory, verbose_name=u'项目分类')
    total_money = models.FloatField(u'筹款金额')
    total_days = models.IntegerField(u'筹款天数')
    summary = models.CharField(u'项目简介', max_length=255)
    content = UEditorField(u'项目内容', width=600, height=300, toolbars='full',
                           imagePath=get_config('UPLOAD_CROWDFUNDING_PROJECT_IMAGES', 'project/images/'),
                           filePath=get_config('UPLOAD_CROWDFUNDING_PROJECT_FILES', 'project/files/'),
                           settings={})
    now_money = models.FloatField(u'已筹集金额', default=0)
    status = models.IntegerField(u'项目状态', choices=STATUS, default=STATUS_DRAFT)
    attention_count = models.IntegerField(u'项目关注数目', default=0)
    tags = TaggableManager(u'标签', help_text='')
    post_datetime = models.DateTimeField(u'发布日期', auto_now_add=True)
    modify_datetime = models.DateTimeField(u'最后修改日期', auto_now=True)

    def __unicode__(self):
        return self.name

    def save_project(self):
        if self.status == self.STATUS_DRAFT:
            self.status = self.STATUS_PENDING
            self.save()

    class Meta:
        verbose_name = u'项目'
        verbose_name_plural = u'项目'
        permissions = (
            ('view_project', u'Can view 项目'),
        )


class ProjectFeedback(models.Model):
    """
    项目回馈描述 model

    """
    project = models.ForeignKey(Project, verbose_name=u'所属项目')
    content = models.TextField(u'回报描述')
    image = models.IntegerField(u'图片描述ID', blank=True, null=True)
    order = models.IntegerField(u'排列顺序', default=0)

    def __unicode__(self):
        return self.content

    class Meta:
        verbose_name = u'项目回馈描述'
        verbose_name_plural = u'项目回馈描述'
        permissions = (
            ('view_projectfeedback', u'Can view 项目回馈描述'),
        )


class ProjectPackage(models.Model):
    """
    项目回馈套餐方案 model

    """
    TYPE_NORMAL = 0
    TYPE_PARTNER = 1
    TYPE = (
        (TYPE_NORMAL, u'普通赞助者'),
        (TYPE_PARTNER, u'合伙人'),
    )

    project = models.ForeignKey(Project, verbose_name=u'所属项目')
    name = models.CharField(u'套餐名称', max_length=30)
    money = models.FloatField(u'投资数额')
    type = models.IntegerField(u'投资类别', choices=TYPE, default=TYPE_NORMAL)
    limit = models.IntegerField(u'名额限制', default=0)
    feedback = models.ManyToManyField(ProjectFeedback, verbose_name=u'项目回馈')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'项目回馈套餐方案'
        verbose_name_plural = u'项目回馈套餐方案'
        permissions = (
            ('view_projectpackage', u'Can view 项目回馈套餐方案'),
        )


class ProjectAttentionManager(models.Manager):
    def is_attention(self, project, user):
        """
        返回用户 user 是否关注项目 project

        """
        queryset = super(ProjectAttentionManager, self).get_queryset().filter(project=project).filter(user=user)
        if queryset.exists():
            return True
        else:
            return False

    def attention(self, project, user):
        """
        关注项目

        """
        queryset = super(ProjectAttentionManager, self).get_queryset().filter(project=project).filter(user=user)
        if not queryset.exists():
            super(ProjectAttentionManager, self).create(project=project, user=user)
            project.attention_count += 1
            project.save()

    def inattention(self, project, user):
        """
        取消关注项目

        """
        queryset = super(ProjectAttentionManager, self).get_queryset().filter(project=project).filter(user=user)
        if queryset.exists():
            queryset[0].delete()
            project.attention_count -= 1
            project.save()


class ProjectAttention(models.Model):
    """
    项目关注表

    """
    project = models.ForeignKey(Project, verbose_name=u'所属项目')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'所属用户')
    datetime = models.DateTimeField(u'关注日期', auto_now=True)

    class Meta:
        verbose_name = u'项目关注'
        verbose_name_plural = u'项目关注'
        permissions = (
            ('view_projectattention', u'Can view 项目关注'),
        )

    objects = models.Manager()
    manager = ProjectAttentionManager()


class ProjectSupportManager(models.Manager):
    def add_support(self, project, user, package, money):
        """
        用户 user 为项目 project 支持 package 套餐, 总金额为 money
        """
        super(ProjectSupportManager, self).create(project=project, user=user, package=package,
                                                  money=money, status=ProjectSupport.STATUS_UNDERWAY)

    def has_support(self, project, user):
        if super(ProjectSupportManager, self).get_queryset().filter(project=project).filter(user=user).exists():
            return True
        else:
            return False


class ProjectSupport(models.Model):
    """
    项目支持表

    """
    STATUS_UNDERWAY = 0
    STATUS_SUCCEED = 1
    STATUS_FAILED = 2
    STATUS = (
        (STATUS_UNDERWAY, u'支持中'),
        (STATUS_SUCCEED, u'支持成功'),
        (STATUS_FAILED, u'支持失败'),
    )

    project = models.ForeignKey(Project, verbose_name=u'所属项目')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'所属用户')
    package = models.ForeignKey(ProjectPackage, verbose_name=u'所属回馈套餐')
    money = models.FloatField(u'支持金额')
    status = models.IntegerField(u'支持状态', choices=STATUS, default=STATUS_UNDERWAY)
    datetime = models.DateTimeField(u'支持日期', auto_now=True)

    def succeed(self):
        self.status = self.STATUS_SUCCEED
        self.save()

    def fail(self):
        self.status = self.STATUS_FAILED
        self.save()

    class Meta:
        verbose_name = u'项目支持表'
        verbose_name_plural = u'项目支持表'
        permissions = (
            ('view_projectsupport', u'Can view 项目支持'),
        )

    objects = models.Manager()
    manager = ProjectSupportManager()


class ProjectRetention(models.Model):
    """
    项目滞留期意愿表

    """
    APIRATION_UNKNOWN = 0
    APIRATION_CONTINUE = 1
    APIRATION_QUIT = 2
    APIRATION = (
        (APIRATION_UNKNOWN, u'不确定'),
        (APIRATION_CONTINUE, u'继续投资'),
        (APIRATION_QUIT, u'放弃投资'),
    )

    project = models.ForeignKey(Project, verbose_name=u'所属项目')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'所属用户')
    apiration = models.IntegerField(u'继续投资意愿', choices=APIRATION, default=APIRATION_UNKNOWN)
    datetime = models.DateTimeField(u'支持日期', auto_now=True)

    class Meta:
        verbose_name = u'项目滞留期意愿表'
        verbose_name_plural = u'项目滞留期意愿表'
        permissions = (
            ('view_projectretention', u'Can view 项目滞留期意愿'),
        )


class ProjectComment(MPTTModel):
    """
    项目评论表

    """
    project = models.ForeignKey(Project, verbose_name=u'所属项目')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'所属用户', blank=True, null=True)
    content = models.TextField(u'评论内容')
    datetime = models.DateTimeField(u'评论日期', auto_now=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u'评论父亲')

    def __unicode__(self):
        return self.content

    class Meta:
        verbose_name = u'项目评论'
        verbose_name_plural = u'项目评论'
        permissions = (
            ('view_projectcomment', u'Can view 项目评论'),
        )

    def save(self, *args, **kwargs):
        super(ProjectComment, self).save(*args, **kwargs)
        ProjectComment.objects.rebuild()

    def get_user_email(self):
        if self.user:
            return self.user.email
        else:
            return None


class ProjectTopicManager(models.Manager):
    def add_topic(self, project, user, title, content):
        super(ProjectTopicManager, self).create(project=project, user=user, title=title, content=content)


class ProjectTopic(models.Model):
    """
    项目讨论主题表

    """
    project = models.ForeignKey(Project, verbose_name=u'所属项目')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'所属用户')
    title = models.CharField(u'主题标题', max_length=255)
    content = models.TextField(u'主题内容')
    post_datetime = models.DateTimeField(u'发布日期', auto_now_add=True)
    modify_datetime = models.DateTimeField(u'最后修改日期', auto_now=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'项目讨论主题'
        verbose_name_plural = u'项目讨论主题'
        permissions = (
            ('view_projecttopic', u'Can view 项目讨论主题'),
        )

    objects = models.Manager()
    manager = ProjectTopicManager()


class ProjectTopicComment(MPTTModel):
    """
    项目讨论主题评论表

    """
    project = models.ForeignKey(Project, verbose_name=u'所属项目')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'所属用户')
    content = models.TextField(u'评论内容')
    datetime = models.DateTimeField(u'评论日期', auto_now_add=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u'评论父亲')
    order = models.PositiveIntegerField(u'排序')

    def __unicode__(self):
        return self.content

    class MPTTMeta:
        order_insertion_by = ['order']

    class Meta:
        verbose_name = u'项目讨论主题评论'
        verbose_name_plural = u'项目讨论主题评论'
        permissions = (
            ('view_projecttopiccomment', u'Can view 项目讨论主题评论'),
        )

    def save(self, *args, **kwargs):
        super(ProjectTopicComment, self).save(*args, **kwargs)
        ProjectTopicComment.objects.rebuild()


class ProjectSection(models.Model):
    """
    项目资金去向阶段表

    """
    STATUS_NOT_DONE = 0
    STATUS_UNDERWAY = 1
    STATUS_DONE = 2
    STATUS = (
        (STATUS_NOT_DONE, u'尚未开始'),
        (STATUS_UNDERWAY, u'正在进行中'),
        (STATUS_DONE, u'已完成'),
    )

    project = models.ForeignKey(Project, verbose_name=u'所属项目')
    title = models.CharField(u'阶段名称', max_length=50)
    description = models.TextField(u'阶段需求描述')
    status = models.IntegerField(u'阶段状态', choices=STATUS, default=STATUS_NOT_DONE)
    order = models.PositiveIntegerField(u'项目阶段顺序')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = u'项目资金去向阶段'
        verbose_name_plural = u'项目资金去向阶段'
        permissions = (
            ('view_projectsection', u'Can view 项目资金去向阶段'),
        )


class ProjectTask(models.Model):
    """
    项目资金去向任务表

    """
    STATUS_NOT_DONE = 0
    STATUS_UNDERWAY = 1
    STATUS_DONE = 2
    STATUS = (
        (STATUS_NOT_DONE, u'尚未开始'),
        (STATUS_UNDERWAY, u'正在进行中'),
        (STATUS_DONE, u'已完成'),
    )

    project = models.ForeignKey(Project, verbose_name=u'所属项目')
    content = models.TextField(u'任务描述')
    status = models.IntegerField(u'任务状态', choices=STATUS, default=STATUS_NOT_DONE)
    order = models.PositiveIntegerField(u'项目任务顺序')

    def __unicode__(self):
        return self.content

    class Meta:
        verbose_name = u'项目资金去向任务'
        verbose_name_plural = u'项目资金去向任务'
        permissions = (
            ('view_projecttask', u'Can view 项目资金去向任务'),
        )
