# -*- coding: utf-8 -*-

from django.db import models


class Order(models.Model):
    """
    订单信息表

    """
    sn = models.CharField(u'订单编号', max_length=25, unique=True)
    user_id = models.IntegerField(u'用户ID')
    user_email = models.EmailField(u'用户电子邮件', max_length=255)
    order_type = models.IntegerField(u'订单类型', help_text=u'0: 充值 1: 提现 2: 项目支持 3: 项目支持失败, 资金退回 4: 项目支持成功，资金转入发起人账户')
    order_status = models.IntegerField(u'订单状态', help_text=u'0: 已确认 1: 已取消 2: 无效订单')
    order_content = models.TextField(u'订单内容', null=True, blank=True)
    pay_status = models.IntegerField(u'支付状态', help_text=u'0: 未付款 1: 已付款')
    pay_way = models.IntegerField(u'支付方式', help_text=u'0: 支付宝')
    sender_type = models.IntegerField(u'发送方类型', help_text=u'0: 支付宝 1: 系统 2: 用户')
    sender_id = models.IntegerField(u'发送方用户ID')
    sender_email = models.EmailField(u'发送方电子邮件', max_length=255)
    money = models.FloatField(u'总金额')
    add_datetime = models.DateTimeField(u'订单生成时间', auto_now_add=True)
    pay_datetime = models.DateTimeField(u'订单支付时间')

    class Meta:
        verbose_name = u'订单信息表'
        verbose_name_plural = u'订单信息表'


class Trade(models.Model):
    """
    交易记录表

    """
    order_id = models.IntegerField(u'所属订单ID')
    sn = models.CharField(u'订单编号', max_length=25, unique=True)
    user_id = models.IntegerField(u'用户ID')
    user_email = models.EmailField(u'用户电子邮件', max_length=255)
    money = models.FloatField(u'交易金额')
    balance = models.FloatField(u'交易后余额')
    datetime = models.DateTimeField(u'交易日期', auto_now_add=True)

    class Meta:
        verbose_name = u'交易记录表'
        verbose_name_plural = u'交易记录表'