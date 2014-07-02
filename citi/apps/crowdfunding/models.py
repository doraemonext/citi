# -*- coding: utf-8 -*-

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from annoying.functions import get_config

from apps.location.models import Location


class ProjectCategory(MPTTModel):
    """
    菜系分类 model

    """
    name = models.CharField(u'菜系分类名称', max_length=30)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', verbose_name=u'分类父亲')

    def __unicode__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = u'菜系分类'
        verbose_name_plural = u'菜系分类'


class Project(models.Model):
    """
    项目 model

    """
    STATUS_UNDERWAY = 'underway'
    STATUS_SUCCEED = 'succeed'
    STATUS_ENDED = 'ended'
    STATUS = (
        ('underway', u'进行中'),
        ('succeed', u'已成功'),
        ('ended', u'已结束'),
    )

    name = models.CharField(u'项目名称', max_length=30)
    location = models.ForeignKey(Location, verbose_name=u'城市位置')
    location_detail = models.CharField(u'详细地址', max_length=255, blank=True, null=True)
    category = models.ForeignKey(ProjectCategory, verbose_name=u'菜系分类')
    total_money = models.FloatField(u'筹款金额')
    total_days = models.IntegerField(u'筹款天数')
    summary = models.CharField(u'项目简介', max_length=255)
    content = models.TextField(u'项目内容')
    now_money = models.FloatField(u'已筹集金额')
    status = models.CharField(u'项目状态', choices=STATUS, default=STATUS_UNDERWAY, max_length=10)
    post_datetime = models.DateTimeField(u'发布日期')
    modify_datetime = models.DateTimeField(u'最后修改日期')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'项目'
        verbose_name_plural = u'项目'


class ProjectCover(models.Model):
    """
    项目封面 model

    """
    project = models.ForeignKey(Project, verbose_name=u'对应项目')
    image = models.ImageField(u'图片文件', upload_to=get_config(
        'UPLOAD_CROWDFUNDING_PROJECT_COVER', 'crowdfunding/project/cover'
    ))
    order = models.IntegerField(u'排列顺序')

    def __unicode__(self):
        return self.image

    class Meta:
        verbose_name = u'项目封面'
        verbose_name_plural = u'项目封面'


class ProjectFeedback(models.Model):
    """
    项目回馈描述 model

    """
    project = models.ForeignKey(Project, verbose_name=u'对应项目')
    content = models.TextField(u'回报描述')
    image = models.ImageField(u'图片描述', upload_to=get_config(
        'UPLOAD_CROWDFUNDING_PROJECT_FEEDBACK', 'crowdfunding/project/feedback'
    ), blank=True, null=True)
    order = models.IntegerField(u'排列顺序')

    def __unicode__(self):
        return self.content

    class Meta:
        verbose_name = u'项目回馈描述'
        verbose_name_plural = u'项目回馈描述'


class ProjectPackage(models.Model):
    """
    项目回馈套餐方案 model

    """
    TYPE_NORMAL = 'normal'
    TYPE_PARTNER = 'partner'
    TYPE = (
        (TYPE_NORMAL, 'normal crowdfunding user'),
        (TYPE_PARTNER, 'partner user'),
    )

    project = models.ForeignKey(Project, verbose_name=u'对应项目')
    name = models.CharField(u'套餐名称', max_length=30)
    money = models.FloatField(u'投资数额')
    type = models.CharField(u'投资类别', choices=TYPE, default=TYPE_NORMAL, max_length=10)
    limit = models.IntegerField(u'名额限制', blank=True, null=True)
    feedback = models.ManyToManyField(ProjectFeedback, verbose_name=u'项目回馈')

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'项目回馈套餐方案'
        verbose_name_plural = u'项目回馈套餐方案'