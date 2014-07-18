# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
from annoying.functions import get_config
from DjangoUeditor.models import UEditorField

from apps.location.models import Location


class ProjectCategory(MPTTModel):
    """
    菜系分类 model

    """
    name = models.CharField(u'菜系分类名称', max_length=30)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u'分类父亲')
    order = models.PositiveIntegerField()

    def __unicode__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['order']

    class Meta:
        verbose_name = u'菜系分类'
        verbose_name_plural = u'菜系分类'
        permissions = (
            ('view_projectcategory', u'Can view 菜系分类'),
        )

    def save(self, *args, **kwargs):
        super(ProjectCategory, self).save(*args, **kwargs)
        ProjectCategory.objects.rebuild()

    def __unicode__(self):
        return self.name


class Project(models.Model):
    """
    项目 model

    """
    STATUS_DRAFT = 'draft'
    STATUS_PENDING = 'pending'
    STATUS_UNDERWAY = 'underway'
    STATUS_SUCCEED = 'succeed'
    STATUS_ENDED = 'ended'
    STATUS_RETENTION = 'retention'
    STATUS = (
        ('draft', u'草稿'),
        ('pending', u'等待审核'),
        ('underway', u'进行中'),
        ('succeed', u'已成功'),
        ('ended', u'已结束'),
        ('retention', u'滞留期'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'所属用户')
    name = models.CharField(u'项目名称', max_length=30)
    location = models.ForeignKey(Location, verbose_name=u'地理位置')
    location_detail = models.CharField(u'详细地址', max_length=255, blank=True, null=True)
    category = models.ForeignKey(ProjectCategory, verbose_name=u'菜系分类')
    total_money = models.FloatField(u'筹款金额')
    total_days = models.IntegerField(u'筹款天数')
    summary = models.CharField(u'项目简介', max_length=255)
    content = UEditorField(u'项目内容', width=600, height=300, toolbars='full',
                           imagePath=get_config('UPLOAD_CROWDFUNDING_PROJECT_IMAGES', 'crowdfunding/project/images/'),
                           filePath=get_config('UPLOAD_CROWDFUNDING_PROJECT_FILES', 'crowdfunding/project/files/'),
                           settings={})
    now_money = models.FloatField(u'已筹集金额', default=0)
    status = models.CharField(u'项目状态', choices=STATUS, default=STATUS_DRAFT, max_length=20)
    attention_count = models.IntegerField(u'项目关注数目', default=0)
    post_datetime = models.DateTimeField(u'发布日期', auto_now_add=True)
    modify_datetime = models.DateTimeField(u'最后修改日期', auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'项目'
        verbose_name_plural = u'项目'
        permissions = (
            ('view_project', u'Can view 项目'),
        )


class ProjectCover(models.Model):
    """
    项目封面 model

    """
    project = models.ForeignKey(Project, verbose_name=u'所属项目')
    image = models.ImageField(u'图片文件', upload_to=get_config(
        'UPLOAD_CROWDFUNDING_PROJECT_COVER', 'crowdfunding/project/cover/'
    ))
    order = models.IntegerField(u'排列顺序', default=0)

    def __unicode__(self):
        return self.image

    class Meta:
        verbose_name = u'项目封面'
        verbose_name_plural = u'项目封面'
        permissions = (
            ('view_projectcover', u'Can view 项目封面'),
        )


class ProjectFeedback(models.Model):
    """
    项目回馈描述 model

    """
    project = models.ForeignKey(Project, verbose_name=u'所属项目')
    content = models.TextField(u'回报描述')
    image = models.ImageField(u'图片描述', upload_to=get_config(
        'UPLOAD_CROWDFUNDING_PROJECT_FEEDBACK', 'crowdfunding/project/feedback/'
    ), blank=True, null=True)
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
    TYPE_NORMAL = 'normal'
    TYPE_PARTNER = 'partner'
    TYPE = (
        (TYPE_NORMAL, u'普通赞助者'),
        (TYPE_PARTNER, u'合伙人'),
    )

    project = models.ForeignKey(Project, verbose_name=u'所属项目')
    name = models.CharField(u'套餐名称', max_length=30)
    money = models.FloatField(u'投资数额')
    type = models.CharField(u'投资类别', choices=TYPE, default=TYPE_NORMAL, max_length=10)
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


class ProjectAttention(models.Model):
    """
    项目关注表

    """
    project = models.ForeignKey(Project, verbose_name=u'所属项目')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'所属用户')
    datetime = models.DateTimeField(u'关注日期', auto_now=True)

    class Meta:
        verbose_name = u'项目关注表'
        verbose_name_plural = u'项目关注表'
        permissions = (
            ('view_projectattention', u'Can view 项目关注'),
        )


class ProjectSupport(models.Model):
    """
    项目支持表

    """
    project = models.ForeignKey(Project, verbose_name=u'所属项目')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'所属用户')
    package = models.ForeignKey(ProjectPackage, verbose_name=u'所属回馈套餐')
    money = models.FloatField(u'支持金额')
    status = models.IntegerField(u'当前状态', help_text=u'0: 支持中 1: 支持成功 2: 支持失败,已退回')
    datetime = models.DateTimeField(u'支持日期', auto_now=True)

    class Meta:
        verbose_name = u'项目支持表'
        verbose_name_plural = u'项目支持表'
        permissions = (
            ('view_projectsupport', u'Can view 项目支持'),
        )


class ProjectRetention(models.Model):
    """
    项目滞留期意愿表

    """
    project = models.ForeignKey(Project, verbose_name=u'所属项目')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=u'所属用户')
    apiration = models.IntegerField(u'继续投资意愿', default=0, help_text=u'0: 不确定 1: 继续投资 2: 放弃投资')
    datetime = models.DateTimeField(u'支持日期', auto_now=True)

    class Meta:
        verbose_name = u'项目滞留期意愿表'
        verbose_name_plural = u'项目滞留期意愿表'
        permissions = (
            ('view_projectretention', u'Can view 项目滞留期意愿'),
        )